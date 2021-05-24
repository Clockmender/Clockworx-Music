import bpy
import aud
from .._base.base_node import CM_ND_BaseNode
from bpy.props import FloatProperty
from bpy.types import NodeSocketFloat
from ..cm_functions import (
    connected_node_sound,
    connected_node_output,
    get_socket_values,
    mix_dry_wet,
)

class CM_ND_AudioReverbNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.reverb_node"
    bl_label = "Reverb"
    bl_icon = "SPEAKER"

    delay_value : FloatProperty(name="Delay (ms)", default=1, min=1, max=50)
    poly_value : FloatProperty(name="Poly Offset (ms)", default=1, min=1, max=50)

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.sound", "Audio")
        self.inputs.new("NodeSocketFloat", "Dry Volume")
        self.inputs.new("NodeSocketFloat", "Wet Volume")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "delay_value")
        layout.prop(self, "poly_value")

    def get_sound(self):
        sockets = self.inputs.keys()
        input_values = get_socket_values(self, sockets, self.inputs)
        if connected_node_output(self, 1) is not None:
            dry_vol = connected_node_output(self, 1)["float"]
        else:
            dry_vol = input_values[1]

        if connected_node_output(self, 2) is not None:
            wet_vol = connected_node_output(self, 2)["float"]
        else:
            wet_vol = input_values[2]

        input = connected_node_sound(self, 0)
        if isinstance(input, dict):
            if "sound" in input.keys():
                sound_d = input["sound"]
                if isinstance(sound_d, aud.Sound):
                    delay = self.delay_value / 1000
                    poly = self.poly_value / 1000
                    snd1 = sound_d.delay(delay)
                    snd = sound_d.mix(snd1)
                    # Add polys
                    sndl = snd.limit(poly,sound_d.length)
                    sndh = snd.limit(-poly,sound_d.length)
                    sound_w = snd.mix(sndl)
                    sound_w = sound_w.mix(sndh)
                    sound = mix_dry_wet(sound_d, sound_w, dry_vol, wet_vol)
                    return {"sound": sound}
        return None

    def output(self):
        return self.get_sound()
