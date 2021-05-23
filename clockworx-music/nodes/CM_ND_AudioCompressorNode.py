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

class CM_ND_AudioCompressorNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.compressor_node"
    bl_label = "Comressor"
    bl_icon = "SPEAKER"

    low1   : FloatProperty(name="Low Frequency",min=15,max=20000)
    qlfac1 : FloatProperty(name="L-QFactor",min=0,max=1)

    low2   : FloatProperty(name="Low Frequency",min=15,max=20000)
    qlfac2 : FloatProperty(name="L-QFactor",min=0,max=1)
    high1  : FloatProperty(name="High Frequency",min=15,max=20000)
    qhfac1 : FloatProperty(name="H-QFactor",min=0,max=1)

    low3   : FloatProperty(name="Low Frequency",min=15,max=20000)
    qlfac3 : FloatProperty(name="L-QFactor",min=0,max=1)
    high2  : FloatProperty(name="High Frequency",min=15,max=20000)
    qhfac2 : FloatProperty(name="H-QFactor",min=0,max=1)

    high3  : FloatProperty(name="High Frequency",min=15,max=20000)
    qhfac3 : FloatProperty(name="H-QFactor",min=0,max=1)

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.sound", "Audio")
        self.inputs.new("NodeSocketFloat", "Dry Volume")
        self.inputs.new("NodeSocketFloat", "Wet Volume")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.label(text="First LowPass",icon="NONE")
        layout.prop(self,"low1")
        layout.prop(self,"qlfac1")
        layout.label(text="First BandPass",icon="NONE")
        layout.prop(self,"low2")
        layout.prop(self,"qlfac2")
        layout.prop(self,"high1")
        layout.prop(self,"qhfac1")
        layout.label(text="Second BandPass",icon="NONE")
        layout.prop(self,"low3")
        layout.prop(self,"qlfac3")
        layout.prop(self,"high2")
        layout.prop(self,"qhfac2")
        layout.label(text="Final HighPass",icon="NONE")
        layout.prop(self,"high3")
        layout.prop(self,"qhfac3")

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
                    if (
                        all([self.qlfac1 > 0, self.qlfac2 > 0, self.qlfac3 > 0,
                        self.qhfac1 > 0,self.qhfac2 > 0, self.qhfac2 > 0])
                        ):
                        # first LowPass
                        sound_w = sound_d.lowpass(self.low1, self.qlfac1)
                        # first BandPass
                        sound_w = sound_w.lowpass(self.low2, self.qlfac2)
                        sound_w = sound_w.highpass(self.high1, self.qhfac1)
                        # second BandPass
                        sound_w = sound_w.lowpass(self.low3, self.qlfac3)
                        sound_w = sound_w.highpass(self.high2, self.qhfac2)
                        # final HighPass
                        sound_w = sound_w.highpass(self.high3, self.qhfac3)
                        sound = mix_dry_wet(sound_d, sound_w, dry_vol, wet_vol)
                        return {"sound": sound}
        return None

    def output(self):
        return self.get_sound()
