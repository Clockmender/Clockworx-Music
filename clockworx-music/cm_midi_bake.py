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
from .cm_functions import get_note, get_freq, osc_generate


class CM_ND_AudioMidiBakeNode(bpy.types.Node):
    bl_idname = "cm_audio.midi_bake_node"
    bl_label = "CM MIDI Bake"
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
    write_name : StringProperty(subtype="FILE_PATH", name="Ouptut File Name", default="//")
    sequence_channel : IntProperty(name="Channel", default=1, description="VSE Channel")
    add_file : BoolProperty(name="Add to VSE", default=False)
    strip_name : StringProperty(name="Strip Name", default="")

    def draw_buttons(self, context, layout):
        cm_pg = context.scene.cm_pg
        layout.context_pointer_set("audionode", self)
        row = layout.row()
        row.prop(cm_pg, "mid_c")
        row.prop(self, "midi_channel")
        row = layout.row()
        row.prop(self, "use_vel")
        row.prop(self, "squ_val")

        layout.prop(cm_pg, "midi_file_name")
        layout.prop(self, "write_name")
        layout.prop(cm_pg, "sound_file_name")
        layout.prop(self, "suffix")
        layout.prop(self, "gen_type")
        row = layout.row()
        row.prop(self, "add_file")
        row.prop(self, "strip_name")
        row = layout.row()
        row.prop(self, "time_off")
        row.prop(self, "sequence_channel")
        row = layout.row()
        split = row.split(factor=0.30, align=True)
        split.label(text="")
        split.operator("cm_audio.create_midi", icon="SOUND")
        row = layout.row()
        split = row.split(factor=0.30, align=True)
        split.label(text="")
        split.operator("cm_audio.create_sound", icon="SPEAKER")
        row = layout.row()
        split = row.split(factor=0.30, align=True)
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
        return True

    def execute(self, context):
        cm_node = context.node
        cm = context.scene.cm_pg
        path = bpy.path.abspath(cm.sound_file_name)
        scene = context.scene
        if not scene.sequence_editor:
            scene.sequence_editor_create()
        soundstrip = scene.sequence_editor.sequences.new_sound(
            "Sound", path, cm_node.sequence_channel, (cm_node.time_off + cm.offset),
        )
        soundstrip.show_waveform = True
        return {"FINISHED"}

def AnalyseMidiFile(context):
    cm_node = context.node
    cm = context.scene.cm_pg
    cm_node.message1 = "Midi File Analysed: " + str(os.path.basename(cm.midi_file_name))
    cm_node.message2 = "Check/Load Sound File, Use Velocity, Easing & Offset"
    fps = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base
    cm.data_dict.clear()
    path = bpy.path.abspath(cm.midi_file_name)
    if ".csv" not in path:
        cm_node.message1 = "No CSV File specified"
        return
    with open(path) as f1:
        for line in f1:
            in_l = [elt.strip() for elt in line.split(",")]
            if in_l[2] == "Header":
                # Get Pulse variable.
                pulse = int(in_l[5])
                cm.data_dict["Pulse"] = pulse
            elif in_l[2] == "Tempo":
                if in_l[1] == "0":
                    # Get Initial Tempo.
                    tempo = in_l[3]
                    bpm = float(round((60000000 / int(tempo)), 3))
                    cm.data_dict["BPM"] = bpm
                    cm.data_dict["Tempo"] = [[0, tempo]]
                elif in_l[0] == "1" and in_l[2] == "Tempo":
                    # Add Tempo Changes & timings to Tempo Key in dataD.
                    frame = round(int(in_l[1]) * (60 * fps) / (bpm * pulse), 2)
                    cm.data_dict.get("Tempo").append([str(frame), in_l[3]])
            elif in_l[2] == "Time_signature":
                # Get Time Signature
                cm.data_dict["TimeSig"] = [int(in_l[3]), int(in_l[4])]
            elif (
                (in_l[2] == "Title_t") and (int(in_l[0]) > 1) and (in_l[3] != "Master Section")
            ):
                # Get Track Names & Numbers
                if in_l[0] == str(cm_node.midi_channel):
                    tName = in_l[3].strip('"')
                    cm.data_dict["Track Name"] = tName
                otName = in_l[3].strip('"')
                if "Tracks" not in dataD.keys():
                    cm.data_dict["Tracks"] = [[otName, int(in_l[0])]]
                    cm.channels = in_l[0] + " - " + otName
                else:
                    cm.data_dict.get("Tracks").append([otName, int(in_l[0])])
                    cm.channels = cm.channels + "&" + in_l[0] + " - " + otName

    cm_node.message2 = "Midi CSV File Analysed and Data Dictionary Built"
    return


class CM_OT_CreateMIDIControls(bpy.types.Operator):
    bl_idname = "cm_audio.create_midi"
    bl_label = "Create MIDI Controls in 3D View"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        cm_node = context.node
        cm = context.scene.cm_pg
        path = bpy.path.abspath(cm.midi_file_name)
        if ".csv" not in path:
            cm_node.message1 = "No MIDI file Specified"
            cm_node.message2 = ""
            return {"FINISHED"}
        AnalyseMidiFile(context)
        cm.event_dict.clear()
        fps = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base

        with open(path) as f1:
            for line in f1:
                in_l = [elt.strip() for elt in line.split(",")]
                if (
                    (len(in_l) == 6)
                    and (in_l[2].split("_")[0] == "Note")
                    and (in_l[0] == str(cm_node.midi_channel))
                ):
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
                    type="SINGLE_ARROW", location=(xLoc, cm_node.midi_channel / 10, 0), radius=0.03
                )
                bpy.context.active_object.name = (
                    str(k) + "_" + cm_node.suffix + str(cm_node.midi_channel)
                )
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
            cm_node.message2 = (
                "Channel "
                + str(cm_node.midi_channel)
                + " Processed, Events: "
                + str(sum(len(v) for v in cm.event_dict.values()))
            )

        return {"FINISHED"}


class CM_OT_CreateMIDISound(bpy.types.Operator):
    bl_idname = "cm_audio.create_sound"
    bl_label = "Create MIDI Sound in VSE"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        cm_node = context.node
        cm = context.scene.cm_pg
        path = bpy.path.abspath(cm.midi_file_name)
        if ".csv" not in path:
            cm_node.message1 = "No MIDI file Specified"
            cm_node.message2 = ""
            return {"FINISHED"}
        AnalyseMidiFile(context)
        cm.time_dict.clear()

        with open(path) as f1:
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
            for k in cm.time_dict.keys():
                values = cm.time_dict.get(k)
                for i in range(int(len(values)/2)):
                    time_s = values[i][0]
                    time_f = values[i + 1][0]
                    volume = values[i][1]
                    snd = osc_generate([0,k], cm_node.gen_type, cm.samples)
                    snd = snd.limit(0, time_f - time_s).rechannel(cm.sound_channels)
                    if first:
                        sound = snd
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
