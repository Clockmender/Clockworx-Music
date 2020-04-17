import bpy
from bpy.types import NodeSocketFloat
from .._base.base_node import CM_ND_BaseNode

class CM_ND_AudioFloatNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.float_node"
    bl_label = "Float"
    bl_icon = "SPEAKER"

    float_num: bpy.props.FloatProperty(name="Float", default=0.0)

    def init(self, context):
        self.outputs.new("NodeSocketFloat", "Float")

    def draw_buttons(self, context, layout):
        layout.prop(self, "float_num", text="")

    def output(self):
        return {"float": self.float_num}
