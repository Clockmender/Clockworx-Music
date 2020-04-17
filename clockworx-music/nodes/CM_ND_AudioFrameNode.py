import bpy
from bpy.types import NodeSocketInt
from .._base.base_node import CM_ND_BaseNode

class CM_ND_AudioFrameNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.frame_node"
    bl_label = "Frame No"
    bl_icon = "SPEAKER"

    frame_num: bpy.props.IntProperty(name="Frame")

    def init(self, context):
        self.outputs.new("NodeSocketInt", "Frame")

    def execute(self):
        self.frame_num = bpy.context.scene.frame_current
        return {"int": self.frame_num}

    def output(self):
        return self.execute()
