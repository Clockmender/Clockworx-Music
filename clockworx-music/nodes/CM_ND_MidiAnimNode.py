import bpy
from .._base.base_node import CM_ND_BaseNode

from bpy.props import (
    IntProperty,
    BoolProperty,
    StringProperty,
    EnumProperty,
    FloatVectorProperty,
    )
from ..cm_functions import (
    connected_node_midi,
    connected_node_output,
    get_socket_values,
    off_set,
    )

class CM_ND_MidiAnimNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio_midi_anim_node"
    bl_label = "MIDI Object Animate"
    bl_width_default = 150
    """Multi-Animate One Object from MIDI Key, or Controls Data"""

    message : StringProperty(name="")
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
    use_bones : BoolProperty(name="Use Bone", default=False)

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.midi", "[Key, Control] Data")
        self.inputs.new("cm_socket.object", "Object")
        self.inputs.new("cm_socket.bone", "Bone")
        self.outputs.new("cm_socket.midi", "[Key, Control] Data")

    def draw_buttons(self, context, layout):
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

    def get_midi(self):
        cm = bpy.context.scene.cm_pg
        tgt_obj = None
        bone = None
        sockets = self.inputs.keys()
        buffer_in = connected_node_midi(self, 0)
        input = connected_node_output(self, 1)
        if isinstance(input, dict):
            if "objects" in input.keys():
                objects = input["objects"]
                if not isinstance(objects, list):
                    objects = [objects]
                if len(objects) == 1:
                    tgt_obj = objects[0]

        bone_in = connected_node_output(self, 2)
        if isinstance(bone_in, dict):
            if "bones" in bone_in.keys():
                bone = bone_in["bones"]

        if buffer_in is not None:
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

            if self.use_bones and bone is not None:
                if self.anim_type == "loc":
                    bone.location = vector_delta
                elif self.anim_type == "rot":
                    bone.rotation_euler = euler_delta
                else:
                    bone.scale = scale_delta
            elif not self.use_bones and tgt_obj is not None:
                if self.anim_type == "loc":
                    tgt_obj.delta_location = vector_delta
                elif self.anim_type == "rot":
                    tgt_obj.delta_rotation_euler = euler_delta
                else:
                    tgt_obj.delta_scale = scale_delta

            return [cm.midi_data["notes"], cm.midi_data["params"]]

        return None


    def output(self):
        output = self.get_midi()
        return {"MIDI Handler": output}
