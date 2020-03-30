import bpy
import aud

from ..cm_functions import (
    connected_node_sound,
)


class CM_ND_AudioReverseNode(bpy.types.Node):
    bl_idname = "cm_audio.reverse_node"
    bl_label = "Reverse"
    bl_icon = "SPEAKER"

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def get_sound(self):
        input = connected_node_sound(self, 0)
        if isinstance(input, dict):
            if "sound" in input.keys():
                sound = input["sound"]
                if isinstance(sound, aud.Sound):
                    sound = sound.reverse()
                    return {"sound": sound}
        return None

    def output(self):
        return self.get_sound()
