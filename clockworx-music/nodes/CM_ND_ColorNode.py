import bpy
from bpy.types import NodeSocketColor
from .._base.base_node import CM_ND_BaseNode
from bpy.props import FloatVectorProperty

class CM_ND_ColorNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.colour_node"
    bl_label = "Colour"
    bl_icon = "SPEAKER"

    colour : FloatVectorProperty(
        default = [0.5, 0.5, 0.5, 1.0], size=4, subtype = "COLOR",
        soft_min = 0.0, soft_max = 1.0)

    def init(self, context):
        super().init(context)
        self.outputs.new("NodeSocketColor", "Colour")

    def draw_buttons(self, context, layout):
        layout.prop(self, "colour", text="")

    def output(self):
        return {"colour": self.colour}

# node_tree.nodes["Principled BSDF"].inputs[0].default_value
