import bpy
import aud

from ..cm_functions import (
    connected_node_sound,
)


class CM_ND_AudioPingPongNode(bpy.types.Node):
    bl_idname = "cm_audio.pingpong_node"
    bl_label = "PingPong"
    bl_icon = "SPEAKER"

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def get_sound(self):
        sound = connected_node_sound(self, 0)
        if sound == None:
            return None
        return sound.pingpong()
