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


class CM_ND_AudioRecordNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.record_node"
    bl_label = "Record Sounds"
    bl_icon = "SPEAKER"
    bl_width_min = 250

    start_frm : IntProperty(name="Start Frame", default=1, min=0)
    stop_frm : IntProperty(name="Stop Frame", default=10, min=1)
    overwrite : BoolProperty(name="Overwrite File", default=False)
    file_name : StringProperty(name="File Name", subtype="FILE_PATH", default="//")
    sequence_channel : IntProperty(name="VSE Channel", default=1, min=1)
    sequence_name : StringProperty(name="VSE Name", default="Record")

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.context_pointer_set("audionode", self)
        layout.prop(self, "start_frm")
        layout.prop(self, "stop_frm")
        layout.prop(self, "overwrite")
        layout.prop(self, "file_name")
        layout.prop(self, "sequence_name")
        layout.prop(self, "sequence_channel")
        layout.operator("cm_audio.record_audio", icon="COLORSET_01_VEC")

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
