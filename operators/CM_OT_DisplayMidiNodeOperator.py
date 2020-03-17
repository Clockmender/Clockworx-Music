import bpy

class CM_OT_DisplayMidiNodeOperator(bpy.types.Operator):
    bl_idname = "cm_audio.display_midi"
    bl_label = "Display Info"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        context.audionode.get_midi()
        return {"FINISHED"}
