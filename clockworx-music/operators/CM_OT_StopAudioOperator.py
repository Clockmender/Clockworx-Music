import bpy
import aud

class CM_OT_StopAudioOperator(bpy.types.Operator):
    bl_idname = "cm_audio.stop_all_audio"
    bl_label = "Stop Audio"

    def execute(self, context):
        aud.Device().stopAll()
        return {"FINISHED"}
