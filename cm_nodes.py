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
    PointerProperty,
    EnumProperty,
    StringProperty,
    BoolProperty,
)
from .cm_sockets import (
    CM_SK_AudioNodeSocket,
    CM_SK_FloatNodeSocket,
    CM_SK_IntNodeSocket,
    CM_SK_BoolNodeSocket,
    CM_SK_TextNodeSocket,
)

from .cm_functions import (
    connected_node_sound,
    connected_node_info,
    get_socket_values,
    get_index,
    get_freq,
    osc_generate,
    get_chord_ind,
    get_chord,
    view_lock,
)


class CM_ND_AudioDebugNode(bpy.types.Node):
    bl_idname = "cm_audio.debug_node"
    bl_label = "Debug"
    bl_icon = "SPEAKER"

    text_input: bpy.props.StringProperty(name="Value", default="")

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Input")

    def draw_buttons(self, context, layout):
        layout.prop(self, "text_input")
        layout.context_pointer_set("audionode", self)
        layout.operator("cm_audio.display_audio")

    def info(self, context):
        input = connected_node_info(self, 0)
        self.text_input = str(input)


class CM_ND_AudioFrameNode(bpy.types.Node):
    bl_idname = "cm_audio.frame_node"
    bl_label = "Frame Info"
    bl_icon = "SPEAKER"

    frame_num: bpy.props.IntProperty(name="Frame")

    def init(self, context):
        self.outputs.new("cm_socket.int", "Frame")

    def draw_buttons(self, context, layout):
        layout.prop(self, "frame_num")

    def execute(self):
        self.frame_num = bpy.context.scene.frame_current
        return self.frame_num


class CM_ND_AudioTimeNode(bpy.types.Node):
    bl_idname = "cm_audio.time_node"
    bl_label = "Time Info"
    bl_icon = "SPEAKER"

    time_num: bpy.props.FloatProperty(name="Time")

    def init(self, context):
        self.outputs.new("cm_socket.float", "Time")

    def draw_buttons(self, context, layout):
        layout.prop(self, "time_num")

    def execute(self):
        self.time_num = (
            bpy.context.scene.frame_current / bpy.context.scene.render.fps
        ) * bpy.context.scene.render.fps_base
        return self.time_num


class CM_ND_AudioBeatsNode(bpy.types.Node):
    bl_idname = "cm_audio.beats_node"
    bl_label = "Beats Info"
    bl_icon = "SPEAKER"

    beats_num: bpy.props.FloatProperty(name="Beats")

    def init(self, context):
        self.outputs.new("cm_socket.float", "Beats")

    def draw_buttons(self, context, layout):
        layout.prop(self, "beats_num")

    def execute(self):
        cm = bpy.context.scene.cm_pg
        bps = cm.bpm / 60
        fps = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base
        frame = bpy.context.scene.frame_current
        self.beats_num = round((((frame - cm.offset) / fps) * bps), 3)
        return self.beats_num


class CM_ND_AudioInfoNode(bpy.types.Node):
    bl_idname = "cm_audio.info_node"
    bl_label = "Project Info"
    bl_icon = "SPEAKER"

    frame_num: bpy.props.IntProperty(name="Frame")
    time_num: bpy.props.FloatProperty(name="Time")
    beats_num: bpy.props.FloatProperty(name="Beats")

    def draw_buttons(self, context, layout):
        layout.prop(self, "frame_num")
        layout.prop(self, "time_num")
        layout.prop(self, "beats_num")

    def execute(self):
        cm = bpy.context.scene.cm_pg
        bps = cm.bpm / 60
        fps = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base
        frame = bpy.context.scene.frame_current
        self.beats_num = round((((frame - cm.offset) / fps) * bps), 3)
        self.time_num = (
            bpy.context.scene.frame_current / bpy.context.scene.render.fps
        ) * bpy.context.scene.render.fps_base
        self.frame_num = bpy.context.scene.frame_current


