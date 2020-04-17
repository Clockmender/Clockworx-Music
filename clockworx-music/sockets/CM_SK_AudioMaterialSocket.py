import bpy
from bpy.types import NodeSocket

class CM_SK_AudioMaterialSocket(bpy.types.NodeSocket):
    bl_idname = "cm_socket.material"
    bl_label = "Material Socket"

    def draw(self, context, layout, node, x):
        layout.label(text=self.name)

    def draw_color(self, context, node):
        return (0.5, 0.6, 0.8, 0.6)
