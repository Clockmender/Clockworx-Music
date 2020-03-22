import bpy
import aud
from ..cm_functions import connected_node_sound


class CM_ND_AudioPlayerNode(bpy.types.Node):
    bl_idname = "cm_audio.player_node"
    bl_label = "Frame Change Player"
    bl_icon = "SPEAKER"
    bl_width_default = 180

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.label(text="Plays on Frame Change", icon="INFO")

    def execute(self):
        sound = connected_node_sound(self, 0)
        if isinstance(sound, aud.Sound):
            aud.Device().play(sound)
