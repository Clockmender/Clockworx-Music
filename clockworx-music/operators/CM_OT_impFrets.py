import bpy

class CM_OT_impFrets(bpy.types.Operator):
    bl_idname = "cm_audio.impfrets"
    bl_label = "Build Fretboard"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        cm = context.scene.cm_pg
        path = (str(bpy.utils.user_resource('SCRIPTS', "addons")) +
            '/clockworx-music/imports/frets.dae')
        bpy.ops.wm.collada_import(filepath=path)
        cm.message1 = ''
        src_obj = bpy.context.view_layer.objects.get('Base-Mesh')
        src_obj.name = 'Bridge'
        src_obj.select_set(state=True)
        src_obj.scale = (cm.bridge_len, cm.bridge_len, cm.bridge_len)
        bpy.context.view_layer.objects.active = src_obj
        bpy.ops.object.transform_apply(location = False, scale = True, rotation = False)
        src_obj.select_set(state=False)
        scl = cm.scale_f
        xLoc = src_obj.location.x
        fret = cm.bridge_len

        fret_name = ['NUT','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12',
            'F13','F14','F15','F16','F17','F18','F19','F20','F21','F22','F23','F24']

        for i in range (0,25):
            bpy.ops.wm.collada_import(filepath=path)
            new_obj = bpy.context.view_layer.objects.get('Base-Mesh')
            new_obj.name = fret_name[i]
            new_obj.location.x = fret
            new_obj.scale.y = scl
            new_obj.select_set(state=True)
            bpy.context.view_layer.objects.active = new_obj
            bpy.ops.object.transform_apply(location = False, scale = True, rotation = False)
            new_obj.select_set(state=False)
            fret = fret * (0.5**(1/12))
            scl = (cm.scale_f + (((cm.bridge_len - fret) / cm.bridge_len)
                * (1 - cm.scale_f)))
        cm.message1 = "Fretboard Built in Active Collection"
        return {"FINISHED"}