class CM_ND_SoundInfoNode(bpy.types.Node):
    bl_idname = "cm_audio.sound_info_node"
    bl_label = "Sound Info"
    bl_icon = "SPEAKER"

    length : FloatProperty(name="Length", default=0)
    samples : IntProperty(name="Samples", default=0)
    channels: IntProperty(name="Channels", default=0)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "length")
        layout.prop(self, "samples")
        layout.prop(self, "channels")

    def execute(self):
        cm = bpy.context.scene.cm_pg
        sound = connected_node_sound(self, 0)
        if sound == None:
            return None
        specs = sound.specs
        length = sound.length
        self.channels = specs[1]
        self.samples = specs[0]
        self.length = length / specs[0]
        if not cm.type_bool:
            self.length = self.length * (60 / cm.bpm)

    def get_sound(self):
        return connected_node_sound(self, 0)


class CM_ND_AudioFloatNode(bpy.types.Node):
    bl_idname = "cm_audio.float_node"
    bl_label = "Float"
    bl_icon = "SPEAKER"

    float_num: bpy.props.FloatProperty(name="Float", default=0.0)

    def init(self, context):
        self.outputs.new("cm_socket.float", "Float")

    def draw_buttons(self, context, layout):
        layout.prop(self, "float_num", text="")

    def get_sound(self):
        return self.float_num


class CM_ND_AudioIntNode(bpy.types.Node):
    bl_idname = "cm_audio.int_node"
    bl_label = "Integer"
    bl_icon = "SPEAKER"

    int_num: bpy.props.IntProperty(name="Integer", default=0)

    def init(self, context):
        self.outputs.new("cm_socket.int", "Integer")

    def draw_buttons(self, context, layout):
        layout.prop(self, "int_num", text="")

    def get_sound(self):
        return self.int_num


class CM_ND_AudioTextNode(bpy.types.Node):
    bl_idname = "cm_audio.text_node"
    bl_label = "Text"
    bl_icon = "SPEAKER"

    text_input: bpy.props.StringProperty(name="Text", default="")

    def init(self, context):
        self.outputs.new("cm_socket.text", "Text")

    def draw_buttons(self, context, layout):
        layout.prop(self, "text_input", text="")

    def get_sound(self):
        return self.text_input


class CM_ND_AudioBoolNode(bpy.types.Node):
    bl_idname = "cm_audio.bool_node"
    bl_label = "Boolean"
    bl_icon = "SPEAKER"

    bool_input: bpy.props.BoolProperty(name="Boolean", default=False)

    def init(self, context):
        self.outputs.new("cm_socket.bool", "Boolean")

    def draw_buttons(self, context, layout):
        layout.prop(self, "bool_input", text="")

    def get_sound(self):
        return self.bool_input


class CM_ND_AudioSoundNode(bpy.types.Node):
    bl_idname = "cm_audio.sound_node"
    bl_label = "Sound Generator"
    bl_icon = "SPEAKER"

    gen_type: EnumProperty(
        items=(
            ("sine", "Sine", "Sine Waveform"),
            ("triangle", "Triangle", "Triangle Waveform"),
            ("square", "Square", "Square Waveform"),
            ("sawtooth", "Sawtooth", "Sawtooth Waveform"),
            ("silence", "Silence", "Silence - no Waveform"),
        ),
        name="Waveform",
        default="sine",
        description="Waveform for Sound",
    )
    message : StringProperty(name="Message")

    def init(self, context):
        self.inputs.new("cm_socket.text", "Note")
        self.inputs.new("cm_socket.float", "Frequency")
        self.inputs.new("cm_socket.float", "Volume")
        self.inputs.new("cm_socket.float", "Delay (B)")
        self.inputs.new("cm_socket.float", "Length (B)")
        self.inputs.new("cm_socket.bool", "Reverse")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "gen_type")
        if self.message != "":
            layout.prop(self, "message", text="")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sockets = self.inputs.keys()
        input_values = get_socket_values(self, sockets, self.inputs)
        input_values[0] = input_values[0].split(",")
        # notes are now a list
        first = True
        for i in range(len(input_values[0])):
            index = get_index(input_values[0][i])
            if index in range(0, 107):
                freq = get_freq(index)
            else:
                freq = 0
            if freq > 0:
                input_values[1] = freq
            sound = osc_generate(input_values, self.gen_type, cm.samples)
            sound = sound.volume(input_values[2])
            bps = cm.bpm / 60
            sound = sound.limit(0, (input_values[4] / bps))
            sound = sound.delay(input_values[3] / bps)
            sound = sound.rechannel(cm.sound_channels)
            if input_values[5]:
                sound = sound.reverse()
            if first:
                sound_out = sound
                first = False
            else:
                sound_out = sound_out.join(sound)
        return sound_out

