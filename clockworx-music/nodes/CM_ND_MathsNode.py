import bpy
from bpy.types import NodeSocketFloat, NodeSocketInt
from .._base.base_node import CM_ND_BaseNode
from bpy.props import EnumProperty
from ..cm_functions import get_socket_values, connected_node_output

class CM_ND_MathsNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.maths_node"
    bl_label = "Maths"
    bl_icon = "SPEAKER"

    operation : EnumProperty(
        items=(
            ("+", "+", "Add Factor"),
            ("-", "-", "Subtract Factor"),
            ("*", "*", "Multiply by Factor"),
            ("/", "/", "Divide by Factor"),
            ("//", "//", "Floor Division by Factor"),
            ("%", "%", "Modulus by Factor"),
            ("**", "**", "Exponent by Factor"),
        ),
        name="Operation",
        default="+",
        description="Maths Opertion",
    )

    def init(self, context):
        super().init(context)
        self.inputs.new("NodeSocketInt", "Input Int")
        self.inputs.new("NodeSocketFloat", "Input Float")
        self.inputs.new("NodeSocketFloat", "Factor")
        self.outputs.new("NodeSocketFloat", "Output (Float)")

    def draw_buttons(self, context, layout):
        layout.prop(self, "operation", text="", icon="RESTRICT_SELECT_OFF")

    def execute(self):
        def maths(input, factor):
            if self.operation == "+":
                return float(input) + factor
            elif self.operation == "-":
                return float(input) - factor
            elif self.operation == "*":
                return float(input) * factor
            elif self.operation == "/":
                return float(input) / factor
            elif self.operation == "//":
                return float(input) // factor
            elif self.operation == "%":
                return float(input) % factor
            elif self.operation == "**":
                return float(input) ** factor

        sockets = self.inputs.keys()

        factor = connected_node_output(self, 2)
        if factor is not None:
            factor = factor["float"]
        else:
            factor = get_socket_values(self, sockets, self.inputs)[2]

        int_v = connected_node_output(self, 0)
        if int_v is not None:
            if "int" in int_v.keys():
                int_v = int_v["int"]
                output = maths(int_v, factor)
                return {"float": output}
            else:
                return None

        flt_v = connected_node_output(self, 1)
        if flt_v is not None:
            if "float" in flt_v.keys():
                flt_v = flt_v["float"]
                output = maths(flt_v, factor)
                return {"float": output}
            else:
                return None

    def output(self):
        return self.execute()
