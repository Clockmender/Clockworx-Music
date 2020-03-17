import bpy


class CM_OT_impDawObjs(bpy.types.Operator):
    bl_idname = "cm_audio.imp_daw_objs"
    bl_label = "Import DAW Objects"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self,context):
        cm = context.scene.cm_pg
        path = (str(bpy.utils.user_resource('SCRIPTS', "addons"))
            + '/clockworx-music/imports/dawObjects.dae')
        bpy.ops.wm.collada_import(filepath=path)
        cm.message1 = "Import DAW Objects Completed"
        return {"FINISHED"}
