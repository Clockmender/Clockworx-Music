import bpy
import aud

from ..cm_functions import (
    connected_node_sound,
)


class CM_ND_AudioLoopNode(bpy.types.Node):
    bl_idname = "cm_audio.loop_node"
    bl_label = "Loop"
    bl_icon = "SPEAKER"

    loop_prop : bpy.props.IntProperty(name="Loops #", default=1, soft_min=0,
    description="Number of Additional Loops")

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "loop_prop")

    def get_sound(self):
        input = connected_node_sound(self, 0)
        if isinstance(input, dict):
            if "sound" in input.keys():
                sound = input["sound"]
                if isinstance(sound, aud.Sound):
                    sound = sound.loop(self.loop_prop)
                    return {"sound": sound}
        return None

    def output(self):
        return self.get_sound()
