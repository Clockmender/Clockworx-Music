import bpy
import aud
from .._base.base_node import CM_ND_BaseNode

from bpy.props import EnumProperty
from ..cm_functions import (
    connected_node_sound,
)

class CM_ND_AudioSeparatorNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.separator_node"
    bl_label = "Separator (for Equaliser)"
    bl_icon = "SPEAKER"
    bl_width_default = 180

    sound_sel : EnumProperty(
        items=(
            ("sound", "All Sounds", "Combined Sound"),
            ("snd1", "Sound 1", "Sound 1"),
            ("snd2", "Sound 2", "Sound 2"),
            ("snd3", "Sound 3", "Sound 3"),
            ("snd4", "Sound 4", "Sound 4"),
            ("snd5", "Sound 5", "Sound 5"),
            ("snd6", "Sound 6", "Sound 6"),
            ("snd7", "Sound 7", "Sound 7"),
            ("snd8", "Sound 8", "Sound 8"),
        ),
        name="Sound",
        default="snd1",
        description="Sound from Collection",
    )

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.sound", "Audio Collection")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "sound_sel")

    def get_sound(self):
        sound_dict = connected_node_sound(self, 0)
        if isinstance(sound_dict, dict):
            if len(sound_dict) == 9:
                sound = sound_dict[self.sound_sel]
                if isinstance(sound, aud.Sound):
                    return {"sound": sound}
        return None

    def output(self):
        return self.get_sound()
