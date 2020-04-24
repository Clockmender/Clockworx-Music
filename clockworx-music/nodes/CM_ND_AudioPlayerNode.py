import bpy
import aud
from bpy.types import NodeSocketBool
from .._base.base_node import CM_ND_BaseNode
from ..cm_functions import (
    connected_node_sound,
    get_socket_values,
    connected_node_output,
)


class CM_ND_AudioPlayerNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.player_node"
    bl_label = "Speaker: Automatic"
    bl_icon = "SPEAKER"

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.sound", "Audio")
        self.inputs.new("NodeSocketBool", "Play")

    def execute(self):
        input = connected_node_sound(self, 0)
        if isinstance(input, dict):
            if "sound" in input.keys():
                sound = input["sound"]
            else:
                sound = None
        else:
            return None

        play_sound = connected_node_output(self, 1)
        if isinstance(play_sound, dict):
            if "bool" in play_sound.keys():
                play_sound = play_sound["bool"]
            else:
                play_sound = get_socket_values(self, sockets, self.inputs)[1]

        if isinstance(sound, aud.Sound) and play_sound:
            aud.Device().play(sound)
