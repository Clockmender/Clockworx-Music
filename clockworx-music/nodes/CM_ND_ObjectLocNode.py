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

class CM_ND_ObjectLocNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.object_loc_node"
    bl_label = "Animate Object(s) from Object(s)"
    bl_icon = "SPEAKER"

    factor_x : FloatProperty(name="Factor X", default=1)
    factor_y : FloatProperty(name="Factor Y", default=1)
    factor_z : FloatProperty(name="Factor Z", default=1)
    animate_group : BoolProperty(name="Animate List", default=False)
    suffix : StringProperty(name="Suffix", default="obj")
    message : StringProperty(name="Info")
    anim_type: EnumProperty(
        items=(
            ("loc", "Location", "Animate Location"),
            ("rot", "Rotation", "Animate Rotation"),
            ("scl", "Scale", "Animate Scale"),
        ),
        name="Animate:",
        default="loc",
        description="Animation Type",
    )

    def draw_buttons(self, context, layout):
        box = layout.box()
        box.prop(self, "anim_type")
        row = box.row()
        box.prop(self, "factor_x")
        box.prop(self, "factor_y")
        box.prop(self, "factor_z")
        layout.separator()
        box = layout.box()
        layout.label(text=self.message, icon="INFO")
        box.prop(self, "animate_group")
        row = box.row()
        row.prop(self, "suffix")
        row.operator("cm_audio.get_suffix", text="", icon="STYLUS_PRESSURE")

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.object", "Control")
        self.inputs.new("cm_socket.object", "Target")

    def execute(self):
        def off_set(obj):
            a_offset = obj.matrix_world.decompose()[0].z
            x_loc = 0
            y_loc = 0
            z_loc = 0
            x_loc = a_offset * self.factor_x
            y_loc = a_offset * self.factor_y
            z_loc = a_offset * self.factor_z
            return (
                Vector((x_loc, y_loc, z_loc)),
                Euler(((x_loc * pi / 18), (y_loc * pi / 18), (z_loc * pi / 18))),
                Vector(((1 + x_loc), (1 + y_loc), (1 + z_loc)))
                )
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
        tgt_obj = None
        if isinstance(input_2, dict):
            objects = []
            if "objects" in input_2.keys():
                objects = input_2["objects"]
                if not isinstance(objects, list):
                    objects = [objects]
                if len(objects) == 1:
                    tgt_obj = objects[0]

        if not self.animate_group and tgt_obj is not None and con_obj is not None:
            self.message = "List Function Inactive"
            vector_delta, euler_delta, scale_delta = off_set(con_obj)
            if self.anim_type == "loc":
                tgt_obj.delta_location = vector_delta
            elif self.anim_type == "rot":
                tgt_obj.delta_rotation_euler = euler_delta
            else:
                tgt_obj.delta_scale = scale_delta

        elif self.animate_group and con_obj is not None:
            search = con_obj.name.split("_")[1]
            self.message = f"Using: '{search}' to find Controls"
            objs_list = ([o for o in bpy.data.objects
                if len(o.name.split("_")) == 2
                and o.name.split("_")[1] == search]
                )
            for obj in objs_list:
                vector_delta, euler_delta, scale_delta = off_set(obj)
                note_name = obj.name.split("_")[0]
                tgt_obj = bpy.data.objects[f"{note_name}_{self.suffix}"]
                if tgt_obj is not None:
                    if self.anim_type == "loc":
                        tgt_obj.delta_location = vector_delta
                    elif self.anim_type == "rot":
                        tgt_obj.delta_rotation_euler = euler_delta
                    else:
                        tgt_obj.delta_scale = scale_delta
