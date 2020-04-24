import bpy

class CM_OT_renMesh(bpy.types.Operator):
    bl_idname = "cm_audio.rename_objs"
    bl_label = "Rename Objects to Suffix"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        cm = context.scene.cm_pg
        if cm.col_name is not "" and cm.suffix_obj is not "":
            if cm.col_name is not None:
                for o in cm.col_name.objects:
                    if "_" in o.name:
                        o.name = o.name.split("_")[0] + "_" + cm.suffix_obj
                    else:
                        o.name = o.name + "_" + cm.suffix_obj
                cm.message1 = ("Processed "
                    + str(len(cm.col_name.objects))
                    + " Objects")
            else:
                cm.message1 = "Collection Does Not Exist"
                return
        else:
            cm.message1 = "Enter Collection/Siffix"
        return {"FINISHED"}
