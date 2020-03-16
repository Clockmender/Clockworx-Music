# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****
#
# -----------------------------------------------------------------------
# Author: Alan Odom (Clockmender) Copyright (c) 2019
# -----------------------------------------------------------------------
#
import aud
import bpy
from bpy.props import (
    IntProperty,
    FloatProperty,
    IntProperty,
    BoolProperty,
    StringProperty,
)
from .cm_sockets import (
    CM_SK_AudioNodeSocket,
)

from .cm_functions import (
    connected_node_sound,
    get_socket_values,
    get_index,
    get_freq,
    osc_generate,
)

class CM_ND_AudioAccumulatorNode(bpy.types.Node):
    bl_idname = "cm_audio.accumulator_node"
    bl_label = "Accumulator"
    bl_icon = "SPEAKER"

    additive_prop : bpy.props.BoolProperty(name="Additive", default=False)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "additive_prop")

    def get_sound(self):
        sound = connected_node_sound(self, 0)
        if sound == None:
            return None
        return sound.accumulate(self.additive_prop)


class CM_ND_AudioDelayNode(bpy.types.Node):
    bl_idname = "cm_audio.delay_node"
    bl_label = "Delay by Time/Beats"
    bl_icon = "SPEAKER"

    time_prop : bpy.props.FloatProperty(name="Delay", default=0, min=0, soft_max=10)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        cm_pg = context.scene.cm_pg
        layout.prop(self, "time_prop")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sound = connected_node_sound(self, 0)
        if sound == None:
            return None
        if cm.type_bool:
            delay = self.time_prop
        else:
            delay = self.time_prop * (60 / cm.bpm)
        return sound.delay(delay)


class CM_ND_AudioEchoNode(bpy.types.Node):
    bl_idname = "cm_audio.echo_node"
    bl_label = "Echo"
    bl_icon = "SPEAKER"

    time_prop : bpy.props.FloatProperty(name="Delay", default=0, min=0, soft_max=10)
    echo_num : IntProperty(name="Echos #", default=4, min=1, max=10)
    factor : FloatProperty(name="Decay Factor", default=0.2, min=0.001, max=0.5)
    volume : FloatProperty(name="Volume", default=1, min=0.1)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "time_prop")
        layout.prop(self, "echo_num")
        layout.prop(self, "factor")
        layout.prop(self, "volume")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sound = connected_node_sound(self, 0)
        if sound == None:
            return None
        volume = self.volume
        sound = sound.volume(volume)
        first = True
        for i in range(self.echo_num):
            if cm.type_bool:
                delay = self.time_prop * (i + 1)
            else:
                delay = (self.time_prop * (i + 1)) * (60 / cm.bpm)
            volume = volume * (1 - self.factor)
            snd = sound.delay(delay).volume(volume)
            if first:
                sound_out = sound.mix(snd)
                first = False
            else:
                sound_out = sound_out.mix(snd)
        return sound_out.volume(self.volume)


class CM_ND_AudioEnvelopeNode(bpy.types.Node):
    bl_idname = "cm_audio.envelope_node"
    bl_label = "Envelope"
    bl_icon = "SPEAKER"

    attack_prop : bpy.props.FloatProperty(name="Attack", default=0.005, min=0, soft_max=2)
    release_prop : bpy.props.FloatProperty(name="Release", default=0.2, min=0, soft_max=5)
    threshold_prop : bpy.props.FloatProperty(name="Threshold", default=0, min=0, soft_max=1)
    arthreshold_prop : bpy.props.FloatProperty(name="A/R Threshold", default=0.1, min=0, soft_max=1)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "attack_prop")
        layout.prop(self, "release_prop")
        layout.prop(self, "threshold_prop")
        layout.prop(self, "arthreshold_prop")

    def get_sound(self):
        sound = connected_node_sound(self, 0)
        if sound == None:
            return None
        return sound.envelope(self.attack_prop, self.release_prop,
            self.threshold_prop, self.arthreshold_prop)


class CM_ND_AudioFaderNode(bpy.types.Node):
    bl_idname = "cm_audio.fader_node"
    bl_label = "Fader by Time/Beats"
    bl_icon = "SPEAKER"

    start_prop : bpy.props.FloatProperty(name="Start In", default=0, soft_min=0)
    length_prop : bpy.props.FloatProperty(name="Length In", default=1, soft_min=0)
    starto_prop : bpy.props.FloatProperty(name="Start Out", default=0, soft_min=0)
    lengtho_prop : bpy.props.FloatProperty(name="Length Out", default=1, soft_min=0)
    fade_in_prop : bpy.props.BoolProperty(name="In", default=False)
    fade_out_prop : bpy.props.BoolProperty(name="Out", default=False)
    message : StringProperty(name="")

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        cm_pg = context.scene.cm_pg
        layout.prop(self, "start_prop")
        layout.prop(self, "length_prop")
        layout.prop(self, "starto_prop")
        layout.prop(self, "lengtho_prop")
        row = layout.row()
        row.prop(self, "fade_in_prop")
        row.prop(self, "fade_out_prop")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sound = connected_node_sound(self, 0)
        if cm.type_bool:
            start_in = self.start_prop
            length_in = self.length_prop
            start_out = self.starto_prop
            length_out = self.lengtho_prop
        else:
            start_in = self.start_prop * (60 / cm.bpm)
            length_in = self.length_prop * (60 / cm.bpm)
            start_out = self.starto_prop * (60 / cm.bpm)
            length_out = self.lengtho_prop * (60 / cm.bpm)
        if sound == None:
            return None
        if self.fade_in_prop:
            sound = sound.fadein(start_in, length_in)
        if self.fade_out_prop:
            sound = sound.fadeout(start_out, length_out)
        return sound


