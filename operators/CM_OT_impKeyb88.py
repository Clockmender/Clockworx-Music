import bpy


class CM_OT_impKeyb88(bpy.types.Operator):
    bl_idname = "cm_audio.impkeyb88"
    bl_label = "Import 88 key Keyboard"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self,context):
        cm = context.scene.cm_pg
        path = (str(bpy.utils.user_resource('SCRIPTS', "addons"))
            + '/clockworx-music/imports/88keys.dae')
        bpy.ops.wm.collada_import(filepath=path)
        cm.message1 = "Import 88 Key Board Completed"
        return {"FINISHED"}
