import bpy
import aud

class CM_OT_PlayAudioNodeOperator(bpy.types.Operator):
    bl_idname = "cm_audio.play_audio"
    bl_label = "Play Audio"

    @classmethod
    def poll(cls, context):
        node = context.node
        if hasattr(node, "get_sound"):
            return node.get_sound() != None
        else:
            return False

    def execute(self, context):
        sound = context.node.get_sound()
        if sound != None:
            aud.Device().play(sound)
        return {"FINISHED"}
