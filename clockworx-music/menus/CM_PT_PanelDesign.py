import bpy
from bpy.types import Panel

class CM_PT_PanelDesign(Panel):
    bl_idname = "CM_PT_Menu_Node"
    bl_label = "CMN Operations"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "CMN"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "cm_AudioNodeTree"

    def draw(self, context):
        layout = self.layout
        cm_pg = context.scene.cm_pg
        box = layout.box()
        box.label(text="Execution on Frame Change")
        row = box.row()
        row.operator("cm_audio.execute_start", text="Start Exec", icon="PLAY")
        row.operator("cm_audio.execute_stop", text="Stop Exec", icon="SNAP_FACE")
        box = layout.box()
        box.label(text="Execution by Time Interval")
        row = box.row()
        row.operator("cm_audio.midi_start", text="Start Midi", icon="PLAY")
        row.operator("cm_audio.midi_stop", text="Stop Midi", icon="SNAP_FACE")
        row = box.row()
        row.prop(cm_pg, "midi_poll_time")
        row.prop(cm_pg, "midi_debug")

        layout.label(text="CM Constants")
        layout.prop(cm_pg, "bpm")
        layout.prop(cm_pg, "time_sig_num")
        layout.prop(cm_pg, "time_sig_den")
        layout.prop(cm_pg, "samples")
        row = layout.row()
        split = row.split(factor=0.70, align=True)
        split.label(text="Note Denominator")
        split.prop(cm_pg, "note_den", text="")
        layout.operator("cm_audio.set_constants_menu", icon="PLAY_SOUND")
        layout.label(text="Other CM Parameters")
        layout.prop(cm_pg, "offset")
        row = layout.row()
        row.prop(cm_pg, "sound_channels")
        row.prop(cm_pg, "mid_c")
        layout.prop(cm_pg, "message")
