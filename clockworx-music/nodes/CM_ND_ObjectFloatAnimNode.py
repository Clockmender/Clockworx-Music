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
    euler_to_quaternion
    )

class CM_ND_ObjectFloatAnimNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.object_float_anim_node"
    bl_label = "Object(s) Float Animate"
    bl_width_default = 150
    """Animate Object(s) from Float Data"""

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
        self.inputs.new("cm_socket.object", "Object(s)")
        self.inputs.new("cm_socket.bone", "Bone(s)")

    def draw_buttons(self, context, layout):
        box = layout.box()
        box.prop(self, "anim_type")
        row = box.row()
        row.prop(self, "factors")
        box = layout.box()
        box.prop(self, "use_bones")

    def execute(self):
        obj_list = None
        bone_list = None
        value = None
        input_1 = connected_node_output(self, 0)
        input_2 = connected_node_output(self, 1)
        if isinstance(input_2, dict):
            if "objects" in input_2.keys():
                obj_list = input_2["objects"]
                if not isinstance(obj_list, list):
                    obj_list = [obj_list]

        bone_in = connected_node_output(self, 2)
        if isinstance(bone_in, dict):
            if "bones" in bone_in.keys():
                bone_list = bone_in["bones"]
            if not isinstance(bone_list, list):
                bone_list = [bone_list]

        if input_1 is not None:
            if isinstance(input_1, dict):
                if "float" in input_1.keys():
                    value = input_1["float"]
            if value is None:
                return

            values = [value, value, value]
            vector_delta, euler_delta, scale_delta = off_set(values, self.factors)
            rotate_quat = euler_to_quaternion(
                euler_delta.x,
                euler_delta.y,
                euler_delta.z
                )

            if self.use_bones and bone_list is not None:
                for bone in bone_list:
                    if self.anim_type == "loc":
                        if self.factors.x != 0:
                            bone.location.x = vector_delta.x
                        if self.factors.y != 0:
                            bone.location.y = vector_delta.y
                        if self.factors.z != 0:
                            bone.location.z = vector_delta.z
                    elif self.anim_type == "rot":
                        if bone.rotation_mode == "QUATERNION":
                            bone.rotation_quaternion = rotate_quat
                        else:
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

            elif not self.use_bones and obj_list is not None:
                for tgt_obj in obj_list:
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
