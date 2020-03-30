import bpy
from bpy.types import NodeSocket

class CM_SK_AudioCollectionSocket(bpy.types.NodeSocket):
    bl_idname = "cm_socket.collection"
    bl_label = "Collection Socket"

    def draw(self, context, layout, node, x):
        layout.label(text=self.name)

    def draw_color(self, context, node):
        return (0.4, 0.9, 0.9, 0.6)
