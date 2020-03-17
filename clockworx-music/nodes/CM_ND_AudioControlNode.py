import bpy
from bpy.props import (
   IntProperty,
   StringProperty,
)
from ..cm_functions import view_lock

class CM_ND_AudioControlNode(bpy.types.Node):
    bl_idname = "cm_audio.control_node"
    bl_label = "Clockworx Music Control"
    bl_icon = "SPEAKER"

    bpm : IntProperty(name="BPM", default=60)
    time_sig_num: IntProperty(name="Time Sig N", default=4)
    time_sig_den: IntProperty(name="Time Sig D", default=4)
    note_den : IntProperty(name="Note Denom.",min=1,default=16,max=64)
    message : StringProperty(name="Message")
    samples : IntProperty(name="Samples", default=44100, min=6000, max=192000)

    def draw_buttons(self, context, layout):
        cm_pg = context.scene.cm_pg
        layout.context_pointer_set("audionode", self)
        layout.operator("cm_audio.execute_start", icon="PLAY")
        layout.operator("cm_audio.execute_stop", icon="SNAP_FACE")
        layout.label(text="CM Constants")
        layout.prop(self, "bpm")
        layout.prop(self, "time_sig_num")
        layout.prop(self, "time_sig_den")
        layout.prop(self, "samples")
        layout.prop(self, "note_den")
        layout.operator("cm_audio.set_constants", icon="PLAY_SOUND")
        layout.label(text="Other CM Parameters")
        layout.prop(cm_pg, "offset")
        row = layout.row()
        row.prop(cm_pg, "sound_channels")
        row.prop(cm_pg, "mid_c")
        if self.message != "":
            layout.prop(self, "message", text="")

    def execute(self):
        view_lock()
