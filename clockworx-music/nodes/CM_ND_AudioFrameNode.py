import bpy


class CM_ND_AudioFrameNode(bpy.types.Node):
    bl_idname = "cm_audio.frame_node"
    bl_label = "Frame Info"
    bl_icon = "SPEAKER"

    frame_num: bpy.props.IntProperty(name="Frame")

    def init(self, context):
        self.outputs.new("cm_socket.int", "Frame")

    def draw_buttons(self, context, layout):
        layout.prop(self, "frame_num")

    def execute(self):
        self.frame_num = bpy.context.scene.frame_current
        return self.frame_num