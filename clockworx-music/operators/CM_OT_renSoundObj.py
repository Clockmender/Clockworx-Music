import bpy

class CM_OT_renSoundObj(bpy.types.Operator):
    bl_idname = "cm_audio.rename_sound_objs"
    bl_label = "Rename Objects to Controls"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        cm = context.scene.cm_pg
        if cm.col_name is not "" and cm.suffix_obj is not "" and cm.con_name is not None:
            if (
                cm.col_name is not None
                and cm.con_name is not None
                ):
                i_objs = cm.con_name.objects
                o_objs = cm.col_name.objects
                if len(i_objs) == len(o_objs):
                    for i in range(len(i_objs)):
                        part = i_objs[i].name.split("_")[0]
                        name = f"{part}_{cm.suffix_obj}"
                        o_objs[i].name = name
                cm.message1 = ("Processed "
                    + str(len(cm.col_name.objects))
                    + " Objects")
            else:
                cm.message1 = "Collection Does Not Exist"
                return
        else:
            cm.message1 = "Enter Collection/Siffix"
        return {"FINISHED"}
