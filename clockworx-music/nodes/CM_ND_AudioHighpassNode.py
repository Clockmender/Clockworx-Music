import bpy
import aud
from .._base.base_node import CM_ND_BaseNode

from ..cm_functions import (
    connected_node_sound,
)

class CM_ND_AudioHighpassNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.highpass_node"
    bl_label = "Highpass"
    bl_icon = "SPEAKER"

    frequency_prop : bpy.props.FloatProperty(name="Frequency",
        default=440, soft_min=20, soft_max=20000)
    q_prop : bpy.props.FloatProperty(name="Q Factor", default=0.5, soft_min=0, soft_max=1)

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "frequency_prop")
        layout.prop(self, "q_prop")

    def get_sound(self):
        input = connected_node_sound(self, 0)
        if isinstance(input, dict):
            if "sound" in input.keys():
                sound = input["sound"]
                if isinstance(sound, aud.Sound):
                    sound = sound.highpass(self.frequency_prop, self.q_prop)
                    return {"sound": sound}
        return None

    def output(self):
        return self.get_sound()
