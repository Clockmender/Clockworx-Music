import bpy
import aud
from .._base.base_node import CM_ND_BaseNode

from ..cm_functions import (
    connected_node_sound,
)

class CM_ND_AudioAccumulatorNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.accumulator_node"
    bl_label = "Accumulator"
    bl_icon = "SPEAKER"

    additive_prop : bpy.props.BoolProperty(name="Additive", default=False)

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "additive_prop")

    def get_sound(self):
        input = connected_node_sound(self, 0)
        if isinstance(input, dict):
            if "sound" in input.keys():
                sound = input["sound"]
                if isinstance(sound, aud.Sound):
                    sound = sound.accumulate(self.additive_prop)
                    return {"sound": sound}
        return None

    def output(self):
        return self.get_sound()
