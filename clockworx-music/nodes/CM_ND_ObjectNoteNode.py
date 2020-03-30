import bpy
from bpy.props import (
   BoolProperty,
   FloatProperty,
   StringProperty,
   EnumProperty,
)

class CM_ND_ObjectNoteNode(bpy.types.Node):
    bl_idname = "cm_audio.object_note_node"
    bl_label = "Note Data: Object"
    bl_icon = "SPEAKER"

    control_name : StringProperty(name="Control", default="")
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
        row = box.row()
        row.prop(self, "control_name")
        row.operator("cm_audio.get_name", text="", icon="STYLUS_PRESSURE")
        box.prop(self, "anim_type")
        box.prop(self, "control_axis")
        box.prop(self, "trigger_value")
        layout.prop(self, "note_vol")
        layout.prop(self, "note_dur")
        layout.prop(self, "note_rev")

    def init(self, context):
        self.outputs.new("cm_socket.generic", "Note Data")

    def get_sound(self):
        out = {}
        obj = bpy.data.objects.get(self.control_name)
        if obj is not None:
            if "_" in obj.name:
                if self.anim_type == "loc":
                    value_obj = obj.location[int(self.control_axis)]
                elif self.anim_type == "rot":
                    value_obj = obj.rotation_euler[int(self.control_axis)]
                else:
                    value_obj = obj.scale[int(self.control_axis)]

                if value_obj == self.trigger_value:
                    note_name = obj.name.split("_")[0]
                    out["note_name"] = note_name
                    out["note_freq"] = 0
                    out["note_vol"] = self.note_vol
                    out["note_dur"] = self.note_dur
                    out["note_rev"] = self.note_rev
        return out

    def output(self):
        return self.get_sound()
