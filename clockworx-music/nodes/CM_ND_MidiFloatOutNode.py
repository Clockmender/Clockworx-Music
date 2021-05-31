import bpy
from .._base.base_node import CM_ND_BaseNode

from bpy.props import (
    IntProperty,
    EnumProperty,
    )
from ..cm_functions import (
    connected_node_midi,
    )

class CM_ND_MidiFloatOutNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.midi_float_out_node"
    bl_label = "MIDI Data Float"

    midi_type: EnumProperty(
        items=(
            ("key", "Keys", "Use MIDI Keys"),
            ("con", "Controls", "Use MIDI Controls"),
        ),
        name="MIDI",
        default="key",
        description="MIDI Type",
    )
    con_px : IntProperty(name="Control", default=32, min=-1, max=127)

    def draw_buttons(self, context, layout):
        box = layout.box()
        row = box.row()
        row.prop(self, "midi_type")
        row = box.row()
        row.prop(self, "con_px")

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.midi", "MIDI Data")
        self.outputs.new("NodeSocketFloat", "Float")

    def get_midi(self):
        sockets = self.inputs.keys()
        buffer_in = connected_node_midi(self, 0)
        if buffer_in is not None:
            if self.midi_type == "con":
                num = 1
            else:
                num = 0
            if isinstance(buffer_in[0], list):
                value = buffer_in[num][self.con_px] / 127
            else:
                value = buffer_in[num]
            return {"float": value}
        else:
            return None

    def output(self):
        output = self.get_midi()
        return output

    def execute(self):
        output = self.get_midi()
        return output
