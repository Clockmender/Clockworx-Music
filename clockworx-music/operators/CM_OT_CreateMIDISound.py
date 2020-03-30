import bpy
import os
import aud
from pathlib import Path
from ..cm_functions import (
    analyse_midi_file,
    osc_generate,
    get_freq,
    )

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
