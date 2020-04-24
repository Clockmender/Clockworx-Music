import bpy
from bpy.types import NodeSocketFloat, NodeSocketBool
from .._base.base_node import CM_ND_BaseNode
from bpy.props import FloatProperty
from ..cm_functions import connected_node_output, get_socket_values

class CM_ND_InRangeNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.in_range_node"
    bl_label = "In Range"
    bl_icon = "SPEAKER"

    max : FloatProperty(name="Max Value", default=1)
    min : FloatProperty(name="Min Value", default=0)

    def init(self, context):
        super().init(context)
        self.inputs.new("NodeSocketFloat", "Input Float")
        self.outputs.new("NodeSocketBool", "Output (Bool)")

    def draw_buttons(self, context, layout):
        layout.prop(self, "min")
        layout.prop(self, "max")

    def execute(self):
        if self.min >= self.max:
            return None
        sockets = self.inputs.keys()
        flt_v = connected_node_output(self, 0)
        if flt_v is None:
            flt_v = get_socket_values(self, sockets, self.inputs)[0]
        if isinstance(flt_v, dict):
            if "float" in flt_v.keys():
                flt_v = flt_v["float"]
            else:
                return None

        if flt_v >= self.min and flt_v <= self.max:
            out_v = True
        else:
            out_v = False
        return {"bool": out_v}

    def output(self):
        return self.execute()
