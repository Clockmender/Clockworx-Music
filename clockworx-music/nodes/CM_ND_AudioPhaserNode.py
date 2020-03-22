import bpy
import aud
from math import pi, sin
from secrets import randbelow
from bpy.props import (
   IntProperty,
   FloatProperty
   )
from ..cm_functions import connected_node_sound

class CM_ND_AudioPhaserNode(bpy.types.Node):
    bl_idname = "cm_audio.phaser_node"
    bl_label = "Phaser"
    bl_icon = "SPEAKER"

    max_offset : FloatProperty(name="Max Offset (ms)", default=1, min=0.1, max=20, step=10)
    resolution : IntProperty(name="Resolution", default=30, min=10, max=50)
    phase_length : FloatProperty(name="Phase Length (s)", default=1, min=0.2, max=10, step=10)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "max_offset")
        layout.prop(self, "phase_length")
        layout.prop(self, "resolution")

    def get_sound(self):
        sound = connected_node_sound(self, 0)
        if sound == None:
            return None
        max_offset = self.max_offset / 1000
        cm = bpy.context.scene.cm_pg
        sound = sound.resample(cm.samples, False)
        slice_t = sound.length / cm.samples
        ref_t   = slice_t / self.resolution
        seq = aud.Sequence()
        for i in range(self.resolution):
            slice = sound.limit(ref_t * i,(ref_t * i) + ref_t)
            rand = randbelow(5)
            shift = (sin(((i * pi) /  self.phase_length)) * self.max_offset) + (rand / 2000)
            entry = seq.add(slice, (ref_t * i) + shift, (ref_t * i) + ref_t + shift, 0)
        seq = seq.resample(cm.samples, False)
        sound = sound.mix(seq).limit(0, sound.length / cm.samples)
        return sound
