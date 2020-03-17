import bpy
from bpy.props import (
    IntProperty,
    BoolProperty,
    StringProperty,
    EnumProperty,
    FloatVectorProperty,
    )
from ..cm_functions import (
    connected_node_midi,
    off_set,
    )

class CM_ND_MidiAnimNode(bpy.types.Node):
    bl_idname = "cm_audio_midi_anim_node"
    bl_label = "MIDI Object Animate"
    bl_width_default = 150
    """Multi-Animate One Object from MIDI Key, or Controls Data"""

    message : StringProperty(name="")
    object_name : StringProperty(name="Object", default="")
    anim_type: EnumProperty(
        items=(
            ("loc", "Location", "Animate Location"),
            ("rot", "Rotation", "Animate Rotation"),
            ("scl", "Scale", "Animate Scale"),
        ),
        name="Animate",
        default="loc",
        description="Animation Type",
    )
    midi_type: EnumProperty(
        items=(
            ("key", "Keys", "Use MIDI Keys"),
            ("con", "Controls", "Use MIDI Controls"),
        ),
        name="MIDI",
        default="key",
        description="MIDI Type",
    )
    factors : FloatVectorProperty(name="", subtype="XYZ", default=(1,1,1))
    con_px : IntProperty(name="X", default=32, min=-1, max=127)
    con_py : IntProperty(name="Y", default=48, min=-1, max=127)
    con_pz : IntProperty(name="Z", default=64, min=-1, max=127)
    use_bones : BoolProperty(name="Use Bones", default=False)
    bone_name : StringProperty(name="Bone", default="")

    def init(self, context):
        self.inputs.new("cm_socket.sound", "[Key, Control] Data")
        self.outputs.new("cm_socket.sound", "[Key, Control] Data")

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, "object_name")
        row.operator("cm_audio.get_target", text="", icon="STYLUS_PRESSURE")
        box = layout.box()
        box.prop(self, "anim_type")
        box.prop(self, "midi_type")
        row = box.row()
        row.prop(self, "factors")
        box.label(text="Controls")
        row = box.row()
        row.prop(self, "con_px")
        row.prop(self, "con_py")
        row.prop(self, "con_pz")
        box = layout.box()
        box.prop(self, "use_bones")
        box.prop(self, "bone_name")

    def get_midi(self):
        cm = bpy.context.scene.cm_pg
        buffer_in = connected_node_midi(self, 0)

        if self.object_name != "" and buffer_in is not None:
            tgt_obj = bpy.data.objects[self.object_name]
            if tgt_obj is not None:
                values = []
                if self.midi_type == "con":
                    num = 1
                else:
                    num = 0
                if self.con_px >= 0:
                    values.append(buffer_in[num][self.con_px] / 127)
                else:
                    values.append(0)
                if self.con_py >= 0:
                    values.append(buffer_in[num][self.con_py] / 127)
                else:
                    values.append(0)
                if self.con_pz >= 0:
                    values.append(buffer_in[num][self.con_pz] / 127)
                else:
                    values.append(0)

                vector_delta, euler_delta, scale_delta = off_set(values, self.factors)
                if self.use_bones and tgt_obj.type == "ARMATURE":
                    bone_list = [item for item in tgt_obj.pose.bones if item.name == self.bone_name]
                    if len(bone_list) == 1:
                        bone = bone_list[0]
                        if self.anim_type == "loc":
                            bone.location = vector_delta
                        elif self.anim_type == "rot":
                            bone.rotation_euler = euler_delta
                        else:
                            bone.scale = scale_delta
                else:
                    if self.anim_type == "loc":
                        tgt_obj.delta_location = vector_delta
                    elif self.anim_type == "rot":
                        tgt_obj.delta_rotation_euler = euler_delta
                    else:
                        tgt_obj.delta_scale = scale_delta

        return [cm.midi_data["notes"], cm.midi_data["params"]]
