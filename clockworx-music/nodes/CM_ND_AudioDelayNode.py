import bpy
import aud
from .._base.base_node import CM_ND_BaseNode

from ..cm_functions import (
    connected_node_sound,
)

class CM_ND_AudioDelayNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.delay_node"
    bl_label = "Delay"
    bl_icon = "SPEAKER"

    time_prop : bpy.props.FloatProperty(name="Delay", default=0, min=0, soft_max=10)

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        cm_pg = context.scene.cm_pg
        layout.prop(self, "time_prop")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        input = connected_node_sound(self, 0)
        if isinstance(input, dict):
            if "sound" in input.keys():
                sound = input["sound"]
                if isinstance(sound, aud.Sound):
                    delay = self.time_prop * (60 / cm.bpm)
                    sound = sound.delay(delay)
                    return {"sound": sound}
        return None


    def output(self):
        return self.get_sound()
