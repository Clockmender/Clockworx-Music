import bpy
from .._base.base_node import CM_ND_BaseNode

from bpy.props import (
   BoolProperty,
   FloatProperty,
   StringProperty,
   EnumProperty,
)
from ..cm_functions import connected_node_output

class CM_ND_ObjectDataNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.object_data_node"
    bl_label = "Object Data"
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
        self.inputs.new("cm_socket.object", "Object")
        self.outputs.new("NodeSocketFloat", "Data (Float)")

    def get_sound(self):
        input_1 = connected_node_output(self, 0)
        if isinstance(input_1, dict):
            if "objects" in input_1.keys():
                con_obj = input_1["objects"]
        else:
            return None

        if con_obj is not None:
            if self.anim_type == "loc":
                value_obj = con_obj.location[int(self.control_axis)]
            elif self.anim_type == "rot":
                value_obj = con_obj.rotation_euler[int(self.control_axis)]
            else:
                value_obj = con_obj.scale[int(self.control_axis)]

        return {"float": value_obj}

    def output(self):
        return self.get_sound()
