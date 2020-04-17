import bpy

class CM_OT_DisplayAudioNodeOperator(bpy.types.Operator):
    bl_idname = "cm_audio.display_audio"
    bl_label = "Display Info"

    @classmethod
    def poll(cls, context):
        node = context.node
        if hasattr(node, "info"):
            return True
        else:
            return False

    def execute(self, context):
        context.node.info(context)
        return {"FINISHED"}
