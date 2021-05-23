import bpy
from .._base.base_node import CM_ND_BaseNode

from bpy.props import StringProperty
from bpy.types import (
    NodeSocketFloat,
    NodeSocketBool,
    NodeSocketString,
)
from ..cm_functions import get_socket_values, connected_node_output

class CM_ND_AudioNoteNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.note_node"
    bl_label = "Note Data: Raw"
    bl_icon = "SPEAKER"

    def init(self, context):
        super().init(context)
        self.outputs.new("cm_socket.note", "Note Data")
        self.inputs.new("NodeSocketString", "Note Name")
        self.inputs.new("NodeSocketFloat", "Frequency")
        self.inputs.new("NodeSocketFloat", "volume")
        self.inputs.new("NodeSocketFloat", "Length (B)")
        self.inputs.new("NodeSocketBool", "Reverse")

    def get_sound(self):
        sockets = self.inputs.keys()
        input_values = get_socket_values(self, sockets, self.inputs)

        if connected_node_output(self, 0) is not None:
            note_name = connected_node_output(self, 0)["text"]
        else:
            note_name = input_values[0]

        if connected_node_output(self, 1) is not None:
            note_freq = connected_node_output(self, 1)["float"]
        else:
            note_freq = input_values[1]

        if connected_node_output(self, 2) is not None:
            note_vol = connected_node_output(self, 2)["float"]
        else:
            note_vol = input_values[2]

        if connected_node_output(self, 3) is not None:
            note_dur = connected_node_output(self, 3)["float"]
        else:
            note_dur = input_values[3]

        if connected_node_output(self, 4) is not None:
            note_rev = connected_node_output(self, 4)["bool"]
        else:
            note_rev = input_values[4]

        output = {}
        output["note_name"] = note_name
        output["note_freq"] = note_freq
        output["note_vol"] = note_vol
        output["note_dur"] = note_dur
        output["note_rev"] = note_rev
        return output

    def output(self):
        return self.get_sound()
