import bpy
from bpy.types import NodeSocketFloat
from .._base.base_node import CM_ND_BaseNode
from bpy.props import IntProperty, BoolProperty
from ..cm_functions import get_socket_values, connected_node_output

class CM_ND_FrameSeqNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.frame_seq_node"
    bl_label = "Step Sequence"
    bl_icon = "SPEAKER"

    last_step : IntProperty(default=0)
    step_idx : BoolProperty(name="Steps/Index", default=True)

    def init(self, context):
        super().init(context)
        self.inputs.new("NodeSocketInt", "Start Frame")
        self.inputs.new("NodeSocketInt", "Steps")
        self.inputs.new("NodeSocketInt", "Step Value")
        self.outputs.new("NodeSocketFloat", "Output (Float)")

    def draw_buttons(self, context, layout):
        layout.prop(self, "step_idx")

    def execute(self):
        curr_frm = bpy.context.scene.frame_current
        sockets = self.inputs.keys()
        start_frm = connected_node_output(self, 0)
        if start_frm == None:
            start_frm = get_socket_values(self, sockets, self.inputs)[0]
        else:
            start_frm = start_frm["int"]
        if start_frm < bpy.context.scene.frame_start:
            return None

        steps = connected_node_output(self, 1)
        if steps == None:
            steps = get_socket_values(self, sockets, self.inputs)[1]
        else:
            steps = steps["int"]
        step_v = connected_node_output(self, 1)
        if step_v == None:
            step_v = get_socket_values(self, sockets, self.inputs)[2]
        else:
            step_v = step_v["int"]
        max_frm = curr_frm + (steps * step_v)

        if curr_frm < start_frm:
            out_frm = 0
            self.last_step = 0
        elif curr_frm == start_frm:
            out_frm = 0
            self.last_step = start_frm
        elif curr_frm == self.last_step + step_v:
            if curr_frm <= start_frm + (steps * step_v):
                if self.step_idx:
                    out_frm = (self.last_step - start_frm) + step_v
                else:
                    out_frm = int((self.last_step - start_frm) + (step_v / steps))
                self.last_step = self.last_step + step_v
            else:
                if self.step_idx:
                    out_frm = self.last_step - start_frm
                else:
                    out_frm = int((self.last_step - start_frm) / step_v)
        else:
            if self.step_idx:
                out_frm = self.last_step - start_frm
            else:
                out_frm = int((self.last_step - start_frm) / step_v)

        return {"float": float(out_frm)}

    def output(self):
        return self.execute()
