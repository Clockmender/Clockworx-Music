import bpy
from bpy.types import NodeSocket
from bpy.props import IntProperty

class CM_SK_IntNodeSocket(bpy.types.NodeSocket):
    bl_idname = "cm_socket.int"
    bl_label = "Integer Socket"
    type = "INT"

    def prop_update(self, context):
        self.id_data.update()

    value: bpy.props.IntProperty(default = 0, update=prop_update)

    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def draw_color(self, context, node):
        return (0.3, 0.7, 0.9, 0.6)
