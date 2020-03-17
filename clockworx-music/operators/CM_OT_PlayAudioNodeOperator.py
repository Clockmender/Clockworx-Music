import bpy
import aud

class CM_OT_PlayAudioNodeOperator(bpy.types.Operator):
    bl_idname = "cm_audio.play_audio"
    bl_label = "Play Audio"

    @classmethod
    def poll(cls, context):
        return context.audionode.get_sound() != None

    def execute(self, context):
        sound = context.audionode.get_sound()
        if sound != None:
            aud.Device().play(sound)
        return {"FINISHED"}
