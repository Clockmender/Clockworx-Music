import bpy
import aud

from ..cm_functions import (
    connected_node_sound,
)

class CM_ND_AudioDelayNode(bpy.types.Node):
    bl_idname = "cm_audio.delay_node"
    bl_label = "Delay by Time/Beats"
    bl_icon = "SPEAKER"

    time_prop : bpy.props.FloatProperty(name="Delay", default=0, min=0, soft_max=10)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        cm_pg = context.scene.cm_pg
        layout.prop(self, "time_prop")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sound = connected_node_sound(self, 0)
        if sound == None:
            return None
        if cm.type_bool:
            delay = self.time_prop
        else:
            delay = self.time_prop * (60 / cm.bpm)
        return sound.delay(delay)
