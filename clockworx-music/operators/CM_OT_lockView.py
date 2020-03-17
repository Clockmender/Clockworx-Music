import bpy
from ..cm_functions import view_lock

class CM_OT_lockView(bpy.types.Operator):
    bl_idname = "cm_audio.lock_view"
    bl_label = "Lock 3D View"

    @classmethod
    def poll(cls, context):
        test = True
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                test = area.spaces[0].region_3d.lock_rotation
        return not test

    def execute(self, context):
        view_lock()
        return {"FINISHED"}
