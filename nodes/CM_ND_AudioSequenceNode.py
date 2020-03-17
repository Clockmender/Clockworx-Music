import bpy
import aud

from ..cm_functions import (
    connected_node_sound,
)


class CM_ND_AudioSequenceNode(bpy.types.Node):
    bl_idname = "cm_audio.sequence_node"
    bl_label = "8-Way Sequencer"
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
        for i in range(8):
            snd = connected_node_sound(self, i)
            if snd is not None:
                if first:
                    sound_list = snd
                    first = False
                else:
                    sound_list = sound_list.join(snd)
        return sound_list
