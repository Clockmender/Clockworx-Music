import bpy
import aud
import os
from pathlib import Path

class CM_OT_WriteAudioNodeOperator(bpy.types.Operator):
    bl_idname = "cm_audio.write_audio"
    bl_label = "Write Audio"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        cm_node = context.node
        return ".flac" in cm_node.write_name

    def execute(self, context):
        cm_node = context.node
        cm = context.scene.cm_pg
        path = bpy.path.abspath(cm_node.write_name)
        my_file = Path(path)
        if my_file.is_file():
            os.remove(path)
        sound = context.audionode.get_sound()
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
        return {"FINISHED"}
