import bpy
from bpy.types import NodeSocketFloat
from .._base.base_node import CM_ND_BaseNode
from bpy.props import FloatProperty
from ..cm_functions import connected_node_output

class CM_ND_MaxMinNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.max_min_node"
    bl_label = "Max Min"
    bl_icon = "SPEAKER"

    max : FloatProperty(name="Max Value", default=1)
    min : FloatProperty(name="Min Value", default=0)

    def init(self, context):
        super().init(context)
        self.inputs.new("NodeSocketFloat", "Input Float")
        self.outputs.new("NodeSocketFloat", "Output (Float)")

    def draw_buttons(self, context, layout):
        layout.prop(self, "min")
        layout.prop(self, "max")

    def execute(self):
        flt_v = connected_node_output(self, 0)
        if flt_v is not None:
            if "float" in flt_v.keys():
                flt_v = flt_v["float"]
                if flt_v >= self.min:
                    out_v = flt_v
                else:
                    out_v = self.min
                if flt_v <= self.max:
                    out_v = flt_v
                else:
                    out_v = self.max
                return {"float": out_v}
        return None

    def output(self):
        return self.execute()
