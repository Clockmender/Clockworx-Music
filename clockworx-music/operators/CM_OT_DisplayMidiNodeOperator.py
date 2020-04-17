import bpy

class CM_OT_DisplayMidiNodeOperator(bpy.types.Operator):
    bl_idname = "cm_audio.display_midi"
    bl_label = "Display Info"

    @classmethod
    def poll(cls, context):
        node = context.node
        if hasattr(node, "get_midi"):
            return True
        else:
            return False

    def execute(self, context):
        context.node.get_midi()
        return {"FINISHED"}
