import bpy
from .._base.base_node import CM_ND_BaseNode
from bpy.types import NodeSocketFloat

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

class CM_ND_ObjectFloatAnimNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.object_float_anim_node"
    bl_label = "Object Float Animate"
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
    use_bones : BoolProperty(name="Use Bones", default=False)

    def init(self, context):
        super().init(context)
        self.inputs.new("NodeSocketFloat", "Input (Float)")
        self.inputs.new("cm_socket.object", "Object")
        self.inputs.new("cm_socket.bone", "Bone")

    def draw_buttons(self, context, layout):
        box = layout.box()
        box.prop(self, "anim_type")
        row = box.row()
        row.prop(self, "factors")
        box = layout.box()
        box.prop(self, "use_bones")

    def execute(self):
        tgt_obj = None
        bone = None
        input_1 = connected_node_output(self, 0)
        input_2 = connected_node_output(self, 1)
        if isinstance(input_2, dict):
            if "objects" in input_2.keys():
                objects = input_2["objects"]
                if not isinstance(objects, list):
                    objects = [objects]
                if len(objects) == 1:
                    tgt_obj = objects[0]

        bone_in = connected_node_output(self, 2)
        if isinstance(bone_in, dict):
            if "bones" in bone_in.keys():
                bone = bone_in["bones"]

        if input_1 is not None:
            value = input_1["float"]
            values = [value, value, value]
            vector_delta, euler_delta, scale_delta = off_set(values, self.factors)

            if self.use_bones and bone is not None:
                if self.anim_type == "loc":
                    if self.factors.x != 0:
                        bone.location.x = vector_delta.x
                    if self.factors.y != 0:
                        bone.location.y = vector_delta.y
                    if self.factors.z != 0:
                        bone.location.z = vector_delta.z
                elif self.anim_type == "rot":
                    if self.factors.x != 0:
                        bone.rotation_euler.x = euler_delta.x
                    if self.factors.y != 0:
                        bone.rotation_euler.y = euler_delta.y
                    if self.factors.z != 0:
                        bone.rotation_euler.z = euler_delta.z
                else:
                    if self.factors.x != 0:
                        bone.scale.x = scale_delta.x
                    if self.factors.y != 0:
                        bone.scale.y = scale_delta.y
                    if self.factors.z != 0:
                        bone.scale.z = scale_delta.z
                        
            elif not self.use_bones and tgt_obj is not None:
                if self.anim_type == "loc":
                    if self.factors.x != 0:
                        tgt_obj.delta_location.x = vector_delta.x
                    if self.factors.y != 0:
                        tgt_obj.delta_location.y = vector_delta.y
                    if self.factors.z != 0:
                        tgt_obj.delta_location.z = vector_delta.z
                elif self.anim_type == "rot":
                    if self.factors.x != 0:
                        tgt_obj.delta_rotation_euler.x = euler_delta.x
                    if self.factors.y != 0:
                        tgt_obj.delta_rotation_euler.y = euler_delta.y
                    if self.factors.z != 0:
                        tgt_obj.delta_rotation_euler.z = euler_delta.z
                else:
                    if self.factors.x != 0:
                        tgt_obj.delta_scale.x = scale_delta.x
                    if self.factors.y != 0:
                        tgt_obj.delta_scale.y = scale_delta.y
                    if self.factors.z != 0:
                        tgt_obj.delta_scale.z = scale_delta.z
