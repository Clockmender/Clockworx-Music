import bpy
from bpy.types import NodeSocket

class CM_SK_AudioShapekeySocket(bpy.types.NodeSocket):
    bl_idname = "cm_socket.shapekey"
    bl_label = "Bone Socket"

    def draw(self, context, layout, node, x):
        layout.label(text=self.name)

    def draw_color(self, context, node):
        return (0.1, 0.4, 0.1, 0.6)
