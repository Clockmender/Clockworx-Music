import bpy
from .._base.base_node import CM_ND_BaseNode

from bpy.props import (
   BoolProperty,
   FloatProperty,
   StringProperty,
)

class CM_ND_AudioNoteNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.note_node"
    bl_label = "Note Data: Raw"
    bl_icon = "SPEAKER"

    note_name : StringProperty(name="Note", default="")
    note_freq : FloatProperty(name="Frequency", default=0.0, min=0, max=32000)
    note_vol : FloatProperty(name="Volume", default=1, min=0, max=10)
    note_dur : FloatProperty(name="Length (B)", default=1, min=0.001)
    note_rev: BoolProperty(name="Reverse", default=False)

    def init(self, context):
        super().init(context)
        self.outputs.new("cm_socket.note", "Note Data")

    def draw_buttons(self, context, layout):
        layout.prop(self, "note_name")
        layout.prop(self, "note_freq")
        layout.prop(self, "note_vol")
        layout.prop(self, "note_dur")
        layout.prop(self, "note_rev")

    def output(self):
        output = {}
        output["note_name"] = self.note_name
        output["note_freq"] = self.note_freq
        output["note_vol"] = self.note_vol
        output["note_dur"] = self.note_dur
        output["note_rev"] = self.note_rev
        return output
