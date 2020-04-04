import bpy
from bpy.types import NodeSocket

class CM_SK_AudioBoneSocket(bpy.types.NodeSocket):
    bl_idname = "cm_socket.bone"
    bl_label = "Bone Socket"

    def draw(self, context, layout, node, x):
        layout.label(text=self.name)

    def draw_color(self, context, node):
        return (0.2, 0.2, 1.0, 0.6)
