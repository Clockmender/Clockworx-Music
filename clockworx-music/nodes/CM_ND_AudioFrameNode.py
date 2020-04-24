import bpy
from bpy.types import NodeSocketFloat
from .._base.base_node import CM_ND_BaseNode
from bpy.props import BoolProperty

class CM_ND_AudioFrameNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.frame_node"
    bl_label = "Frame No"
    bl_icon = "SPEAKER"

    def init(self, context):
        self.outputs.new("NodeSocketFloat", "Frame")

    def execute(self):
        return {"float": float(bpy.context.scene.frame_current)}

    def output(self):
        return self.execute()
