import bpy
from .._base.base_node import CM_ND_BaseNode
from math import pi
from mathutils import Vector, Euler
from bpy.props import (
    FloatProperty,
    EnumProperty,
    StringProperty,
    BoolProperty,
)
from ..cm_functions import connected_node_output

class CM_ND_ShapekeyAnimNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.shapekey_anim_node"
    bl_label = "Animate Shapekey(s) from Object(s)"
    bl_icon = "SPEAKER"

    factor : FloatProperty(name="Factor", default=1)
    animate_group : BoolProperty(name="Animate List", default=False)
    message : StringProperty(name="Info")

    def draw_buttons(self, context, layout):
        box = layout.box()
        box.prop(self, "factor")
        box.prop(self, "animate_group")
        layout.separator()
        layout.label(text=self.message, icon="INFO")

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.object", "Control(s)")
        self.inputs.new("cm_socket.shapekey", "Shapekey(s)")

    def execute(self):
        def off_set(obj):
            a_offset = obj.matrix_world.decompose()[0].z
            a_offset = a_offset * self.factor
            return a_offset

        input_1 = connected_node_output(self, 0)
        con_obj = None
        if isinstance(input_1, dict):
            objects = []
            if "objects" in input_1.keys():
                objects = input_1["objects"]
                if not isinstance(objects, list):
                    objects = [objects]
                if len(objects) == 1:
                    con_obj = objects[0]

        input_2 = connected_node_output(self, 1)
        key_list = None
        if isinstance(input_2, dict):
            if "sk-basis" in input_2.keys():
                key_list = [k for k in input_2.keys() if "key" in k]

        if not self.animate_group and key_list is not None and con_obj is not None:
            search = con_obj.name.split("_")[0]
            self.message = "List Function Inactive"
            value = off_set(con_obj)
            if len(key_list) == 1:
                input_2[key_list[0]].value = value

        elif self.animate_group and key_list is not None:
            self.message = "Using List of Controls"
            for obj in objects:
                if "_" in obj.name:
                    value = off_set(obj)
                    note_name = obj.name.split("_")[0]
                    key = f"key-{note_name}"
                    input_2[key].value = value




# list(object.data.shape_keys.key_blocks)
# key_blocks["fs3"].value
