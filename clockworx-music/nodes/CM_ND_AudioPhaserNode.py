import bpy
import aud
from .._base.base_node import CM_ND_BaseNode

from math import pi, sin
from secrets import randbelow
from bpy.props import (
   IntProperty,
   FloatProperty
   )
from bpy.types import NodeSocketFloat
from ..cm_functions import (
    connected_node_sound,
    connected_node_output,
    get_socket_values,
    mix_dry_wet,
)

class CM_ND_AudioPhaserNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.phaser_node"
    bl_label = "Phaser"
    bl_icon = "SPEAKER"

    max_offset : FloatProperty(name="Max Offset (ms)", default=1, min=0.1, max=20, step=10)
    resolution : IntProperty(name="Resolution", default=30, min=10, max=50)
    phase_length : FloatProperty(name="Phase Length (s)", default=1, min=0.2, max=10, step=10)

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.sound", "Audio")
        self.inputs.new("NodeSocketFloat", "Dry Volume")
        self.inputs.new("NodeSocketFloat", "Wet Volume")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "max_offset")
        layout.prop(self, "phase_length")
        layout.prop(self, "resolution")

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
                    max_offset = self.max_offset / 1000
                    cm = bpy.context.scene.cm_pg
                    sound_w = sound_d.resample(cm.samples, False)
                    slice_t = sound_d.length / cm.samples
                    ref_t   = slice_t / self.resolution
                    seq = aud.Sequence()
                    for i in range(self.resolution):
                        slice = sound_w.limit(ref_t * i,(ref_t * i) + ref_t)
                        rand = randbelow(5)
                        shift = (sin(((i * pi) /  self.phase_length)) * self.max_offset) + (rand / 2000)
                        entry = seq.add(slice, (ref_t * i) + shift, (ref_t * i) + ref_t + shift, 0)
                    seq = seq.resample(cm.samples, False)
                    sound_w = sound_w.mix(seq).limit(0, sound_w.length / cm.samples)
                    sound = mix_dry_wet(sound_d, sound_w, dry_vol, wet_vol)
                    return {"sound": sound}
        return None

    def output(self):
        return self.get_sound()
