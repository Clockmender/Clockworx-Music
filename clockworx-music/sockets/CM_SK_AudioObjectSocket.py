import bpy
from bpy.types import NodeSocket

class CM_SK_AudioObjectSocket(bpy.types.NodeSocket):
    bl_idname = "cm_socket.object"
    bl_label = "Object Socket"

    def draw(self, context, layout, node, x):
        layout.label(text=self.name)

    def draw_color(self, context, node):
        return (0.8, 0.2, 0.8, 0.6)
