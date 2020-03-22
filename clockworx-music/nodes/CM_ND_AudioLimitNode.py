import bpy
import aud

from ..cm_functions import (
    connected_node_sound,
)


class CM_ND_AudioLimitNode(bpy.types.Node):
    bl_idname = "cm_audio.limit_node"
    bl_label = "Limit by Time/Beats"
    bl_icon = "SPEAKER"

    start_prop : bpy.props.FloatProperty(name="Start (B)", default=0, soft_min=0)
    end_prop : bpy.props.FloatProperty(name="Length (B)", default=1, soft_min=0)
    message : bpy.props.StringProperty(name="")

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        cm_pg = context.scene.cm_pg
        layout.prop(self, "start_prop")
        layout.prop(self, "end_prop")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sound = connected_node_sound(self, 0)
        start = self.start_prop * (60 / cm.bpm)
        length = self.end_prop * (60 / cm.bpm)
        if sound == None or self.start_prop >= self.end_prop:
            return None
        return sound.limit(start, length)
