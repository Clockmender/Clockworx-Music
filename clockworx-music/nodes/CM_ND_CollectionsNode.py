import bpy
from .._base.base_node import CM_ND_BaseNode
from bpy.types import Collection

from bpy.props import (
    StringProperty,
    IntProperty,
    PointerProperty,
)

class CM_ND_CollectionsNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.collections_node"
    bl_label = "Collection"
    bl_icon = "SPEAKER"

    collection : PointerProperty(type=Collection)

    def draw_buttons(self, context, layout):
        layout.prop(self, "collection", text="")


    def init(self, context):
        super().init(context)
        self.outputs.new("cm_socket.collection", "Collection")

    def execute(self):
        return {"collections": self.collection}

    def output(self):
        return self.execute()

    def get_midi(self):
        return self.execute()
