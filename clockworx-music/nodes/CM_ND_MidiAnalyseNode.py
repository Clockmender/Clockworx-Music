import bpy
from .._base.base_node import CM_ND_BaseNode

from bpy.props import (
    IntProperty,
    StringProperty,
    )

class CM_ND_MidiAnalyseNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.midi_analyse_node"
    bl_label = "MIDI Analyser"
    bl_icon = "SPEAKER"

    midi_file_name : StringProperty(subtype="FILE_PATH", name="Midi CSV file", default="//")
    midi_channel : IntProperty(name="Channel", default=2, min=2)
    bpm : IntProperty(name="BPM", default=0)
    tempo : IntProperty(name="1st Tempo", default=0)
    pulse : IntProperty(name="Pulse", default=0)
    time_sig : StringProperty(name="Time Sig", default="")
    track_name : StringProperty(name="Track Name", default="")
    tracks : StringProperty(name="Tracks", default="")


    def init(self, context):
        super().init(context)
        self.outputs.new("cm_socket.generic", "File Info")

    def draw_buttons(self, context, layout):
        cm_pg = context.scene.cm_pg
        layout.context_pointer_set("audionode", self)
        layout.prop(self, "midi_file_name")
        layout.prop(self, "midi_channel")
        layout.prop(self, "track_name")
        layout.prop(self, "bpm")
        layout.prop(self, "pulse")
        layout.prop(self, "tempo")
        layout.prop(self, "time_sig")
        layout.prop(cm_pg, "channels")
        layout.prop(self, "tracks")
        layout.operator("cm_audio.analyse_midi", text="Analyse File")

    def output(self):
        cm = bpy.context.scene.cm_pg
        return cm.data_dict
