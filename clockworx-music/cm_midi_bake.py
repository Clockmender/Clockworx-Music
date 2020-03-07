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
import os
import aud
import bpy
from pathlib import Path
from bpy.props import (
    IntProperty,
    FloatProperty,
    StringProperty,
    BoolProperty,
    EnumProperty,
    )
from .cm_functions import (
    get_note,
    get_freq,
    osc_generate,
    analyse_midi_file,
    )


class CM_ND_AudioMidiBakeNode(bpy.types.Node):
    bl_idname = "cm_audio.midi_bake_node"
    bl_label = "Clockworx MIDI Bake"
    bl_icon = "SPEAKER"

    use_vel : BoolProperty(name="Use MIDI Velocity", default=False)
    squ_val : BoolProperty(name="Use Square Waveforms", default=True)
    midi_channel: IntProperty(name="Midi Channel", default=2, min=2)
    time_off : FloatProperty(name="Offset (B)", default=0,
        description="Number of Beats offset from start of Song for Sound File")
    suffix : StringProperty(name="Obj Suffix", default="key")
    message1 : StringProperty()
    message2 : StringProperty()

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
    midi_file_name : StringProperty(subtype="FILE_PATH", name="Midi CSV file", default="//")
    sound_file_name : StringProperty(subtype="FILE_PATH", name="Sound file", default="//")
    write_name : StringProperty(subtype="FILE_PATH", name="Ouptut File Name", default="//")
    sequence_channel : IntProperty(name="Channel", default=1, description="VSE Channel")
    add_file : BoolProperty(name="Add to VSE", default=False)
    strip_name : StringProperty(name="Strip Name", default="")
    volume : FloatProperty(name="Volume", default=1.0)
    make_all : BoolProperty(name="All Channels", default=False)
    label_cont : BoolProperty(name="Label Controls", default=False)

    def draw_buttons(self, context, layout):
        cm_pg = context.scene.cm_pg
        layout.context_pointer_set("audionode", self)
        row = layout.row()
        row.prop(cm_pg, "mid_c")
        row.prop(self, "midi_channel")
        row = layout.row()
        row.prop(self, "use_vel")
        row.prop(self, "squ_val")

        layout.prop(self, "midi_file_name")
        layout.prop(self, "write_name")
        layout.prop(self, "sound_file_name")
        row = layout.row()
        row.prop(self, "label_cont")
        row.label(text="Control Suffix:")
        row.prop(self, "suffix", text="")
        layout.prop(self, "gen_type")
        row = layout.row()
        row.prop(self, "add_file")
        row.prop(self, "strip_name")
        row = layout.row()
        row.prop(self, "time_off")
        row.prop(self, "sequence_channel")
        row = layout.row()
        split = row.split(factor=0.50, align=True)
        split.label(text="")
        split.prop(self, "volume")
        layout.separator()
        row = layout.row()
        split = row.split(factor=0.3, align=True)
        split.prop(self, "make_all")
        split.operator("cm_audio.create_midi", icon="SOUND")
        row = layout.row()
        split = row.split(factor=0.3, align=True)
        split.label(text="")
        split.operator("cm_audio.create_sound", icon="SPEAKER")
        row = layout.row()
        split = row.split(factor=0.3, align=True)
        split.label(text="")
        split.operator("cm_audio.load_sound", icon="FILE_NEW")

        layout.label(text="")
        if self.message1 != "":
            layout.prop(self, "message1", text="")
        if self.message2 != "":
            layout.prop(self, "message2", text="")


class CM_OT_LoadSoundFile(bpy.types.Operator):
    bl_idname = "cm_audio.load_sound"
    bl_label = "Load Sound File to VSE"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        cm_node = context.node
        return cm_node.sound_file_name != "" and cm_node.sound_file_name != "//"

    def execute(self, context):
        cm_node = context.node
        cm = context.scene.cm_pg
        path = bpy.path.abspath(cm_node.sound_file_name)
        scene = context.scene
        offset = cm_node.time_off
        if not cm.type_bool:
            offset = offset * (60 / cm.bpm)
        if not scene.sequence_editor:
            scene.sequence_editor_create()
        soundstrip = scene.sequence_editor.sequences.new_sound(
            "Sound", path, cm_node.sequence_channel, (offset + cm.offset),
        )
        soundstrip.show_waveform = True
        return {"FINISHED"}


