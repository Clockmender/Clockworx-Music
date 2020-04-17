import bpy
import aud

class CM_OT_StopAudioNodeOperator(bpy.types.Operator):
    bl_idname = "cm_audio.stop_audio"
    bl_label = "Stop Audio"

    @classmethod
    def poll(cls, context):
        node = context.node
        if hasattr(node, "get_sound"):
            return True
        else:
            return False

    def execute(self, context):
        sound = context.node.get_sound()
        if sound != None:
            aud.Device().stopAll()
        return {"FINISHED"}
