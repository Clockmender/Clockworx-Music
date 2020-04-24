import bpy
from bpy.types import NodeSocketFloat, NodeSocketInt
from bpy.props import BoolProperty
from .._base.base_node import CM_ND_BaseNode
from ..cm_functions import get_socket_values, connected_node_output

class CM_ND_TriggerNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.trigger_node"
    bl_label = "Periodic Trigger"
    bl_icon = "SPEAKER"

    pulse : BoolProperty(name="Pulse/Switch", default=True)

    def init(self, context):
        super().init(context)
        self.inputs.new("NodeSocketInt", "Cycle Length")
        self.inputs.new("NodeSocketInt", "Phase")
        self.outputs.new("NodeSocketBool", "Output (Bool)")

    def draw_buttons(self, context, layout):
        layout.prop(self, "pulse")

    def execute(self):
        sockets = self.inputs.keys()
        cyc_len = connected_node_output(self, 0)
        if cyc_len is not None:
            cyc_len = cyc_len["float"]
        else:
            cyc_len = get_socket_values(self, sockets, self.inputs)[0]

        phase = connected_node_output(self, 1)
        if phase is not None:
            phase = phase["float"]
        else:
            phase = get_socket_values(self, sockets, self.inputs)[1]

        if cyc_len < 2 or phase < 0 or phase > cyc_len:
            return None

        if self.pulse:
            return {"bool": bpy.context.scene.frame_current % cyc_len == phase}
        else:
            out = ((bpy.context.scene.frame_current - phase) // cyc_len) % 2 == 0
            return {"bool": out}

    def output(self):
        return self.execute()
