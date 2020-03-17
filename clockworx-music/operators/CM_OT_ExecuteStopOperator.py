import bpy
from ..cm_functions import start_clock

class CM_OT_ExecuteStopOperator(bpy.types.Operator):
    bl_idname = "cm_audio.execute_stop"
    bl_label = "CM Execute Stop"

    @classmethod
    def poll(cls, context):
        return start_clock in bpy.app.handlers.frame_change_post

    def execute(self, context):
        cm = context.scene.cm_pg
        if start_clock in bpy.app.handlers.frame_change_post:
            bpy.app.handlers.frame_change_post.remove(start_clock)
        #if start_clock in bpy.app.handlers.render_init:
        #    bpy.app.handlers.render_init.append(start_clock)
        return {"FINISHED"}
