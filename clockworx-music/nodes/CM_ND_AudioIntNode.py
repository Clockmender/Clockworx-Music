import bpy
from bpy.types import NodeSocketInt
from .._base.base_node import CM_ND_BaseNode

class CM_ND_AudioIntNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.int_node"
    bl_label = "Integer"
    bl_icon = "SPEAKER"

    int_num: bpy.props.IntProperty(name="Integer", default=0)

    def init(self, context):
        self.outputs.new("NodeSocketInt", "Integer")

    def draw_buttons(self, context, layout):
        layout.prop(self, "int_num", text="")

    def output(self):
        return {"int": self.int_num}
