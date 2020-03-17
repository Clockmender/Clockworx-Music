import bpy
from ..cm_functions import start_clock

class CM_OT_ExecuteStartOperator(bpy.types.Operator):
    bl_idname = "cm_audio.execute_start"
    bl_label = "CM Execute Start"

    @classmethod
    def poll(cls, context):
        return start_clock not in bpy.app.handlers.frame_change_post

    def execute(self, context):
        cm = context.scene.cm_pg
        if start_clock not in bpy.app.handlers.frame_change_post:
            bpy.app.handlers.frame_change_post.append(start_clock)
        #if start_clock not in bpy.app.handlers.render_init:
        #    bpy.app.handlers.render_init.append(start_clock)
        return {"FINISHED"}
