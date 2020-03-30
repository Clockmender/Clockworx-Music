import bpy
import aud

from ..cm_functions import (
    connected_node_sound,
)


class CM_ND_AudioPitchNode(bpy.types.Node):
    bl_idname = "cm_audio.pitch_node"
    bl_label = "Pitch"
    bl_icon = "SPEAKER"

    pitch_prop : bpy.props.FloatProperty(name="Pitch", default=1, soft_min=0.1, soft_max=4)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "pitch_prop")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        input = connected_node_sound(self, 0)
        if isinstance(input, dict):
            if "sound" in input.keys():
                sound = input["sound"]
                if isinstance(sound, aud.Sound):
                    sound = sound.pitch(self.pitch_prop)
                    return {"sound": sound}
        return None

    def output(self):
        return self.get_sound()
