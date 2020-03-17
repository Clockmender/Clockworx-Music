import bpy

class CM_ND_AudioBoolNode(bpy.types.Node):
    bl_idname = "cm_audio.bool_node"
    bl_label = "Boolean"
    bl_icon = "SPEAKER"

    bool_input: bpy.props.BoolProperty(name="Boolean", default=False)

    def init(self, context):
        self.outputs.new("cm_socket.bool", "Boolean")

    def draw_buttons(self, context, layout):
        layout.prop(self, "bool_input", text="")

    def get_sound(self):
        return self.bool_input
