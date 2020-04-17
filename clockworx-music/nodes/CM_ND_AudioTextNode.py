import bpy
from bpy.types import NodeSocketString
from .._base.base_node import CM_ND_BaseNode

class CM_ND_AudioTextNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.text_node"
    bl_label = "Text"
    bl_icon = "SPEAKER"

    text_input: bpy.props.StringProperty(name="Text", default="")

    def init(self, context):
        self.outputs.new("NodeSocketString", "Text")

    def draw_buttons(self, context, layout):
        layout.prop(self, "text_input", text="")

    def output(self):
        return {"text": self.text_input}
