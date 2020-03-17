import bpy
import aud

from ..cm_functions import (
    connected_node_sound,
)

class CM_ND_AudioHighpassNode(bpy.types.Node):
    bl_idname = "cm_audio.highpass_node"
    bl_label = "Highpass"
    bl_icon = "SPEAKER"

    frequency_prop : bpy.props.FloatProperty(name="Frequency",
        default=440, soft_min=20, soft_max=20000)
    q_prop : bpy.props.FloatProperty(name="Q Factor", default=0.5, soft_min=0, soft_max=1)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "frequency_prop")
        layout.prop(self, "q_prop")

    def get_sound(self):
        sound = connected_node_sound(self, 0)
        if sound == None:
            return None
        return sound.highpass(self.frequency_prop, self.q_prop)
