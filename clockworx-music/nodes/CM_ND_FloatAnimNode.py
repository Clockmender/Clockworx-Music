import bpy
from bpy.props import (
    BoolProperty,
    StringProperty,
    EnumProperty,
    FloatVectorProperty,
    )
from ..cm_functions import (
    connected_node_midi,
    off_set,
    )

class CM_ND_FloatAnimNode(bpy.types.Node):
    bl_idname = "cm_audio_float_anim_node"
    bl_label = "Float Object Animate"
    bl_width_default = 150
    """Animate One Object from Float Data"""

    object_name : StringProperty(name="Object", default="")
    factors : FloatVectorProperty(name="", subtype="XYZ", default=(1,1,1))
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
        box.prop(self, "factors")
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
                values = []
                values.append(buffer_in[num] * self.factors.x)
                values.append(buffer_in[num] * self.factors.y)
                values.append(buffer_in[num] * self.factors.z)
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

        return [cm.midi_data["notes_cu"], cm.midi_data["params_cu"]]
