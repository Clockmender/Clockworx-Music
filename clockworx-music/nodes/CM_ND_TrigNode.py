import bpy
from bpy.types import NodeSocketFloat
from .._base.base_node import CM_ND_BaseNode
from bpy.props import FloatProperty, EnumProperty
from ..cm_functions import connected_node_output
from math import sin, cos, tan, asin, acos, atan, pi

class CM_ND_TrigNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.trig_node"
    bl_label = "Trigonometry"
    bl_icon = "SPEAKER"

    operation : EnumProperty(
        items=(
            ("sin", "Sine", "Sine Input"),
            ("cos", "Cosine", "Cosine Input"),
            ("tan", "Tangent", "Tangent Input"),
            ("asin", "ArcSine", "ArcSine Input by Factor"),
            ("acos", "ArcCosine", "ArcCosine Input by Factor"),
            ("atan", "ArcTangent", "ArcTangent Input by Factor"),
        ),
        name="Operation",
        default="sin",
        description="Maths Opertion",
    )
    max_tan : FloatProperty(name="Max Tangent", default=1000, min=10)

    def init(self, context):
        super().init(context)
        self.inputs.new("NodeSocketFloat", "Input Float")
        self.outputs.new("NodeSocketFloat", "Output (Float)")

    def draw_buttons(self, context, layout):
        layout.prop(self, "operation")
        layout.prop(self, "max_tan")

    def execute(self):
        flt_v = connected_node_output(self, 0)
        if flt_v is not None:
            if "float" in flt_v.keys():
                flt_v = flt_v["float"]
                if self.operation == "sin":
                    return {"float": round(sin(flt_v * pi / 180),5)}
                elif self.operation == "cos":
                    return {"float": round(cos(flt_v * pi / 180),5)}
                elif self.operation == "tan":
                    out = round(tan(flt_v * pi / 180))
                    if out >= self.max_tan:
                        out = self.max_tan
                    return {"float": out}
                elif self.operation == "asin":
                    if flt_v <= 1 and flt_v >= -1:
                        return {"float": round(asin(flt_v) * 180 / pi, 5)}
                elif self.operation == "acos":
                    if flt_v <= 1 and flt_v >= -1:
                        return {"float": round(acos(flt_v) * 180 / pi, 5)}
                elif self.operation == "atan":
                    if flt_v <= self.max_tan and flt_v >= -self.max_tan:
                        return {"float": round(atan(flt_v) * 180 / pi, 5)}
                else:
                    return 0

        return 0

    def output(self):
        return self.execute()
