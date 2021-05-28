import bpy
from .._base.base_node import CM_ND_BaseNode

from bpy.props import (
   BoolProperty,
   FloatProperty,
   StringProperty,
   EnumProperty,
)
from ..cm_functions import connected_node_output

class CM_ND_BoneDataNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.bone_data_node"
    bl_label = "Bone Data"
    bl_icon = "SPEAKER"

    anim_type: EnumProperty(
        items=(
        ("loc", "Location", "Source: Location"),
          ("rot", "Rotation", "Source: Rotation"),
          ("scl", "Scale", "Source: Scale"),
        ),
        name="Source:",
        default="loc",
        description="Animation Type",
        )
    control_axis : EnumProperty(
        items=(
          ("0", "X Axis", "X Axis"),
          ("1", "Y Axis", "Y Axis"),
          ("2", "Z Axis", "Z Axis"),
        ),
        name="Axis",
        default="0",
        description="Contol Axis",
        )

    def draw_buttons(self, context, layout):
        box = layout.box()
        box.prop(self, "anim_type")
        box.prop(self, "control_axis")

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.bone", "Bone")
        self.outputs.new("NodeSocketFloat", "Data (Float)")

    def get_sound(self):
        input_1 = connected_node_output(self, 0)
        if isinstance(input_1, dict):
            if "bones" in input_1.keys():
                bones = input_1["bones"]
                if isinstance(bones, list):
                    bone = bones[0]
                else:
                    bone = input_1["bones"]
        else:
            return None

        if bone is not None:
            if self.anim_type == "loc":
                value_bone = bone.location[int(self.control_axis)]
            elif self.anim_type == "rot":
                value_bone = bone.rotation_euler[int(self.control_axis)]
            else:
                value_bone = bone.scale[int(self.control_axis)]

        return {"float": value_bone}

    def output(self):
        return self.get_sound()
