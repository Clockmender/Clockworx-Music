import bpy
from bpy.types import NodeSocketBool
from .._base.base_node import CM_ND_BaseNode

class CM_ND_AudioBoolNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.bool_node"
    bl_label = "Boolean"
    bl_icon = "SPEAKER"

    bool_input: bpy.props.BoolProperty(name="Boolean", default=False)

    def init(self, context):
        self.outputs.new("NodeSocketBool", "Boolean")

    def draw_buttons(self, context, layout):
        layout.prop(self, "bool_input", text="")

    def output(self):
        return {"bool": self.bool_input}
