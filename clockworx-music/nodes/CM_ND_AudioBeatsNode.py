import bpy
from bpy.types import NodeSocketFloat
from .._base.base_node import CM_ND_BaseNode

class CM_ND_AudioBeatsNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.beats_node"
    bl_label = "Beats Info"
    bl_icon = "SPEAKER"

    beats_num: bpy.props.FloatProperty(name="Beats")

    def init(self, context):
        self.outputs.new("NodeSocketFloat", "Beats")

    def execute(self):
        cm = bpy.context.scene.cm_pg
        bps = cm.bpm / 60
        fps = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base
        frame = bpy.context.scene.frame_current
        self.beats_num = round((((frame - cm.offset) / fps) * bps), 3)
        return {"float": self.beats_num}

    def output(self):
        return self.execute()
