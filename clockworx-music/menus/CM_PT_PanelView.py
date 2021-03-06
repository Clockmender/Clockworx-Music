import bpy
from bpy.types import Panel

class CM_PT_PanelView(Panel):
    bl_idname = "CM_PT_Menu_View"
    bl_label = "CMN Operations"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "CMN"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        cm_pg = context.scene.cm_pg
        layout = self.layout
        box = layout.box()
        box.label(text="Imports")
        box.operator("cm_audio.impkeyb88", icon="FILE_NEW")
        box.operator("cm_audio.impkeyb61", icon="FILE_NEW")
        box.operator("cm_audio.imp_daw_objs", icon="FILE_NEW")
        box.separator()
        box.prop(cm_pg, "bridge_len")
        box.prop(cm_pg, "scale_f")
        box.operator("cm_audio.impfrets", icon="FILE_NEW")
        box = layout.box()
        box.label(text="Utilities")
        row = box.row()
        split = row.split(factor=0.4, align=True)
        split.label(text="Obj Collection")
        split.prop(cm_pg, "col_name", text="")
        row = box.row()
        split = row.split(factor=0.4, align=True)
        split.label(text="Suffix")
        split.prop(cm_pg, "suffix_obj", text="")
        box.operator("cm_audio.rename_objs", icon = "PREFERENCES")

        row = box.row()
        split = row.split(factor=0.4, align=True)
        split.label(text="Con Collection")
        split.prop(cm_pg, "con_name", text="")
        box.operator("cm_audio.rename_sound_objs", icon = "PREFERENCES")

        row = layout.row()
        layout.label(text=cm_pg.message, icon="INFO")
        row = layout.row()
        row.operator("cm_audio.lock_view", icon="URL", text="")
        row.label(text="View Lock (Pianoroll)")
        row.operator("cm_audio.unlock_view", icon="WORLD", text="")

        box = layout.box()
        box.label(text="Trig Wave Generator")
        row = box.row()
        split = row.split(factor=0.5, align=True)
        split.prop(cm_pg, "trig_type")
        split.prop(cm_pg, "trig_cycles")
        row = box.row()
        split = row.split(factor=0.5, align=True)
        split.prop(cm_pg, "trig_amp")
        split.prop(cm_pg, "trig_len")
        row = box.row()
        split = row.split(factor=0.5, align=True)
        split.prop(cm_pg, "trig_obj", text="")
        split.prop(cm_pg, "trig_del")
        row = box.row()
        split = row.split(factor=0.5, align=True)
        split.prop(cm_pg, "trig_res")
        split.prop(cm_pg, "trig_tanmax")
        row = box.row()
        row.prop(cm_pg, "trig_off")
        box.operator("cm_audio.wave_generator", icon="SEQ_LUMA_WAVEFORM")
