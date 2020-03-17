import bpy


class CM_ND_AudioInfoNode(bpy.types.Node):
    bl_idname = "cm_audio.info_node"
    bl_label = "Project Info"
    bl_icon = "SPEAKER"

    frame_num: bpy.props.IntProperty(name="Frame")
    time_num: bpy.props.FloatProperty(name="Time")
    beats_num: bpy.props.FloatProperty(name="Beats")

    def draw_buttons(self, context, layout):
        layout.prop(self, "frame_num")
        layout.prop(self, "time_num")
        layout.prop(self, "beats_num")

    def execute(self):
        cm = bpy.context.scene.cm_pg
        bps = cm.bpm / 60
        fps = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base
        frame = bpy.context.scene.frame_current
        self.beats_num = round((((frame - cm.offset) / fps) * bps), 3)
        self.time_num = (
            bpy.context.scene.frame_current / bpy.context.scene.render.fps
        ) * bpy.context.scene.render.fps_base
        self.frame_num = bpy.context.scene.frame_current
