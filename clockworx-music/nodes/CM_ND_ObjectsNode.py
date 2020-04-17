import bpy
from .._base.base_node import CM_ND_BaseNode
from bpy.types import Object

from bpy.props import (
    PointerProperty,
)

from ..cm_functions import connected_node_output

class CM_ND_ObjectsNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.objects_node"
    bl_label = "Object"
    bl_icon = "SPEAKER"

    object : PointerProperty(type=Object)

    def draw_buttons(self, context, layout):
        layout.prop(self, "object", text="")

    def init(self, context):
        super().init(context)
        self.outputs.new("cm_socket.object", "Object")

    def execute(self):
        return {"objects": self.object}

    def output(self):
        return self.execute()

    def get_midi(self):
        return self.execute()
