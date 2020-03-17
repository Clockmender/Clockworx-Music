import bpy

class CM_ND_AudioTextNode(bpy.types.Node):
    bl_idname = "cm_audio.text_node"
    bl_label = "Text"
    bl_icon = "SPEAKER"

    text_input: bpy.props.StringProperty(name="Text", default="")

    def init(self, context):
        self.outputs.new("cm_socket.text", "Text")

    def draw_buttons(self, context, layout):
        layout.prop(self, "text_input", text="")

    def get_sound(self):
        return self.text_input
