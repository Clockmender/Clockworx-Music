import bpy
import aud

from ..cm_functions import (
    connected_node_sound,
)


class CM_ND_AudioLowpassNode(bpy.types.Node):
    bl_idname = "cm_audio.lowpass_node"
    bl_label = "Lowpass"
    bl_icon = "SPEAKER"

    frequency_prop : bpy.props.FloatProperty(name="Frequency",
        default=440, soft_min=20, soft_max=20000)
    q_prop : bpy.props.FloatProperty(name="Q Factor", default=0.5, soft_min=0, soft_max=1)

    def init(self, context):
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
                    return {"sound": sound.lowpass(self.frequency_prop, self.q_prop)}
        return None

    def output(self):
        return self.get_sound()
