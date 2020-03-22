import bpy
import aud

from ..cm_functions import (
    connected_node_sound,
)

class CM_ND_AudioFaderNode(bpy.types.Node):
    bl_idname = "cm_audio.fader_node"
    bl_label = "Fader by Time/Beats"
    bl_icon = "SPEAKER"

    start_prop : bpy.props.FloatProperty(name="Start In", default=0, soft_min=0)
    length_prop : bpy.props.FloatProperty(name="Length In", default=1, soft_min=0)
    starto_prop : bpy.props.FloatProperty(name="Start Out", default=0, soft_min=0)
    lengtho_prop : bpy.props.FloatProperty(name="Length Out", default=1, soft_min=0)
    fade_in_prop : bpy.props.BoolProperty(name="In", default=False)
    fade_out_prop : bpy.props.BoolProperty(name="Out", default=False)
    message : bpy.props.StringProperty(name="")

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        cm_pg = context.scene.cm_pg
        layout.prop(self, "start_prop")
        layout.prop(self, "length_prop")
        layout.prop(self, "starto_prop")
        layout.prop(self, "lengtho_prop")
        row = layout.row()
        row.prop(self, "fade_in_prop")
        row.prop(self, "fade_out_prop")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sound = connected_node_sound(self, 0)
        start_in = self.start_prop * (60 / cm.bpm)
        length_in = self.length_prop * (60 / cm.bpm)
        start_out = self.starto_prop * (60 / cm.bpm)
        length_out = self.lengtho_prop * (60 / cm.bpm)
        if sound == None:
            return None
        if self.fade_in_prop:
            sound = sound.fadein(start_in, length_in)
        if self.fade_out_prop:
            sound = sound.fadeout(start_out, length_out)
        return sound
