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

class CM_ND_AudioEchoNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.echo_node"
    bl_label = "Echo"
    bl_icon = "SPEAKER"

    time_prop : bpy.props.FloatProperty(name="Delay", default=0, min=0, soft_max=10, precision=3)
    echo_num : bpy.props.IntProperty(name="Echos #", default=4, min=1, max=10)
    factor : bpy.props.FloatProperty(name="Decay Factor", default=0.2, min=0.001, max=0.5)

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.sound", "Audio")
        self.inputs.new("NodeSocketFloat", "Dry Volume")
        self.inputs.new("NodeSocketFloat", "Wet Volume")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "time_prop")
        layout.prop(self, "echo_num")
        layout.prop(self, "factor")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        input = connected_node_sound(self, 0)
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

        if isinstance(input, dict):
            if "sound" in input.keys():
                sound_d = input["sound"]
                if isinstance(sound_d, aud.Sound):
                    first = True
                    volume = 1
                    for i in range(self.echo_num):
                        delay = (self.time_prop * (i + 1)) * (60 / cm.bpm)
                        volume = volume * (1 - self.factor)
                        snd = sound_d.delay(delay).volume(volume)
                        if first:
                            sound_out = sound_d.mix(snd)
                            first = False
                        else:
                            sound_out = sound_out.mix(snd)
                    sound = mix_dry_wet(sound_d, sound_out, dry_vol, wet_vol)
                    return {"sound": sound}
        return None

    def output(self):
        return self.get_sound()
