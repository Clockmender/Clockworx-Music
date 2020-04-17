import bpy
import aud
from .._base.base_node import CM_ND_BaseNode

from bpy.props import (
   StringProperty,
   IntProperty,
   FloatProperty,
   BoolProperty,
)
from ..cm_functions import connected_node_sound


class CM_ND_AudioWriteNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.write_node"
    bl_label = "Speaker: Play/Write"
    bl_icon = "SPEAKER"
    bl_width_default = 180

    write_name : StringProperty(subtype="FILE_PATH", name="Ouptut File Name", default="//")
    sequence_channel : IntProperty(name="Channel", default=1)
    add_file : BoolProperty(name="Add to VSE", default=False)
    time_off : FloatProperty(name="Offset (B)", default=0,
        description="Number of Beats offset from start of song")
    strip_name : StringProperty(name="Strip Name", default="")

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.sound", "Audio")

    def get_sound(self):
        input = connected_node_sound(self, 0)
        if isinstance(input, dict):
            if "sound" in input.keys():
                sound = input["sound"]
            else:
                sound = None
            return sound
        else:
            return None

    def draw_buttons(self, context, layout):
        layout.context_pointer_set("audionode", self)
        layout.operator("cm_audio.play_audio")
        box = layout.box()
        box.operator("cm_audio.stop_audio")
        box.prop(self, "write_name")
        box.prop(self, "strip_name")
        box.prop(self, "add_file")
        box.prop(self, "time_off")
        box.prop(self, "sequence_channel")
        box.operator("cm_audio.write_audio")
