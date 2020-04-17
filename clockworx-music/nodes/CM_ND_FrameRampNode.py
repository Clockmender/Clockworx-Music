import bpy
from bpy.types import NodeSocketInt, NodeSocketFloat
from .._base.base_node import CM_ND_BaseNode
from bpy.props import IntProperty
from ..cm_functions import get_socket_values, connected_node_output

class CM_ND_FrameRampNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.frame_ramp_node"
    bl_label = "Frame Ramp"
    bl_icon = "SPEAKER"

    start_frame : IntProperty(name="Start Frame", default=1)
    stop_frame : IntProperty(name="Stop Frame", default=10)

    def init(self, context):
        super().init(context)
        self.inputs.new("NodeSocketFloat", "Input Value")
        self.outputs.new("NodeSocketInt", "Frame Out")

    def draw_buttons(self, context, layout):
        layout.prop(self, "start_frame")
        layout.prop(self, "stop_frame")

    def execute(self):
        if self.stop_frame <= self.start_frame:
            return None
        frame_current = bpy.context.scene.frame_current
        frame_mod = bpy.context.scene.frame_current - self.start_frame
        if frame_mod >= bpy.context.scene.frame_start:
            if frame_current <= self.stop_frame:
                frame_out = frame_mod
            else:
                frame_out = self.stop_frame - self.start_frame
        else:
            frame_out = 0

        input = connected_node_output(self, 0)
        if input is not None:
            input = input["float"]
        else:
            sockets = self.inputs.keys()
            input = get_socket_values(self, sockets, self.inputs)[0]
        output = {}
        output["int"] = frame_out
        output["float"] = input * frame_out
        return output

    def output(self):
        return self.execute()