class CM_ND_AudioHighpassNode(bpy.types.Node):
    bl_idname = "cm_audio.highpass_node"
    bl_label = "Highpass"
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
        sound = connected_node_sound(self, 0)
        if sound == None:
            return None
        return sound.highpass(self.frequency_prop, self.q_prop)


class CM_ND_AudioLimitNode(bpy.types.Node):
    bl_idname = "cm_audio.limit_node"
    bl_label = "Limit by Time/Beats"
    bl_icon = "SPEAKER"

    start_prop : bpy.props.FloatProperty(name="Start", default=0, soft_min=0)
    end_prop : bpy.props.FloatProperty(name="Length", default=1, soft_min=0)
    message : StringProperty(name="")

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        cm_pg = context.scene.cm_pg
        layout.prop(self, "start_prop")
        layout.prop(self, "end_prop")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sound = connected_node_sound(self, 0)
        if cm.type_bool:
            start = self.start_prop
            length = self.start_prop + self.end_prop
        else:
            start = self.start_prop * (60 / cm.bpm)
            length = self.end_prop * (60 / cm.bpm)
        if sound == None or self.start_prop >= self.end_prop:
            return None
        return sound.limit(start, length)


class CM_ND_AudioLoopNode(bpy.types.Node):
    bl_idname = "cm_audio.loop_node"
    bl_label = "Loop"
    bl_icon = "SPEAKER"

    loop_prop : bpy.props.IntProperty(name="Loops #", default=1, soft_min=0,
    description="Number of Additional Loops")

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "loop_prop")

    def get_sound(self):
        sound = connected_node_sound(self, 0)
        if sound == None:
            return None
        return sound.loop(self.loop_prop)


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
        sound = connected_node_sound(self, 0)
        if sound == None:
            return None
        return sound.lowpass(self.frequency_prop, self.q_prop)


class CM_ND_AudioPitchNode(bpy.types.Node):
    bl_idname = "cm_audio.pitch_node"
    bl_label = "Pitch"
    bl_icon = "SPEAKER"

    pitch_prop : bpy.props.FloatProperty(name="Pitch", default=1, soft_min=0.1, soft_max=4)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "pitch_prop")

    def get_sound(self):
        sound = connected_node_sound(self, 0)
        if sound == None:
            return None
        return sound.pitch(self.pitch_prop)


class CM_ND_AudioVolumeNode(bpy.types.Node):
    bl_idname = "cm_audio.volume_node"
    bl_label = "Volume"
    bl_icon = "SPEAKER"

    volume_prop : bpy.props.FloatProperty(name="Volume", default=1, soft_min=0, soft_max=1)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "volume_prop")

    def get_sound(self):
        sound = connected_node_sound(self, 0)
        if sound == None:
            return None
        return sound.volume(self.volume_prop)


class CM_ND_AudioJoinNode(bpy.types.Node):
    bl_idname = "cm_audio.join_node"
    bl_label = "Simple Join"
    bl_icon = "SPEAKER"

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio 1")
        self.inputs.new("cm_socket.sound", "Audio 2")
        self.outputs.new("cm_socket.sound", "Audio")

    def get_sound(self):
        sound1 = connected_node_sound(self, 0)
        sound2 = connected_node_sound(self, 1)
        if sound1 == None or sound2 == None:
            return None
        return sound1.join(sound2)


class CM_ND_AudioSequenceNode(bpy.types.Node):
    bl_idname = "cm_audio.sequence_node"
    bl_label = "8-Way Sequencer"
    bl_icon = "SPEAKER"

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio 1")
        self.inputs.new("cm_socket.sound", "Audio 2")
        self.inputs.new("cm_socket.sound", "Audio 3")
        self.inputs.new("cm_socket.sound", "Audio 4")
        self.inputs.new("cm_socket.sound", "Audio 5")
        self.inputs.new("cm_socket.sound", "Audio 6")
        self.inputs.new("cm_socket.sound", "Audio 7")
        self.inputs.new("cm_socket.sound", "Audio 8")
        self.outputs.new("cm_socket.sound", "Audio")

    def get_sound(self):
        first = True
        for i in range(8):
            snd = connected_node_sound(self, i)
            if snd is not None:
                if first:
                    sound_list = snd
                    first = False
                else:
                    sound_list = sound_list.join(snd)
        return sound_list


