import bpy
from bpy.types import NodeSocket
from bpy.props import FloatProperty

class CM_SK_FloatNodeSocket(bpy.types.NodeSocket):
    bl_idname = "cm_socket.float"
    bl_label = "Float Socket"
    type = "VALUE"

    def prop_update(self, context):
        self.id_data.update()

    value: bpy.props.FloatProperty(default = 0.0, update=prop_update)

    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def draw_color(self, context, node):
        return (0.8, 0.8, 0.8, 0.6)
