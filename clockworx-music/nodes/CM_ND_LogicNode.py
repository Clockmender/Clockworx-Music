import bpy
from bpy.types import NodeSocketBool
from .._base.base_node import CM_ND_BaseNode
from bpy.props import EnumProperty
from ..cm_functions import connected_node_output

class CM_ND_LogicNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.logic_node"
    bl_label = "Logic"
    bl_icon = "SPEAKER"

    operation : EnumProperty(
        items=(
            ("and", "And", "Logical And"),
            ("or", "Or", "Logical Or"),
            ("nand", "Nand", "Logical Not And"),
            ("nor", "Nor", "Logical Not Or"),
        ),
        name="Operation",
        default="and",
        description="Logic Opertion",
    )

    def init(self, context):
        super().init(context)
        self.inputs.new("NodeSocketBool", "Bool 1")
        self.inputs.new("NodeSocketBool", "Bool 2")
        self.outputs.new("NodeSocketBool", "Output (Bool)")

    def draw_buttons(self, context, layout):
        layout.prop(self, "operation", text="", icon="RESTRICT_SELECT_OFF")

    def execute(self):
        input_1 = connected_node_output(self, 0)
        input_2 = connected_node_output(self, 1)
        if input_1 is None or input_2 is None:
            return None
        else:
            input_1 = input_1["bool"]
            input_2 = input_2["bool"]
            if self.operation == "and":
                return {"bool": (input_1 and input_2)}
            elif self.operation == "or":
                return {"bool": (input_1 or input_2)}
            elif self.operation == "nand":
                return {"bool": (not input_1 and not input_2)}
            elif self.operation == "nor":
                return {"bool": (not input_1 or not input_2)}

    def output(self):
        return self.execute()
