import bpy
from bpy.types import NodeSocket
from bpy.props import StringProperty

class CM_SK_NoteNodeSocket(bpy.types.NodeSocket):
    bl_idname = "cm_socket.note"
    bl_label = "Note Socket"
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
        return (0.3, 0.4, 0.6, 1.0)
