import bpy
from bpy.types import NodeSocketColor
from .._base.base_node import CM_ND_BaseNode
from bpy.props import FloatProperty
from ..cm_functions import get_socket_values, connected_node_output

class CM_ND_ColorRGBANode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.colour_rgba_node"
    bl_label = "Colour RGBA"
    bl_icon = "SPEAKER"

    def init(self, context):
        super().init(context)
        self.inputs.new("NodeSocketFloat", "Red")
        self.inputs.new("NodeSocketFloat", "Green")
        self.inputs.new("NodeSocketFloat", "Blue")
        self.inputs.new("NodeSocketFloat", "Alpha")
        self.outputs.new("NodeSocketColor", "Colour")

    def output(self):
        sockets = self.inputs.keys()
        red_v = connected_node_output(self, 0)
        if red_v is None:
            red_v = get_socket_values(self, sockets, self.inputs)[0]
        else:
            red_v = red_v["float"]

        grn_v = connected_node_output(self, 1)
        if grn_v is None:
            grn_v = get_socket_values(self, sockets, self.inputs)[1]
        else:
            grn_v = grn_v["float"]

        blu_v = connected_node_output(self, 2)
        if blu_v is None:
            blu_v = get_socket_values(self, sockets, self.inputs)[2]
        else:
            blu_v = blu_v["float"]

        alp_v = connected_node_output(self, 3)
        if alp_v is None:
            alp_v = get_socket_values(self, sockets, self.inputs)[3]
        else:
            alp_v = alp_v["float"]

        inputs = [red_v, grn_v, blu_v, alp_v]
        for i in range(4):
            if inputs[i] < 0:
                inputs[i] = 0
            if inputs[i] > 1:
                inputs[i] = 1
        colour = ((inputs[0], inputs[1], inputs[2], inputs[3]))
        return {"colour": colour}
