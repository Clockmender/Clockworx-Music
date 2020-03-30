import bpy
import aud
from bpy.props import (
    FloatProperty,
    EnumProperty,
    StringProperty,
    BoolProperty,
)
from ..cm_functions import (
    connected_node_sound,
)

class CM_ND_ObjectSoundNode(bpy.types.Node):
    bl_idname = "cm_audio.object_sound_node"
    bl_label = "Speaker: Object"
    bl_icon = "SPEAKER"

    anim_type : EnumProperty(
        items=(
            ("loc", "Location", "Animate Location"),
            ("rot", "Rotation", "Animate Rotation"),
            ("scl", "Scale", "Animate Scale"),
        ),
        name="Animate:",
        default="loc",
        description="Animation Type",
    )
    control_name : StringProperty(name="Control", default="")
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
    last_value : FloatProperty(name="Last Value")
    trigger_value : FloatProperty(name="Trigger Value", default=0.0)
    operand : EnumProperty(
        items=(
            ("con", "Approached", "Value Reaches the Trigger Value"),
            ("dev", "Deviated From", "Value Deviated from the Trigger Value"),
        ),
        name="Operand",
        default="con",
        description="Trigger Operand",
    )

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        box = layout.box()
        row = box.row()
        row.prop(self, "control_name")
        row.operator("cm_audio.get_name", text="", icon="STYLUS_PRESSURE")
        box.prop(self, "anim_type")
        box.prop(self, "control_axis")
        box.prop(self, "operand")
        box.prop(self, "trigger_value")

    def execute(self):
        input = connected_node_sound(self, 0)
        if isinstance(input, dict):
            if "sound" in input.keys():
                sound = input["sound"]
            else:
                sound = None
        else:
            return None
        if not isinstance(sound, aud.Sound):
            return None
        obj = bpy.data.objects[self.control_name]
        if obj is not None:
            if self.anim_type == "loc":
                value_obj = obj.location[int(self.control_axis)]
            elif self.anim_type == "rot":
                value_obj = obj.rotation_euler[int(self.control_axis)]
            else:
                value_obj = obj.scale[int(self.control_axis)]
            if self.operand == "con":
                # Play as value has approached trigger
                if value_obj == self.trigger_value and self.last_value != self.trigger_value:
                    if sound != None:
                        aud.Device().play(sound)
            else:
                # Play as value has deviated from trigger
                if self.trigger_value == self.last_value and value_obj != self.trigger_value:
                    if sound != None:
                        aud.Device().play(sound)
            self.last_value = value_obj
