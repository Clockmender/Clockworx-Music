import bpy



class CM_ND_AudioTimeNode(bpy.types.Node):
    bl_idname = "cm_audio.time_node"
    bl_label = "Time Info"
    bl_icon = "SPEAKER"

    def init(self, context):
        self.outputs.new("cm_socket.generic", "Time")

    def execute(self):
        return {"out1":(
            bpy.context.scene.frame_current / bpy.context.scene.render.fps
        ) * bpy.context.scene.render.fps_base}

    def output(self):
        return self.execute()
