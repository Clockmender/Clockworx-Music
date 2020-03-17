import bpy
from ..cm_functions import connected_node_info


class CM_ND_AudioDebugNode(bpy.types.Node):
    bl_idname = "cm_audio.debug_node"
    bl_label = "Debug"
    bl_icon = "SPEAKER"

    text_input: bpy.props.StringProperty(name="Value", default="")

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Input")

    def draw_buttons(self, context, layout):
        layout.prop(self, "text_input")
        layout.context_pointer_set("audionode", self)
        layout.operator("cm_audio.display_audio")

    def info(self, context):
        input = connected_node_info(self, 0)
        self.text_input = str(input)
