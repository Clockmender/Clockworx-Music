import bpy
import aud
import os
from pathlib import Path

class CM_OT_RecordAudioNodeOperator(bpy.types.Operator):
    bl_idname = "cm_audio.record_audio"
    bl_label = "Record Audio"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        cm_node = context.node
        return ".flac" in cm_node.file_name

    def execute(self, context):
        cm_node = context.node
        cm = context.scene.cm_pg
        start_frm = cm_node.start_frm
        stop_frm = cm_node.stop_frm
        frame_time = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base
        first = True
        sound_out = None
        if start_frm >= stop_frm:
            return {"FINISHED"}

        for i in range(start_frm, stop_frm + 1):
            context.scene.frame_current = i
            delay = (context.scene.frame_current - start_frm) / frame_time
            sound = cm_node.get_sound()
            if sound is not None:
                sound = sound.delay(delay)
                if first:
                    sound_out = sound
                    first = False
                else:
                    sound_out = sound_out.mix(sound)

        if sound_out is not None:
            path = bpy.path.abspath(cm_node.file_name)
            my_file = Path(path)
            if my_file.is_file():
                if cm_node.overwrite:
                    os.remove(path)
                else:
                    self.report({"ERROR"}, "File Exists - Overwrite not Checked")
                    return {"FINISHED"}
            snd_out = sound_out.write(path, aud.RATE_16000, aud.CHANNELS_STEREO,
                aud.FORMAT_FLOAT32, aud.CONTAINER_FLAC, aud.CODEC_FLAC)

            if not context.scene.sequence_editor:
                context.scene.sequence_editor_create()
            soundstrip = context.scene.sequence_editor.sequences.new_sound(
                f"{cm_node.sequence_name}: {start_frm}-{stop_frm}",
                path,
                cm_node.sequence_channel,
                start_frm,
            )
            soundstrip.show_waveform = True
            aud.Device().play(sound_out)
            context.scene.frame_current = start_frm

        return {"FINISHED"}
