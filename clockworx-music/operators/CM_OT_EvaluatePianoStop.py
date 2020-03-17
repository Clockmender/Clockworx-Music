import bpy
from ..cm_functions import (
    view_lock,
    start_piano,
    )

class CM_OT_EvaluatePianoStop(bpy.types.Operator):
    bl_idname = "cm_audio.evaluate_piano_stop"
    bl_label = "Stop Piano Roll"
    bl_description = "Stops the Pianoroll Player"

    @classmethod
    def poll(cls, context):
        return start_piano in bpy.app.handlers.frame_change_post

    def execute(self, context):
        if start_piano in bpy.app.handlers.frame_change_post:
            bpy.app.handlers.frame_change_post.remove(start_piano)
            bpy.ops.screen.animation_cancel(restore_frame=True)
        return {"FINISHED"}
