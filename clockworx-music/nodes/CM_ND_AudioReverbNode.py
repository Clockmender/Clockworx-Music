import bpy
import aud
from bpy.props import FloatProperty
from ..cm_functions import (
    connected_node_sound,
)

class CM_ND_AudioReverbNode(bpy.types.Node):
    bl_idname = "cm_audio.reverb_node"
    bl_label = "Reverb"
    bl_icon = "SPEAKER"

    delay_value : FloatProperty(name="Delay (ms)", default=1, min=1, max=50)
    poly_value : FloatProperty(name="Poly Offset (ms)", default=1, min=1, max=50)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "delay_value")
        layout.prop(self, "poly_value")

    def get_sound(self):
        input = connected_node_sound(self, 0)
        if isinstance(input, dict):
            if "sound" in input.keys():
                sound = input["sound"]
                if isinstance(sound, aud.Sound):
                    delay = self.delay_value / 1000
                    poly = self.poly_value / 1000
                    snd1 = sound.delay(delay)
                    snd = sound.mix(snd1)
                    # Add polys
                    sndl = sound.limit(poly,sound.length)
                    sndh = sound.limit(-poly,sound.length)
                    sound = sound.mix(sndl)
                    sound = sound.mix(sndh)
                    return {"sound": sound}
        return None

    def output(self):
        return self.get_sound()
