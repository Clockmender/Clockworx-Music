import bpy
from ..cm_functions import (
    view_lock,
    start_piano,
    )

class CM_OT_EvaluatePiano(bpy.types.Operator):
    bl_idname = "cm_audio.evaluate_piano"
    bl_label = "Play Piano Roll"
    bl_description = "Plays the Notes written to Pointer Object"

    def execute(self, context):
        view_lock()
        bpy.app.handlers.frame_change_post.append(start_piano)
        bpy.ops.screen.animation_play(reverse=False, sync=False)
        return {"FINISHED"}
