import bpy
from math import cos, pi
from .._base.base_node import CM_ND_BaseNode
from bpy.props import (
   IntProperty,
   FloatProperty,
   StringProperty,
)

class CM_ND_BounceNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.bounce_node"
    bl_label = "Bounce Generator"
    bl_width_default = 200

    frm_s: IntProperty(name="Start Frame", default=2, min=2)
    frm_e: IntProperty(name="End Frame", default=10, min=10)
    speed: FloatProperty(name="Cycle Speed", default=4, min=4)
    spd_d: FloatProperty(name="Speed Decay Factor", default=1, precision=3, min=0.8, max=1)
    spd_v: FloatProperty(name="Compute Factor", default=1, precision=2)
    hgt_s: FloatProperty(name="Start Height", default=1)
    hgt_b: FloatProperty(name="Base Height",default=0)
    message1: StringProperty("")

    def init(self, context):
        super().init(context)
        self.outputs.new("NodeSocketFloat", "Float")

    def draw_buttons(self, context, layout):
        layout.prop(self, "frm_s")
        layout.prop(self, "frm_e")
        layout.prop(self, "speed")
        layout.prop(self, "spd_d")
        layout.prop(self, "hgt_s")
        layout.prop(self, "hgt_b")
        if (self.message1 != ""):
            layout.label(text=self.message1, icon = "ERROR")

    def execute(self):
        if self.frm_s >= self.frm_e + 5 or self.frm_s < bpy.context.scene.frame_start:
            self.message1 = "Start/End Frame Errors"
            cos_w = 0
        frm_c = bpy.context.scene.frame_current
        if self.hgt_s <= (self.hgt_b + 0.1):
            self.message1 = "Height Errors!"
            cos_w = 0
        elif self.frm_s <= bpy.context.scene.frame_start:
            self.message1 = "Start Frame Error!"
            cos_w = 0
        else:
            self.message1 = ""
            len_m = self.frm_e - self.frm_s
            if frm_c == (self.frm_s - 1):
                self.spd_v = self.speed
            if frm_c >= self.frm_s and frm_c <= self.frm_e:
                if self.spd_d == 1:
                    speed = self.speed
                else:
                    speed = self.spd_v
                    if speed <= 4:
                        speed = 4
                fac_m = len_m - (frm_c - self.frm_s)
                cos_w = abs(cos((frm_c - self.frm_s) * 2 * pi / (speed * 2)))
                cos_w = (cos_w * fac_m * self.hgt_s / (self.frm_e - self.frm_s)) + self.hgt_b
                self.spd_v = self.spd_v * (0.99 + (self.spd_d / 100))
            elif frm_c < self.frm_s:
                cos_w = self.hgt_s + self.hgt_b
            else:
                cos_w = self.hgt_b

        return {"float": cos_w}

    def output(self):
        return self.execute()
