import bpy
from bpy.types import NodeSocket

class CM_SK_AudioMidiSocket(bpy.types.NodeSocket):
    bl_idname = "cm_socket.midi"
    bl_label = "MIDI Socket"

    def draw(self, context, layout, node, x):
        layout.label(text=self.name)

    def draw_color(self, context, node):
        return (1, 1, 0, 0.6)