class CM_ND_AudioChordNode(bpy.types.Node):
    bl_idname = "cm_audio.chord_node"
    bl_label = "Chord Generator"
    bl_icon = "SPEAKER"

    gen_type: EnumProperty(
        items=(
            ("sine", "Sine", "Sine Waveform"),
            ("triangle", "Triangle", "Triangle Waveform"),
            ("square", "Square", "Square Waveform"),
            ("sawtooth", "Sawtooth", "Sawtooth Waveform"),
            ("silence", "Silence", "Silence - no Waveform"),
        ),
        name="Waveform",
        default="sine",
        description="Waveform for Sound",
    )
    message : StringProperty(name="Message")
    num_notes : IntProperty(name="Notes #", default=3, min=3, max=5)

    def init(self, context):
        self.inputs.new("cm_socket.text", "Note")
        self.inputs.new("cm_socket.float", "Volume")
        self.inputs.new("cm_socket.float", "Length (B)")
        self.inputs.new("cm_socket.bool", "Reverse")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "gen_type")
        if self.message != "":
            layout.prop(self, "message", text="")
        layout.prop(self, "num_notes")

    def get_sound(self):
        self.use_custom_color = True
        self.useNetworkColor = False
        self.color = (0.5,0.75,1.0)
        cm = bpy.context.scene.cm_pg
        sockets = self.inputs.keys()
        input_values = get_socket_values(self, sockets, self.inputs)
        index_list = get_chord_ind(input_values[0], self.num_notes)
        input_values.insert(1, 0)
        bps = cm.bpm / 60
        duration = input_values[3] * (1 / bps)
        for i in range(0, self.num_notes):
            input_values[1] = get_freq(index_list[i])
            snd = osc_generate(input_values, self.gen_type, cm.samples)
            snd = snd.volume(input_values[2])
            snd = snd.limit(0, duration)
            snd = snd.rechannel(cm.sound_channels)
            if i == 0:
                sound = snd
            else:
                sound = sound.mix(snd)
        if input_values[4]:
            sound = sound.reverse()
        return sound


class CM_ND_AudioArpeggioNode(bpy.types.Node):
    bl_idname = "cm_audio.arpeggio_node"
    bl_label = "Arpeggio Generator"
    bl_icon = "SPEAKER"

    gen_type: EnumProperty(
        items=(
            ("sine", "Sine", "Sine Waveform"),
            ("triangle", "Triangle", "Triangle Waveform"),
            ("square", "Square", "Square Waveform"),
            ("sawtooth", "Sawtooth", "Sawtooth Waveform"),
        ),
        name="Waveform",
        default="sine",
        description="Waveform for Sound",
    )
    message : StringProperty(name="Message")
    num_notes : IntProperty(name="Notes #", default=3, min=3, max=9)

    def init(self, context):
        self.inputs.new("cm_socket.text", "Note")
        self.inputs.new("cm_socket.float", "Volume")
        self.inputs.new("cm_socket.float", "Length (B)")
        self.inputs.new("cm_socket.bool", "Reverse")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "gen_type")
        layout.prop(self, "num_notes")
        if self.message != "":
            layout.prop(self, "message", text="")

    def get_sound(self):
        self.use_custom_color = True
        self.useNetworkColor = False
        self.color = (0.5,0.75,1.0)
        cm = bpy.context.scene.cm_pg
        sockets = self.inputs.keys()
        input_values = get_socket_values(self, sockets, self.inputs)
        freq_list = get_chord(input_values[0],self.num_notes)
        bps = cm.bpm / 60
        duration = input_values[2] * (1 / bps)
        if input_values[3]:
            freq_list = freq_list[::-1]
        for r in range(len(freq_list)):
            snd = osc_generate([0, freq_list[r]], self.gen_type, cm.samples)
            snd = snd.limit(0, duration).volume(input_values[1])
            if r == 0:
                sound = snd
            else:
                sound = sound.join(snd)
        return sound