class CM_ND_AnalyseMidiNode(bpy.types.Node):
    bl_idname = "cm_audio.analyse_midi_node"
    bl_label = "Clockworx MIDI Analyser"
    bl_icon = "SPEAKER"

    midi_file_name : StringProperty(subtype="FILE_PATH", name="Midi CSV file", default="//")
    midi_channel : IntProperty(name="Channel", default=2, min=2)
    bpm : IntProperty(name="BPM", default=0)
    tempo : IntProperty(name="1st Tempo", default=0)
    pulse : IntProperty(name="Pulse", default=0)
    time_sig : StringProperty(name="Time Sig", default="")
    track_name : StringProperty(name="Track Name", default="")
    tracks : StringProperty(name="Tracks", default="")


    def init(self, context):
        self.outputs.new("cm_socket.sound", "File Info")

    def draw_buttons(self, context, layout):
        cm_pg = context.scene.cm_pg
        layout.context_pointer_set("audionode", self)
        layout.prop(self, "midi_file_name")
        layout.prop(self, "midi_channel")
        layout.prop(self, "track_name")
        layout.prop(self, "bpm")
        layout.prop(self, "pulse")
        layout.prop(self, "tempo")
        layout.prop(self, "time_sig")
        layout.prop(cm_pg, "channels")
        layout.prop(self, "tracks")
        layout.operator("cm_audio.analyse_midi", text="Analyse File")

    def info(self,context):
        cm = context.scene.cm_pg
        return cm.data_dict


class CM_OT_AnalyseMidiFile(bpy.types.Operator):
    bl_idname = "cm_audio.analyse_midi"
    bl_label = "Analyse Midi File"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        cm_node = context.node
        return ".csv" in cm_node.midi_file_name

    def execute(self, context):
        cm_node = context.node
        cm = context.scene.cm_pg
        path = bpy.path.abspath(cm_node.midi_file_name)
        analyse_midi_file(context)
        cm_node.pulse = cm.data_dict["Pulse"]
        cm_node.bpm = cm.data_dict["BPM"]
        cm_node.tempo = int(cm.data_dict["Tempo"][0][1])
        cm_node.time_sig = f"{cm.data_dict['TimeSig'][0]}:{cm.data_dict['TimeSig'][0]}"
        cm_node.track_name = cm.data_dict['Track Name']
        first = True
        for v in range(len(cm.data_dict['Tracks'])):
            if first:
                cm_node.tracks = cm.data_dict['Tracks'][v][0]
                first = False
            else:
                cm_node.tracks = cm_node.tracks + ", " + cm.data_dict['Tracks'][v][0]
        return {"FINISHED"}


class CM_OT_CreateMIDIControls(bpy.types.Operator):
    bl_idname = "cm_audio.create_midi"
    bl_label = "Create MIDI Controls in 3D View"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        cm_node = context.node
        return ".csv" in cm_node.midi_file_name

    def execute(self, context):
        cm_node = context.node
        cm = context.scene.cm_pg
        path = bpy.path.abspath(cm_node.midi_file_name)
        analyse_midi_file(context)
        fps = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base
        if cm_node.make_all:
            channel_list = cm.channels.split(",")
        else:
            channel_list = []
            channel_list.append(str(cm_node.midi_channel))
        max = 0
        for channel in channel_list:
            cm.event_dict.clear()
            with open(path) as f1:
                for line in f1:
                    in_l = [elt.strip() for elt in line.split(",")]
                    if (
                        (len(in_l) == 6)
                        and (in_l[2].split("_")[0] == "Note")
                        and (in_l[0] == channel)
                        ):
                        # taken above str(cm_node.midi_channel)
                        # Note events for the chosen channel
                        noteNum = int(in_l[4]) - 12 if cm.mid_c else int(in_l[4])
                        noteName = get_note(noteNum, 0)
                        if cm_node.use_vel:
                            velo = round(int(in_l[5]) / 127, 3)
                            onOff = velo if in_l[2] == "Note_on_c" else 0.0
                        else:
                            onOff = 1.0 if in_l[2] == "Note_on_c" else 0.0
                        # time would be value * 60 / bpm * Pulse
                        frame = (
                            int(in_l[1])
                            * (60 * fps)
                            / (cm.data_dict.get("BPM") * cm.data_dict.get("Pulse"))
                        )
                        # Check frame does not overlap last entry
                        # Note cannot start before previous same note has finished!
                        if noteName in cm.event_dict.keys():  # Is not the first note event
                            lastFrame = cm.event_dict.get(noteName)[-1][0]
                            if frame <= lastFrame:
                                frame = (
                                    lastFrame + cm.spacing if cm.spacing > 0 else lastFrame + cm.easing
                                )
                        frame = frame + cm.offset
                        if noteName not in cm.event_dict.keys():
                            cm.event_dict[noteName] = [[frame, onOff]]
                        else:
                            # Add records for events
                            if cm_node.squ_val:
                                if in_l[2] == "Note_on_c":
                                    cm.event_dict[noteName].append([(frame - cm.easing), 0.0])
                                else:
                                    if cm_node.use_vel:
                                        velo = cm.data_dict.get(noteName)[-1][1]
                                        cm.event_dict[noteName].append([(frame - cm.easing), velo])
                                    else:
                                        cm.event_dict[noteName].append([(frame - cm.easing), 1.0])
                            cm.event_dict[noteName].append([frame, onOff])
                # Make Control Empties.
                xLoc = 0
                for k in cm.event_dict.keys():
                    bpy.ops.object.empty_add(
                        type="SINGLE_ARROW", location=(xLoc, int(channel) / 10, 0), radius=0.03
                    )
                    bpy.context.active_object.name = f"{str(k)}_{cm_node.suffix}{channel}"
                    #(
                    #    str(k) + "_" + cm_node.suffix + channel
                    #)
                    if cm_node.label_cont:
                        bpy.context.active_object.show_name = True
                    indV = True
                    for v in cm.event_dict.get(k):
                        frm = v[0]
                        val = v[1]
                        if indV:
                            # add keyframe just before first Note On
                            bpy.context.active_object.location.z = 0
                            bpy.context.active_object.keyframe_insert(
                                data_path="location", index=2, frame=frm - cm.easing
                            )
                            indV = False
                        bpy.context.active_object.location.z = val / 10
                        bpy.context.active_object.keyframe_insert(
                            data_path="location", index=2, frame=frm
                        )
                    bpy.context.active_object.select_set(state=False)
                    xLoc = xLoc + 0.1
                cm_node.message1 = "Process Complete"
                max = max + sum(len(v) for v in cm.event_dict.values())
            cm_node.message2 = (
                "Channel "
                + cm.channels
                + " Processed, Events: "
                + str(max)
            )

        return {"FINISHED"}


