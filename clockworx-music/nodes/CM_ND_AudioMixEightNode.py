import bpy
import aud

from ..cm_functions import (
    connected_node_sound,
)


class CM_ND_AudioMixEightNode(bpy.types.Node):
    bl_idname = "cm_audio.mix_eight_node"
    bl_label = "8 Channel Mixer"
    bl_icon = "SPEAKER"

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio 1")
        self.inputs.new("cm_socket.sound", "Audio 2")
        self.inputs.new("cm_socket.sound", "Audio 3")
        self.inputs.new("cm_socket.sound", "Audio 4")
        self.inputs.new("cm_socket.sound", "Audio 5")
        self.inputs.new("cm_socket.sound", "Audio 6")
        self.inputs.new("cm_socket.sound", "Audio 7")
        self.inputs.new("cm_socket.sound", "Audio 8")
        self.outputs.new("cm_socket.sound", "Audio")

    def get_sound(self):
        first = True
        sound_list = None
        sound = None
        for i in range(8):
            input = connected_node_sound(self, i)
            if isinstance(input, dict):
                if "sound" in input.keys():
                    sound = input["sound"]
                    if isinstance(sound, aud.Sound):
                        if first:
                            sound_list = sound
                            first = False
                        else:
                            sound_list = sound_list.mix(sound)
        return {"sound": sound_list}

    def output(self):
        return self.get_sound()
