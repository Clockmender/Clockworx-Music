import bpy
import aud

from ..cm_functions import (
    connected_node_sound,
)

class CM_ND_AudioAccumulatorNode(bpy.types.Node):
    bl_idname = "cm_audio.accumulator_node"
    bl_label = "Accumulator"
    bl_icon = "SPEAKER"

    additive_prop : bpy.props.BoolProperty(name="Additive", default=False)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "additive_prop")

    def get_sound(self):
        sound = connected_node_sound(self, 0)
        if sound == None:
            return None
        return sound.accumulate(self.additive_prop)