class CM_ND_AudioFileNode(bpy.types.Node):
    bl_idname = "cm_audio.file_node"
    bl_label = "Sound File"
    bl_icon = "SPEAKER"

    file_name_prop: bpy.props.StringProperty(subtype="FILE_PATH", name="File", default="//")

    def init(self, context):
        self.inputs.new("cm_socket.float", "Volume")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "file_name_prop")

    def get_sound(self):
        sockets = self.inputs.keys()
        input_values = get_socket_values(self, sockets, self.inputs)
        cm = bpy.context.scene.cm_pg
        sound = aud.Sound.file(bpy.path.abspath(self.file_name_prop))
        sound = sound.volume(input_values[0])
        sound = sound.rechannel(cm.sound_channels)
        return sound


class CM_ND_AudioOutputNode(bpy.types.Node):
    bl_idname = "cm_audio.output_node"
    bl_label = "Speaker"
    bl_icon = "SPEAKER"

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")

    def get_sound(self):
        sound = connected_node_sound(self, 0)
        return sound

    def draw_buttons(self, context, layout):
        layout.context_pointer_set("audionode", self)
        layout.operator("cm_audio.play_audio")
        layout.operator("cm_audio.stop_audio")


class CM_ND_AudioWriteNode(bpy.types.Node):
    bl_idname = "cm_audio.write_node"
    bl_label = "Play/Write Sound"
    bl_icon = "SPEAKER"

    write_name : StringProperty(subtype="FILE_PATH", name="Ouptut File Name", default="//")
    sequence_channel : IntProperty(name="Channel", default=1)
    add_file : BoolProperty(name="Add to VSE", default=False)
    time_off : FloatProperty(name="Offset (B)", default=0,
        description="Number of Beats offset from start of song")
    strip_name : StringProperty(name="Strip Name", default="")

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")

    def get_sound(self):
        sound = connected_node_sound(self, 0)
        return sound

    def draw_buttons(self, context, layout):
        layout.context_pointer_set("audionode", self)
        layout.operator("cm_audio.play_audio")
        box = layout.box()
        box.operator("cm_audio.stop_audio")
        box.prop(self, "write_name")
        box.prop(self, "strip_name")
        box.prop(self, "add_file")
        box.prop(self, "time_off")
        box.prop(self, "sequence_channel")
        box.operator("cm_audio.write_audio")


class CM_ND_AudioControlNode(bpy.types.Node):
    bl_idname = "cm_audio.control_node"
    bl_label = "Clockworx Music Control"
    bl_icon = "SPEAKER"

    bpm : IntProperty(name="BPM", default=60)
    time_sig_num: IntProperty(name="Time Sig N", default=4)
    time_sig_den: IntProperty(name="Time Sig D", default=4)
    note_den : IntProperty(name="Note Denom.",min=1,default=16,max=64)
    message : StringProperty(name="Message")
    samples : IntProperty(name="Samples", default=44100, min=6000, max=192000)

    def draw_buttons(self, context, layout):
        cm_pg = context.scene.cm_pg
        layout.context_pointer_set("audionode", self)
        layout.operator("cm_audio.execute_start", icon="PLAY")
        layout.operator("cm_audio.execute_stop", icon="SNAP_FACE")
        layout.label(text="CM Constants")
        layout.prop(self, "bpm")
        layout.prop(self, "time_sig_num")
        layout.prop(self, "time_sig_den")
        layout.prop(self, "samples")
        layout.prop(self, "note_den")
        layout.operator("cm_audio.set_constants", icon="PLAY_SOUND")
        layout.label(text="Other CM Parameters")
        layout.prop(cm_pg, "offset")
        row = layout.row()
        row.prop(cm_pg, "sound_channels")
        row.prop(cm_pg, "mid_c")
        if self.message != "":
            layout.prop(self, "message", text="")

    def execute(self):
        view_lock()
