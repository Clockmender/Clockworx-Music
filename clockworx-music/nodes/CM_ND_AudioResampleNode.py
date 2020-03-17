import bpy
import aud

from ..cm_functions import (
    connected_node_sound,
)


class CM_ND_AudioResampleNode(bpy.types.Node):
    bl_idname = "cm_audio.resample_node"
    bl_label = "Resample To System"
    bl_icon = "SPEAKER"

    qual_bool : bpy.props.BoolProperty(name="H/L Quality", default=False)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, "qual_bool")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sound = connected_node_sound(self, 0)
        if sound == None:
          return None
        return sound.resample(cm.samples, self.qual_bool)