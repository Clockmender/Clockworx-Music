import bpy
from math import pi
from mathutils import Vector, Euler
from bpy.props import (
    FloatProperty,
    EnumProperty,
    StringProperty,
    BoolProperty,
)


class CM_ND_ObjectLocNode(bpy.types.Node):
    bl_idname = "cm_audio.object_loc_node"
    bl_label = "Animate Objects from Object"
    bl_icon = "SPEAKER"

    control_name : StringProperty(name="Control", default="")
    factor_x : FloatProperty(name="Factor X", default=1)
    factor_y : FloatProperty(name="Factor Y", default=1)
    factor_z : FloatProperty(name="Factor Z", default=1)
    lx_bool : BoolProperty(name="X", default=False)
    ly_bool : BoolProperty(name="Y", default=False)
    lz_bool : BoolProperty(name="Z", default=False)
    object_name : StringProperty(name="Target", default="")
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
        row.prop(self, "control_name")
        row.operator("cm_audio.get_name", text="", icon="STYLUS_PRESSURE")
        row = box.row()
        box.prop(self, "factor_x")
        box.prop(self, "factor_y")
        box.prop(self, "factor_z")
        row = box.row()
        row.prop(self, "lx_bool")
        row.prop(self, "ly_bool")
        row.prop(self, "lz_bool")
        row = box.row()
        row.prop(self, "object_name")
        row.operator("cm_audio.get_target", text="", icon="STYLUS_PRESSURE")
        layout.label(text="")
        box = layout.box()
        box.prop(self, "message", text="")
        box.prop(self, "animate_group")
        row = box.row()
        row.prop(self, "suffix")
        row.operator("cm_audio.get_suffix", text="", icon="STYLUS_PRESSURE")

    def execute(self):
        def off_set(obj):
            a_offset = obj.matrix_world.decompose()[0].z
            x_loc = 0
            y_loc = 0
            z_loc = 0
            if self.lx_bool:
                x_loc = a_offset * self.factor_x
            if self.ly_bool:
                y_loc = a_offset * self.factor_y
            if self.lz_bool:
                z_loc = a_offset * self.factor_z
            return (
                Vector((x_loc, y_loc, z_loc)),
                Euler(((x_loc * pi / 18), (y_loc * pi / 18), (z_loc * pi / 18))),
                Vector(((1 + x_loc), (1 + y_loc), (1 + z_loc)))
                )

        if not self.animate_group:
            self.message = "List Function Inactive"
            obj = bpy.data.objects[self.control_name]
            if obj is not None:
                vector_delta, euler_delta, scale_delta = off_set(obj)
                tgt_obj = bpy.data.objects[self.object_name]
                if tgt_obj is not None:
                    if self.anim_type == "loc":
                        tgt_obj.delta_location = vector_delta
                    elif self.anim_type == "rot":
                        tgt_obj.delta_rotation_euler = euler_delta
                    else:
                        tgt_obj.delta_scale = scale_delta

        else:
            search = self.control_name.split("_")[1]
            self.message = f"Using: '{search}' to find Controls"
            objs_list = ([o for o in bpy.data.objects
                if len(o.name.split("_")) == 2
                and o.name.split("_")[1] == search]
                )
            for obj in objs_list:
                vector_delta, euler_delta, scale_delta = off_set(obj)
                note_name = obj.name.split("_")[0]
                tgt_obj = bpy.data.objects[f"{note_name}_{self.suffix}"]
                if self.anim_type == "loc":
                    tgt_obj.delta_location = vector_delta
                elif self.anim_type == "rot":
                    tgt_obj.delta_rotation_euler = euler_delta
                else:
                    tgt_obj.delta_scale = scale_delta
