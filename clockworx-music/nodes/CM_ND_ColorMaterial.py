import bpy
from bpy.types import NodeSocketColor
from .._base.base_node import CM_ND_BaseNode
from bpy.props import FloatVectorProperty
from ..cm_functions import get_socket_values, connected_node_output

class CM_ND_ColorMaterial(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.colour_material_node"
    bl_label = "Material Colour"
    bl_icon = "SPEAKER"

    def init(self, context):
        super().init(context)
        self.inputs.new("NodeSocketColor", "Colour")
        self.inputs.new("cm_socket.material", "Material")

    def execute(self):
        cm = bpy.context.scene.cm_pg
        sockets = self.inputs.keys()
        input_values = get_socket_values(self, sockets, self.inputs)
        input = connected_node_output(self, 0)
        if input is not None:
            colour = input["colour"]
        else:
            colour = input_values[0]
        material = input_values[1]
        if colour is not None:
            material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = colour
            material.diffuse_color = colour

    def output(self):
        return self.execute()

# diffuse_color
