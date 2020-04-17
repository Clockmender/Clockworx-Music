import bpy
from .._base.base_node import CM_ND_BaseNode
from bpy.props import (
    IntProperty,
    StringProperty,
)


class CM_ND_RenderNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.render_node"
    bl_label = "Render Animation"
    bl_icon = "SPEAKER"
    bl_width_default = 200

    strt_frame : IntProperty(name="Start Frame", default=1, min=1)
    stop_frame : IntProperty(name="End Frame", default=10, min=2)
    render_dir : StringProperty(subtype="DIR_PATH", name="Render Directory", default="//")

    def draw_buttons(self, context, layout):
        layout.prop(self, "strt_frame")
        layout.prop(self, "stop_frame")
        layout.prop(self, "render_dir")
        layout.separator()
        layout.operator("cm_audio.render_animation", icon="RENDER_ANIMATION")
