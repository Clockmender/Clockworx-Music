import bpy
from bpy.types import NodeSocketBool
from .._base.base_node import CM_ND_BaseNode
from bpy.props import EnumProperty
from ..cm_functions import connected_node_output

class CM_ND_ConditionNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.condition_node"
    bl_label = "Condition"
    bl_icon = "SPEAKER"

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.generic", "Input 1")
        self.inputs.new("NodeSocketBool", "Bool")
        self.inputs.new("cm_socket.generic", "Input 2")
        self.outputs.new("cm_socket.generic", "Output")

    def execute(self):
        input_1 = connected_node_output(self, 0)
        input_2 = connected_node_output(self, 2)
        switch = connected_node_output(self, 1)

        if all([input_1 is not None, input_2 is not None, switch is not None]):
            switch = switch["bool"]
            if switch:
                return input_1
            else:
                return input_2

        return None

    def output(self):
        return self.execute()
