import bpy

class CM_OT_UnlockView(bpy.types.Operator):
    bl_idname = "cm_audio.unlock_view"
    bl_label = "Unlock 3D View"

    @classmethod
    def poll(cls, context):
        test = True
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                test = area.spaces[0].region_3d.lock_rotation
        return test

    def execute(self, context):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].region_3d.lock_rotation = False
        return {"FINISHED"}
