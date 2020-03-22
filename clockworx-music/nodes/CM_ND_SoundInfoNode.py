import bpy
from bpy.props import (
    FloatProperty,
    IntProperty,
)
from ..cm_functions import connected_node_sound

class CM_ND_SoundInfoNode(bpy.types.Node):
    bl_idname = "cm_audio.sound_info_node"
    bl_label = "Sound Info"
    bl_icon = "SPEAKER"

    length : FloatProperty(name="Length (B)", default=0)
    samples : IntProperty(name="Samples", default=0)
    channels: IntProperty(name="Channels", default=0)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "length")
        layout.prop(self, "samples")
        layout.prop(self, "channels")

    def execute(self):
        cm = bpy.context.scene.cm_pg
        sound = connected_node_sound(self, 0)
        if sound == None:
            return None
        specs = sound.specs
        length = sound.length
        self.channels = specs[1]
        self.samples = specs[0]
        self.length = length / specs[0]
        self.length = self.length * (60 / cm.bpm)

    def get_sound(self):
        return connected_node_sound(self, 0)
