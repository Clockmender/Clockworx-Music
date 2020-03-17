import bpy



class CM_ND_AudioTimeNode(bpy.types.Node):
    bl_idname = "cm_audio.time_node"
    bl_label = "Time Info"
    bl_icon = "SPEAKER"

    time_num: bpy.props.FloatProperty(name="Time")

    def init(self, context):
        self.outputs.new("cm_socket.float", "Time")

    def draw_buttons(self, context, layout):
        layout.prop(self, "time_num")

    def execute(self):
        self.time_num = (
            bpy.context.scene.frame_current / bpy.context.scene.render.fps
        ) * bpy.context.scene.render.fps_base
        return self.time_num
