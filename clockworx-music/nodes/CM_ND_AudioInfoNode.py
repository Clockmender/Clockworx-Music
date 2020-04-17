import bpy
from .._base.base_node import CM_ND_BaseNode

class CM_ND_AudioInfoNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.info_node"
    bl_label = "Project Info"
    bl_icon = "SPEAKER"

    def init(self, context):
        self.outputs.new("cm_socket.generic", "Project Info")

    def execute(self):
        cm = bpy.context.scene.cm_pg
        bps = cm.bpm / 60
        fps = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base
        frame = bpy.context.scene.frame_current
        output = {}
        output["frame_no"] = bpy.context.scene.frame_current
        output["time_num"] = (
            bpy.context.scene.frame_current / bpy.context.scene.render.fps
            ) * bpy.context.scene.render.fps_base
        output["beats_num"] = round((((frame - cm.offset) / fps) * bps), 3)
        return output

    def output(self):
        return self.execute()
