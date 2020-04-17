import bpy
from bpy.types import NodeSocket

class CM_SK_AudioSoundSocket(bpy.types.NodeSocket):
    bl_idname = "cm_socket.sound_data"
    bl_label = "Sound Data Socket"

    def draw(self, context, layout, node, x):
        layout.label(text=self.name)

    def draw_color(self, context, node):
        return (0.5, 0.5, 1.0, 0.6)
