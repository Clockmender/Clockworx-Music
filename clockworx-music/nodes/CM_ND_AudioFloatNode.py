import bpy


class CM_ND_AudioFloatNode(bpy.types.Node):
    bl_idname = "cm_audio.float_node"
    bl_label = "Float"
    bl_icon = "SPEAKER"

    float_num: bpy.props.FloatProperty(name="Float", default=0.0)

    def init(self, context):
        self.outputs.new("cm_socket.float", "Float")

    def draw_buttons(self, context, layout):
        layout.prop(self, "float_num", text="")

    def get_sound(self):
        return self.float_num
