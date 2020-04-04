import bpy
from bpy.props import (
    BoolProperty,
    StringProperty,
    EnumProperty,
    FloatVectorProperty,
    )
from ..cm_functions import (
    connected_node_midi,
    connected_node_output,
    off_set,
    )

class CM_ND_FloatAnimNode(bpy.types.Node):
    bl_idname = "cm_audio_float_anim_node"
    bl_label = "Float Object Animate"
    bl_width_default = 150
    """Animate One Object from Float Data"""

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

    def init(self, context):
        self.inputs.new("cm_socket.midi", "[Key, Control] Data")
        self.inputs.new("cm_socket.object", "Object")
        self.inputs.new("cm_socket.bone", "Bone")

    def draw_buttons(self, context, layout):
        box = layout.box()
        box.prop(self, "anim_type")
        box.prop(self, "midi_type")
        row = box.row()
        row.prop(self, "factors")
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
            if self.midi_type == "con":
                num = 1
            else:
                num = 0
            values = []
            values.append(buffer_in[num] * self.factors.x)
            values.append(buffer_in[num] * self.factors.y)
            values.append(buffer_in[num] * self.factors.z)
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

        return None


    def output(self):
        output = self.get_midi()
        return {"MIDI Handler": output}
