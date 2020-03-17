import bpy


class CM_ND_AudioIntNode(bpy.types.Node):
    bl_idname = "cm_audio.int_node"
    bl_label = "Integer"
    bl_icon = "SPEAKER"

    int_num: bpy.props.IntProperty(name="Integer", default=0)

    def init(self, context):
        self.outputs.new("cm_socket.int", "Integer")

    def draw_buttons(self, context, layout):
        layout.prop(self, "int_num", text="")

    def get_sound(self):
        return self.int_num
