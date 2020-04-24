import bpy
from bpy.types import NodeSocket
from bpy.props import StringProperty

class CM_SK_GuitarNodeSocket(bpy.types.NodeSocket):
    bl_idname = "cm_socket.guitar"
    bl_label = "Guitar Socket"
    type = "VALUE"

    def prop_update(self, context):
        self.id_data.update()

    value: StringProperty(default = "", update=prop_update)

    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def draw_color(self, context, node):
        return (0.3, 0.6, 0.8, 1.0)
