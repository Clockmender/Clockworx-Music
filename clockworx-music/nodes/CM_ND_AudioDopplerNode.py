import bpy
import aud
from .._base.base_node import CM_ND_BaseNode
from math import pi, cos
from secrets import randbelow
from bpy.props import (
   IntProperty,
   FloatProperty,
   BoolProperty,
   )
from ..cm_functions import connected_node_sound

class CM_ND_AudioDopplerNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.doppler_node"
    bl_label = "Doppler"
    bl_icon = "SPEAKER"
    bl_width_default = 180

    max_offset : FloatProperty(name="Max Pitch Shift", default=1, min=-1, max=1, step=2)
    resolution : IntProperty(name="Resolution", default=30, min=10, max=50)
    orig_vol : FloatProperty(name="Original Volume", default=1, min=0.0, max=1, step=2)
    pre_num : IntProperty(name="Pre Sound Number", default=0, min=0)
    post_num : IntProperty(name="Post Sound Number", default=0, min=0)

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "max_offset")
        layout.prop(self, "orig_vol")
        layout.prop(self, "resolution")
        layout.prop(self, "pre_num")
        layout.prop(self, "post_num")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        input = connected_node_sound(self, 0)
        if isinstance(input, dict):
            if "sound" in input.keys():
                sound = input["sound"]
                if isinstance(sound, aud.Sound):
                    sound = sound.resample(cm.samples, False)
                    slice_t = sound.length / cm.samples
                    ref_t = slice_t / self.resolution
                    for i in range(self.resolution):
                        start_t = ref_t * i
                        end_t = (ref_t * i) + ref_t
                        slice = sound.limit(start_t, end_t)
                        pitch_value = 1 + (cos(i * ( pi / self.resolution)) * self.max_offset)
                        sndS = slice.pitch(pitch_value).resample(cm.samples, False)
                        if i == 0:
                            sound_d = sndS
                        else:
                            sound_d = sound_d.join(sndS)

                    if self.pre_num > 0:
                        sound_pre = sound.pitch(1 + self.max_offset).resample(cm.samples, False)
                        for i in range(1, self.pre_num):
                            sound_pre = sound_pre.join(sound_pre)
                    else:
                        sound_pre = None

                    if self.post_num > 0:
                        sound_post = sound.pitch(1 - self.max_offset).resample(cm.samples, False)
                        for i in range(1, self.post_num):
                            sound_post = sound_post.join(sound_post)
                    else:
                        sound_post = None

                    if sound_pre is not None:
                        sound_out = sound_pre.join(sound_d)
                    else:
                        sound_out = sound_d

                    if sound_post is not None:
                        sound_out = sound_out.join(sound_post)

                    if sound_out.specs[1] != cm.sound_channels:
                        sound_out = sound_out.rechannel(cm.sound_channels)

                    if self.orig_vol > 0:
                        sound = sound.volume(self.orig_vol)
                        sound_out = sound_out.mix(sound)
                    return {"sound": sound_out}
        return None

    def output(self):
        return self.get_sound()
