import bpy
import aud
from bpy.types import (
    NodeSocketFloat,
    NodeSocketBool,
)
from .._base.base_node import CM_ND_BaseNode
from ..cm_functions import get_socket_values, connected_node_output

class CM_ND_AudioFileNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.file_node"
    bl_label = "Sound File"
    bl_icon = "SPEAKER"

    file_name_prop: bpy.props.StringProperty(subtype="FILE_PATH", name="File", default="//")

    def init(self, context):
        super().init(context)
        self.inputs.new("NodeSocketFloat", "Volume")
        self.inputs.new("NodeSocketFloat", "Start (B)")
        self.inputs.new("NodeSocketFloat", "Length (B)")
        self.inputs.new("NodeSocketBool", "Reverse")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "file_name_prop")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sockets = self.inputs.keys()
        input_values = get_socket_values(self, sockets, self.inputs)
        cm = bpy.context.scene.cm_pg
        sound = aud.Sound.file(bpy.path.abspath(self.file_name_prop))
        sound = sound.resample(cm.samples, False)

        if connected_node_output(self, 0) is not None:
            volume = connected_node_output(self, 0)["float"]
        else:
            volume = input_values[0]
        sound = sound.volume(volume)

        if connected_node_output(self, 1) is not None:
            start = connected_node_output(self, 1)["float"]
        else:
            start = input_values[1] * (60 / cm.bpm)
        start = start * (60 / cm.bpm)

        if connected_node_output(self, 2) is not None:
            stop = connected_node_output(self, 2)["float"]
        else:
            stop = input_values[2] * (60 / cm.bpm)
        stop = start + stop
        sound = sound.limit(start, stop)

        if connected_node_output(self, 3) is not None:
            rev = connected_node_output(self, 3)["bool"]
        else:
            rev = input_values[3]

        if rev:
            sound = sound.reverse()
        sound = sound.rechannel(cm.sound_channels)
        return {"sound": sound}

    def output(self):
        return self.get_sound()
