import bpy
from .._base.base_node import CM_ND_BaseNode

from bpy.props import (
   BoolProperty,
   FloatProperty,
   StringProperty,
   EnumProperty,
)
from ..cm_functions import connected_node_output

class CM_ND_ObjectNoteNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.object_note_node"
    bl_label = "Note Data: Object"
    bl_icon = "SPEAKER"

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
    control_axis : EnumProperty(
        items=(
          ("0", "X Axis", "X Axis"),
          ("1", "Y Axis", "Y Axis"),
          ("2", "Z Axis", "Z Axis"),
        ),
        name="Axis",
        default="0",
        description="Contol Axis",
        )
    trigger_value : FloatProperty(name="Trigger Value", default=1.0)
    note_name : StringProperty(name="Note", default="")
    note_freq : FloatProperty(name="Frequency", default=0.0, min=0, max=32000)
    note_vol : FloatProperty(name="Volume", default=1, min=0, max=10)
    note_dur : FloatProperty(name="Length (B)", default=1, min=0.001)
    note_rev: BoolProperty(name="Reverse", default=False)

    def draw_buttons(self, context, layout):
        box = layout.box()
        box.prop(self, "anim_type")
        box.prop(self, "control_axis")
        box.prop(self, "trigger_value")
        layout.prop(self, "note_vol")
        layout.prop(self, "note_dur")
        layout.prop(self, "note_rev")

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.object", "Control")
        self.outputs.new("cm_socket.note", "Note Data")

    def get_sound(self):
        out = {}
        input_1 = connected_node_output(self, 0)
        if isinstance(input_1, dict):
            objects = []
            if "objects" in input_1.keys():
                con_obj = input_1["objects"]

        if con_obj is not None:
            if "_" in con_obj.name:
                if self.anim_type == "loc":
                    value_obj = con_obj.location[int(self.control_axis)]
                elif self.anim_type == "rot":
                    value_obj = con_obj.rotation_euler[int(self.control_axis)]
                else:
                    value_obj = con_obj.scale[int(self.control_axis)]

                if value_obj == self.trigger_value:
                    note_name = con_obj.name.split("_")[0]
                    out["note_name"] = note_name
                    out["note_freq"] = 0
                    out["note_vol"] = self.note_vol
                    out["note_dur"] = self.note_dur
                    out["note_rev"] = self.note_rev
        return out

    def output(self):
        return self.get_sound()
