import bpy
from bpy.types import NodeSocket
from bpy.props import BoolProperty

class CM_SK_BoolNodeSocket(bpy.types.NodeSocket):
    bl_idname = "cm_socket.bool"
    bl_label = "Boolean Node Socket"
    type = "BOOLEAN"

    def prop_update(self, context):
        self.id_data.update()

    value: bpy.props.BoolProperty(default = False, update=prop_update)

    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def draw_color(self, context, node):
        return (0.9, 0.9, 0.3, 0.6)