class CM_OT_CreateMIDISound(bpy.types.Operator):
    bl_idname = "cm_audio.create_sound"
    bl_label = "Create MIDI Sound (in VSE)"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        cm_node = context.node
        return ".csv" in cm_node.midi_file_name and ".flac" in cm_node.write_name

    def execute(self, context):
        cm_node = context.node
        cm = context.scene.cm_pg
        path = bpy.path.abspath(cm_node.midi_file_name)
        analyse_midi_file(context)
        cm.time_dict.clear()

        with open(path) as f1:
            count = 0
            for line in f1:
                in_l = [elt.strip() for elt in line.split(",")]
                if (
                    (len(in_l) == 6)
                    and (in_l[2].split("_")[0] == "Note")
                    and (in_l[0] == str(cm_node.midi_channel))
                ):
                    # Note events for the chosen channel
                    # Write frequencies to dictionary
                    noteNum = int(in_l[4]) - 12 if cm.mid_c else int(in_l[4])
                    noteFreq = get_freq(noteNum)
                    if cm_node.use_vel:
                        velo = round(int(in_l[5]) / 127, 3)
                        onOff = velo if in_l[2] == "Note_on_c" else 0.0
                    else:
                        onOff = 1.0 if in_l[2] == "Note_on_c" else 0.0
                    # time would be value * 60 / bpm * Pulse
                    time = (
                        int(in_l[1])
                        * 60
                        / (cm.data_dict.get("BPM") * cm.data_dict.get("Pulse"))
                    )
                    if noteFreq not in cm.time_dict.keys():
                        cm.time_dict[noteFreq] = [[time, onOff]]
                    else:
                        cm.time_dict[noteFreq].append([time, onOff])
            # Make Sounds.
            first = True
            #count = 0
            for k in cm.time_dict.keys():
                values = cm.time_dict.get(k)
                for i in range(int(len(values)/2)):
                    r = i * 2
                    time_s = values[r][0]
                    time_f = values[r + 1][0]
                    volume = values[r][1]
                    snd = osc_generate([0,k], cm_node.gen_type, cm.samples)
                    snd = snd.limit(0, time_f - time_s).rechannel(cm.sound_channels)
                    snd = snd.volume(cm_node.volume)
                    if first:
                        sound = snd.delay(time_s)
                        first = False
                    else:
                        sound = sound.mix(snd.delay(time_s))
            # Write File
            if ".flac" not in cm_node.write_name:
                cm_node.message1 = "No/Wrong Output File Specified must be .flac"
                return {"FINISHED"}
            path = bpy.path.abspath(cm_node.write_name)
            my_file = Path(path)
            if my_file.is_file():
                os.remove(path)
            snd_out = sound.write(path, aud.RATE_16000, aud.CHANNELS_STEREO,
                aud.FORMAT_FLOAT32, aud.CONTAINER_FLAC, aud.CODEC_FLAC)
            if cm_node.add_file:
                bps = cm.bpm / 60
                fps = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base
                frame = ((cm_node.time_off * (1 / bps)) * fps) + cm.offset
                scene = context.scene
                if not scene.sequence_editor:
                    scene.sequence_editor_create()
                soundstrip = scene.sequence_editor.sequences.new_sound(
                    "Sound", path, cm_node.sequence_channel, frame,
                )
                soundstrip.show_waveform = True
                if cm_node.strip_name != "":
                    soundstrip.name = cm_node.strip_name
            cm_node.message1 = "Process Complete"
            cm_node.message2 = (
                "Channel "
                + str(cm_node.midi_channel)
                + " Processed, Events: "
                + str(sum(len(v) for v in cm.time_dict.values()))
            )

        return {"FINISHED"}