class CM_ND_AudioMixNode(bpy.types.Node):
    bl_idname = "cm_audio.mix_node"
    bl_label = "Mix"
    bl_icon = "SPEAKER"

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio 1")
        self.inputs.new("cm_socket.sound", "Audio 2")
        self.outputs.new("cm_socket.sound", "Audio")

    def get_sound(self):
        sound1 = connected_node_sound(self, 0)
        sound2 = connected_node_sound(self, 1)
        if sound1 == None or sound2 == None:
            return None
        return sound1.mix(sound2)


class CM_ND_AudioMixEightNode(bpy.types.Node):
    bl_idname = "cm_audio.mix_eight_node"
    bl_label = "8 Channel Mixer"
    bl_icon = "SPEAKER"

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio 1")
        self.inputs.new("cm_socket.sound", "Audio 2")
        self.inputs.new("cm_socket.sound", "Audio 3")
        self.inputs.new("cm_socket.sound", "Audio 4")
        self.inputs.new("cm_socket.sound", "Audio 5")
        self.inputs.new("cm_socket.sound", "Audio 6")
        self.inputs.new("cm_socket.sound", "Audio 7")
        self.inputs.new("cm_socket.sound", "Audio 8")
        self.outputs.new("cm_socket.sound", "Audio")

    def get_sound(self):
        first = True
        for i in range(8):
            snd = connected_node_sound(self, i)
            if snd is not None:
                if first:
                    sound_list = snd
                    first = False
                else:
                    sound_list = sound_list.mix(snd)
        return sound_list


class CM_ND_AudioModulateNode(bpy.types.Node):
    bl_idname = "cm_audio.modulate_node"
    bl_label = "Modulate"
    bl_icon = "SPEAKER"

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio 1")
        self.inputs.new("cm_socket.sound", "Audio 2")
        self.outputs.new("cm_socket.sound", "Audio")

    def get_sound(self):
        sound1 = connected_node_sound(self, 0)
        sound2 = connected_node_sound(self, 1)
        if sound1 == None or sound2 == None:
            return None
        return sound1.modulate(sound2)


class CM_ND_AudioPingPongNode(bpy.types.Node):
    bl_idname = "cm_audio.pingpong_node"
    bl_label = "PingPong"
    bl_icon = "SPEAKER"

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def get_sound(self):
        sound = connected_node_sound(self, 0)
        if sound == None:
            return None
        return sound.pingpong()


class CM_ND_AudioReverseNode(bpy.types.Node):
    bl_idname = "cm_audio.reverse_node"
    bl_label = "Reverse"
    bl_icon = "SPEAKER"

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def get_sound(self):
        sound = connected_node_sound(self, 0)
        if sound == None:
          return None
        return sound.reverse()


class CM_ND_AudioResampleNode(bpy.types.Node):
    bl_idname = "cm_audio.resample_node"
    bl_label = "Resample To System"
    bl_icon = "SPEAKER"

    qual_bool : BoolProperty(name="H/L Quality", default=False)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, "qual_bool")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sound = connected_node_sound(self, 0)
        if sound == None:
          return None
        return sound.resample(cm.samples, self.qual_bool)


class CM_ND_AudioSlicerNode(bpy.types.Node):
    bl_idname = "cm_audio.slicer_node"
    bl_label = "Audio Slicer"
    bl_icon = "SPEAKER"

    slices_num : bpy.props.IntProperty(name="Slices #", default=5, min=2)
    slices_length : bpy.props.FloatProperty(name="Length (B)", default=1, min=0.001)
    slices_seq : bpy.props.StringProperty(name="", default="1,2,3,4,5",
        description="Playback Sequence - slice numbers from 1")
    slices_rev : bpy.props.StringProperty(name="", default="",
        description="Positions in Sequence to reverse")
    volume : FloatProperty(name="Volume", default=1, min=0.1)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, "slices_num")
        row.prop(self, "slices_length")
        row = layout.row()
        split = row.split(factor=0.30, align=True)
        split.label(text="Sequence")
        split.prop(self, "slices_seq")
        row = layout.row()
        split = row.split(factor=0.30, align=True)
        split.label(text="Reversals")
        split.prop(self, "slices_rev")
        row = layout.row()
        split = row.split(factor=0.30, align=True)
        split.label(text="")
        split.prop(self, "volume")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sound = connected_node_sound(self, 0)
        sound_out = None
        if sound == None or self.slices_num < 2 or "," not in self.slices_seq:
            return None
        length = self.slices_length * (60 / cm.bpm)
        start = 0
        stop = start + length
        params = []
        for i in range(self.slices_num):
            params.append([start, stop])
            start = start + length
            stop = stop + length
        first = True
        reversals = self.slices_rev.split(",")
        ind_r = 1
        for r in self.slices_seq.split(","):
            # FIXME Check it's an integer
            ind = int(r) - 1
            start = params[ind][0]
            stop = params[ind][1]
            if first:
                sound_out = sound.limit(start, stop).volume(self.volume)
                if str(ind_r) in reversals:
                    sound_out = sound_out.reverse().volume(self.volume)
                first = False
            else:
                snd = sound.limit(start, stop).volume(self.volume)
                if str(ind_r) in reversals:
                    snd = snd.reverse().volume(self.volume)
                sound_out = sound_out.join(snd)
            ind_r = ind_r + 1
        return sound_out
