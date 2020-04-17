import bpy
from bpy.types import NodeSocketFloat, NodeSocketInt, NodeSocketBool
from .._base.base_node import CM_ND_BaseNode
from bpy.props import EnumProperty
from ..cm_functions import get_socket_values, connected_node_output

class CM_ND_CompareNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.compare_node"
    bl_label = "Compare"
    bl_icon = "SPEAKER"

    operation : EnumProperty(
        items=(
            ("==", "==", "Equal"),
            ("!=", "!=", "Not Equal"),
            (">", ">", "Greater Than"),
            ("<", "<", "Less Than"),
            (">=", ">=", "Greater Than or Equal"),
            ("<=", "<=", "Less Than or Equal"),
        ),
        name="Operation",
        default="==",
        description="Compare Opertion",
    )

    def init(self, context):
        super().init(context)
        self.inputs.new("NodeSocketInt", "Integer 1")
        self.inputs.new("NodeSocketInt", "Integer 2")
        self.inputs.new("NodeSocketFloat", "Float 1")
        self.inputs.new("NodeSocketFloat", "Float 2")
        self.outputs.new("NodeSocketBool", "Output (Bool)")

    def draw_buttons(self, context, layout):
        layout.prop(self, "operation", text="", icon="RESTRICT_SELECT_OFF")

    def execute(self):
        def maths(input_1, input_2):
            if self.operation == "==":
                return float(input_1) == float(input_2)
            elif self.operation == "!=":
                return float(input_1) != float(input_2)
            elif self.operation == ">":
                return float(input_1) > float(input_2)
            elif self.operation == "<":
                return float(input_1) < float(input_2)
            elif self.operation == ">=":
                return float(input_1) >= float(input_2)
            elif self.operation == "<=":
                return float(input_1) <= float(input_2)

        sockets = self.inputs.keys()

        int_v1 = connected_node_output(self, 0)
        if int_v1 is not None:
            int_v1 = int_v1["int"]
            int_v2 = connected_node_output(self, 1)
            if int_v2 is None:
                int_v2 = get_socket_values(self, sockets, self.inputs)[1]
            output = maths(int_v1, int_v2)
            return {"bool": output}

        flt_v1 = connected_node_output(self, 2)
        if flt_v1 is not None:
            flt_v1 = flt_v1["float"]
            flt_v2 = connected_node_output(self, 3)
            if flt_v2 is None:
                flt_v2 = get_socket_values(self, sockets, self.inputs)[3]
            output = maths(flt_v1, flt_v2)
            return {"bool": output}

        return None

    def output(self):
        return self.execute()
