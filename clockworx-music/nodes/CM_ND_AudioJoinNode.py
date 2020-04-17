import bpy
import aud
from .._base.base_node import CM_ND_BaseNode

from ..cm_functions import (
    connected_node_sound,
)


class CM_ND_AudioJoinNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.join_node"
    bl_label = "Join"
    bl_icon = "SPEAKER"

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.sound", "Audio 1")
        self.inputs.new("cm_socket.sound", "Audio 2")
        self.outputs.new("cm_socket.sound", "Audio")

    def get_sound(self):
        input1 = connected_node_sound(self, 0)
        input2 = connected_node_sound(self, 1)
        if isinstance(input1, dict) and isinstance(input2, dict):
            if "sound" in input1.keys():
                sound1 = input1["sound"]
            if "sound" in input2.keys():
                sound2 = input2["sound"]
            if isinstance(sound1, aud.Sound) and isinstance(sound2, aud.Sound):
                sound = sound1.join(sound2)
                return {"sound": sound}
        return None

    def output(self):
        return self.get_sound()
