import bpy
from .._base.base_node import CM_ND_BaseNode
from bpy.types import Material

from bpy.props import (
    PointerProperty,
)

class CM_ND_MaterialNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.material_node"
    bl_label = "Material"
    bl_icon = "SPEAKER"

    material : PointerProperty(type=Material)

    def draw_buttons(self, context, layout):
        layout.prop(self, "material", text="")


    def init(self, context):
        super().init(context)
        self.outputs.new("cm_socket.material", "Material")

    def execute(self):
        return {"material": self.material}

    def output(self):
        return self.execute()

    def get_midi(self):
        return self.execute()
