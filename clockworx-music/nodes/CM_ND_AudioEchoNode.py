import bpy
import aud
from .._base.base_node import CM_ND_BaseNode

from ..cm_functions import (
    connected_node_sound,
)

class CM_ND_AudioEchoNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.echo_node"
    bl_label = "Echo"
    bl_icon = "SPEAKER"

    time_prop : bpy.props.FloatProperty(name="Delay", default=0, min=0, soft_max=10)
    echo_num : bpy.props.IntProperty(name="Echos #", default=4, min=1, max=10)
    factor : bpy.props.FloatProperty(name="Decay Factor", default=0.2, min=0.001, max=0.5)
    volume : bpy.props.FloatProperty(name="Volume", default=1, min=0.1)

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "time_prop")
        layout.prop(self, "echo_num")
        layout.prop(self, "factor")
        layout.prop(self, "volume")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        input = connected_node_sound(self, 0)
        if isinstance(input, dict):
            if "sound" in input.keys():
                sound = input["sound"]
                if isinstance(sound, aud.Sound):
                    volume = self.volume
                    sound = sound.volume(volume)
                    first = True
                    for i in range(self.echo_num):
                        delay = (self.time_prop * (i + 1)) * (60 / cm.bpm)
                        volume = volume * (1 - self.factor)
                        snd = sound.delay(delay).volume(volume)
                        if first:
                            sound_out = sound.mix(snd)
                            first = False
                        else:
                            sound_out = sound_out.mix(snd)
                    sound_out.volume(self.volume)
                    return {"sound": sound_out}
        return None

    def output(self):
        return self.get_sound()
