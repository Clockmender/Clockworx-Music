import bpy
import aud
from .._base.base_node import CM_ND_BaseNode
from ..cm_functions import connected_node_sound


class CM_ND_AudioPlayerNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.player_node"
    bl_label = "Speaker: Automatic"
    bl_icon = "SPEAKER"
    bl_width_default = 180

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.label(text="Plays on Frame Change", icon="INFO")
        layout.label(text="Click Start Exec...")

    def execute(self):
        input = connected_node_sound(self, 0)
        if isinstance(input, dict):
            if "sound" in input.keys():
                sound = input["sound"]
            else:
                sound = None
        else:
            return None
        if isinstance(sound, aud.Sound):
            aud.Device().play(sound)
