import bpy
import aud

from ..cm_functions import (
    connected_node_sound,
)

class CM_ND_AudioEchoNode(bpy.types.Node):
    bl_idname = "cm_audio.echo_node"
    bl_label = "Echo"
    bl_icon = "SPEAKER"

    time_prop : bpy.props.FloatProperty(name="Delay", default=0, min=0, soft_max=10)
    echo_num : bpy.props.IntProperty(name="Echos #", default=4, min=1, max=10)
    factor : bpy.props.FloatProperty(name="Decay Factor", default=0.2, min=0.001, max=0.5)
    volume : bpy.props.FloatProperty(name="Volume", default=1, min=0.1)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "time_prop")
        layout.prop(self, "echo_num")
        layout.prop(self, "factor")
        layout.prop(self, "volume")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sound = connected_node_sound(self, 0)
        if sound == None:
            return None
        volume = self.volume
        sound = sound.volume(volume)
        first = True
        for i in range(self.echo_num):
            if cm.type_bool:
                delay = self.time_prop * (i + 1)
            else:
                delay = (self.time_prop * (i + 1)) * (60 / cm.bpm)
            volume = volume * (1 - self.factor)
            snd = sound.delay(delay).volume(volume)
            if first:
                sound_out = sound.mix(snd)
                first = False
            else:
                sound_out = sound_out.mix(snd)
        return sound_out.volume(self.volume)
