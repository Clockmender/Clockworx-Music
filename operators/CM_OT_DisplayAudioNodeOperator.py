import bpy

class CM_OT_DisplayAudioNodeOperator(bpy.types.Operator):
    bl_idname = "cm_audio.display_audio"
    bl_label = "Display Info"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        context.audionode.info(context)
        return {"FINISHED"}
