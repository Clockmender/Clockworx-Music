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

class CM_ND_AudioDelayNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.delay_node"
    bl_label = "Delay"
    bl_icon = "SPEAKER"

    time_prop : bpy.props.FloatProperty(name="Delay (B)", default=0, min=0, soft_max=10)

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.sound", "Audio")
        self.inputs.new("NodeSocketFloat", "Dry Volume")
        self.inputs.new("NodeSocketFloat", "Wet Volume")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        cm_pg = context.scene.cm_pg
        layout.prop(self, "time_prop")

    def get_sound(self):
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
                if isinstance(sound_d, aud.Sound):
                    delay = self.time_prop * (60 / cm.bpm)
                    sound_w = sound_d.delay(delay)
                    sound = mix_dry_wet(sound_d, sound_w, dry_vol, wet_vol)
                    return {"sound": sound}
        return None


    def output(self):
        return self.get_sound()
