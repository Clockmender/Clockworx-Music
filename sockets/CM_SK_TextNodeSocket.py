import bpy
from bpy.types import NodeSocket
from bpy.props import StringProperty

class CM_SK_TextNodeSocket(bpy.types.NodeSocket):
    bl_idname = "cm_socket.text"
    bl_label = "Text Socket"
    type = "STRING"

    def prop_update(self, context):
        self.id_data.update()

    value: bpy.props.StringProperty(default = "", update=prop_update)

    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def draw_color(self, context, node):
        return (0.01, 0.9, 0.3, 0.6)
