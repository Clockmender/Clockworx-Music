import bpy
import aud

from ..cm_functions import (
    connected_node_sound,
)

class CM_ND_AudioEnvelopeNode(bpy.types.Node):
    bl_idname = "cm_audio.envelope_node"
    bl_label = "Envelope"
    bl_icon = "SPEAKER"

    attack_prop : bpy.props.FloatProperty(name="Attack", default=0.005, min=0, soft_max=2)
    release_prop : bpy.props.FloatProperty(name="Release", default=0.2, min=0, soft_max=5)
    threshold_prop : bpy.props.FloatProperty(name="Threshold", default=0, min=0, soft_max=1)
    arthreshold_prop : bpy.props.FloatProperty(name="A/R Threshold", default=0.1, min=0, soft_max=1)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "attack_prop")
        layout.prop(self, "release_prop")
        layout.prop(self, "threshold_prop")
        layout.prop(self, "arthreshold_prop")

    def get_sound(self):
        sound = connected_node_sound(self, 0)
        if sound == None:
            return None
        return sound.envelope(self.attack_prop, self.release_prop,
            self.threshold_prop, self.arthreshold_prop)