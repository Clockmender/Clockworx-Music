import bpy
from .._base.base_node import CM_ND_BaseNode

from bpy.props import (
    BoolProperty,
    IntProperty,
    FloatProperty,
    )
from ..cm_functions import (
    connected_node_midi,
    )


class CM_ND_MidiNoteNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.midi_note_node"
    bl_label = "MIDI Key Info"
    bl_icon = "SPEAKER"

    midi_type : IntProperty(name="Type", default=0)
    midi_id : IntProperty(name="ID", default=0)
    midi_value : FloatProperty(name="Value", default=0.0)

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.midi", "Midi Data")
        self.outputs.new("cm_socket.midi", "Key Data")

    def draw_buttons(self, context, layout):
        layout.prop(self, "midi_type")
        layout.prop(self, "midi_id")
        layout.prop(self, "midi_value")
        layout.context_pointer_set("audionode", self)
        layout.operator("cm_audio.display_midi", text="Update Display")

    def get_midi(self):
        cm = bpy.context.scene.cm_pg
        buffer_in = connected_node_midi(self, 0)
        if buffer_in is not None:
            buffer1 = buffer_in[0]
            if len(buffer_in[0]) > 0:
                self.midi_type = buffer1[0][0]
                self.midi_id = buffer1[0][1]
                self.midi_value = buffer1[0][2] / 127
                output = ([cm.midi_buffer["buffer1"][0][0],
                    cm.midi_buffer["buffer1"][0][1],
                    cm.midi_buffer["buffer1"][0][2] / 127
                    ])
                return output
            else:
                return None
        else:
            return None
