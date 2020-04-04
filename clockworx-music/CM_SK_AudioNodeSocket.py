import bpy
from bpy.types import NodeSocket

class CM_SK_AudioNodeSocket(bpy.types.NodeSocket):
    bl_idname = "cm_socket.sound"
    bl_label = "Sound Socket"

    def draw(self, context, layout, node, x):
        layout.label(text=self.name)

    def draw_color(self, context, node):
        return (1, 0.5, 0, 0.6)
