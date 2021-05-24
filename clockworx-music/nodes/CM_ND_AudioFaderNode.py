import bpy
import aud
from .._base.base_node import CM_ND_BaseNode
from bpy.types import NodeSocketFloat
from ..cm_functions import (
    connected_node_sound,
    connected_node_output,
    get_socket_values,
    mix_dry_wet,
)

class CM_ND_AudioFaderNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.fader_node"
    bl_label = "Fader"
    bl_icon = "SPEAKER"

    start_prop : bpy.props.FloatProperty(name="Start In", default=0, soft_min=0)
    length_prop : bpy.props.FloatProperty(name="Length In", default=1, soft_min=0)
    starto_prop : bpy.props.FloatProperty(name="Start Out", default=0, soft_min=0)
    lengtho_prop : bpy.props.FloatProperty(name="Length Out", default=1, soft_min=0)
    fade_in_prop : bpy.props.BoolProperty(name="In", default=False)
    fade_out_prop : bpy.props.BoolProperty(name="Out", default=False)
    message : bpy.props.StringProperty(name="")

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.sound", "Audio")
        self.inputs.new("NodeSocketFloat", "Dry Volume")
        self.inputs.new("NodeSocketFloat", "Wet Volume")
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
        cm = bpy.context.scene.cm_pg
        sockets = self.inputs.keys()
        input_values = get_socket_values(self, sockets, self.inputs)
        if connected_node_output(self, 1) is not None:
            dry_vol = connected_node_output(self, 1)["float"]
        else:
            dry_vol = input_values[1]

        if connected_node_output(self, 2) is not None:
            wet_vol = connected_node_output(self, 2)["float"]
        else:
            wet_vol = input_values[2]

        input = connected_node_sound(self, 0)
        if isinstance(input, dict):
            if "sound" in input.keys():
                sound_d = input["sound"]
                sound_w = input["sound"]
                if isinstance(sound_w, aud.Sound):
                    start_in = self.start_prop * (60 / cm.bpm)
                    length_in = self.length_prop * (60 / cm.bpm)
                    start_out = self.starto_prop * (60 / cm.bpm)
                    length_out = self.lengtho_prop * (60 / cm.bpm)
                    if self.fade_in_prop:
                        sound_w = sound_w.fadein(start_in, length_in)
                    if self.fade_out_prop:
                        sound_w = sound_w.fadeout(start_out, length_out)
                    sound = mix_dry_wet(sound_d, sound_w, dry_vol, wet_vol)
                    return {"sound": sound}
        return None

    def output(self):
        return self.get_sound()
