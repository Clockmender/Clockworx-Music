import bpy
import aud

from ..cm_functions import (
    connected_node_sound,
)


class CM_ND_AudioModulateNode(bpy.types.Node):
    bl_idname = "cm_audio.modulate_node"
    bl_label = "Modulate"
    bl_icon = "SPEAKER"

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio 1")
        self.inputs.new("cm_socket.sound", "Audio 2")
        self.outputs.new("cm_socket.sound", "Audio")

    def get_sound(self):
        sound1 = connected_node_sound(self, 0)
        sound2 = connected_node_sound(self, 1)
        if sound1 == None or sound2 == None:
            return None
        return sound1.modulate(sound2)
