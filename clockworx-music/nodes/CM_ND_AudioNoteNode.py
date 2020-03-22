import bpy
import aud
from bpy.props import (
   BoolProperty,
   FloatProperty,
   StringProperty,
)

class CM_ND_AudioNoteNode(bpy.types.Node):
    bl_idname = "cm_audio.note_node"
    bl_label = "Note Input Data"
    bl_icon = "SPEAKER"

    note_params : StringProperty(name="Params", default="")
    note_name : StringProperty(name="Note", default="")
    note_freq : FloatProperty(name="Frequency", default=0.0, min=0, max=32000)
    note_vol : FloatProperty(name="Volume", default=1, min=0, max=10)
    note_del : FloatProperty(name="Delay (B)", default=0, min=0)
    note_dur : FloatProperty(name="Length (B)", default=1, min=0.001)
    note_rev: BoolProperty(name="Reverse", default=False)

    def init(self, context):
        self.outputs.new("cm_socket.sound", "Note Data")

    def draw_buttons(self, context, layout):
        #layout.prop(self, "note_name")
        #layout.prop(self, "note_freq")
        #layout.prop(self, "note_vol")
        #layout.prop(self, "note_del")
        #layout.prop(self, "note_dur")
        #layout.prop(self, "note_rev")
        layout.label(text="Note,Volume,Length,Reverse")
        layout.prop(self, "note_params")

    def get_sound(self):
        return self.note_params

    def info(self, context):
        return self.note_params

    def execute(self):
        return self.note_params
