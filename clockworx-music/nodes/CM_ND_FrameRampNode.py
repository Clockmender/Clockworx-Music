import bpy
from bpy.types import NodeSocketFloat
from .._base.base_node import CM_ND_BaseNode
from bpy.props import IntProperty, FloatProperty
from ..cm_functions import get_socket_values, connected_node_output

class CM_ND_FrameRampNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.frame_ramp_node"
    bl_label = "Frame Ramp"
    bl_icon = "SPEAKER"

    start_frame : IntProperty(name="Start Frame", default=1)
    stop_frame : IntProperty(name="Stop Frame", default=10)
    last_inp : FloatProperty()

    def init(self, context):
        super().init(context)
        self.inputs.new("NodeSocketFloat", "Input Value")
        self.outputs.new("NodeSocketFloat", "Output (Float)")

    def draw_buttons(self, context, layout):
        layout.prop(self, "start_frame")
        layout.prop(self, "stop_frame")

    def execute(self):
        input = connected_node_output(self, 0)
        if input is not None:
            input = input["float"]
        else:
            sockets = self.inputs.keys()
            input = get_socket_values(self, sockets, self.inputs)[0]
        if self.stop_frame <= self.start_frame:
            return None

        frame_mod = bpy.context.scene.frame_current - self.start_frame
        if frame_mod >= bpy.context.scene.frame_start:
            if bpy.context.scene.frame_current <= self.stop_frame:
                inp_out = input * frame_mod
                self.last_inp = input
            else:
                inp_out = (self.stop_frame - self.start_frame) * self.last_inp
        else:
            inp_out = 0

        return {"float": inp_out}

    def output(self):
        return self.execute()
