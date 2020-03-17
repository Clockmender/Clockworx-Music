import bpy
from ..cm_functions import connected_node_sound


class CM_ND_AudioOutputNode(bpy.types.Node):
    bl_idname = "cm_audio.output_node"
    bl_label = "Speaker"
    bl_icon = "SPEAKER"

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")

    def get_sound(self):
        sound = connected_node_sound(self, 0)
        return sound

    def draw_buttons(self, context, layout):
        layout.context_pointer_set("audionode", self)
        layout.operator("cm_audio.play_audio")
        layout.operator("cm_audio.stop_audio")
