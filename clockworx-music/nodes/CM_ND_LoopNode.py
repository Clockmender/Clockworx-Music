import bpy
from bpy.types import NodeSocketBool
from bpy.props import (
   BoolProperty,
   IntProperty,
   EnumProperty,
   StringProperty,
   FloatProperty,
)
from .._base.base_node import CM_ND_BaseNode
from ..cm_functions import (
    get_socket_values,
    connected_node_output,
)

class CM_ND_LoopNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.loop_node"
    bl_label = "Dr. Clock Loop Programmer"
    bl_icon = "SPEAKER"
    bl_width_default = 500
    bl_width_max = 500
    bl_width_min = 500

    pos_b1 : BoolProperty(default=False)
    pos_b2 : BoolProperty(default=False)
    pos_b3 : BoolProperty(default=False)
    pos_b4 : BoolProperty(default=False)
    pos_b5 : BoolProperty(default=False)
    pos_b6 : BoolProperty(default=False)
    pos_b7 : BoolProperty(default=False)
    pos_b8 : BoolProperty(default=False)
    pos_b9 : BoolProperty(default=False)
    pos_b10 : BoolProperty(default=False)
    pos_b11 : BoolProperty(default=False)
    pos_b12 : BoolProperty(default=False)
    pos_b13 : BoolProperty(default=False)
    pos_b14 : BoolProperty(default=False)
    pos_b15 : BoolProperty(default=False)
    pos_b16 : BoolProperty(default=False)

    pos_as1 : BoolProperty(default=False)
    pos_as2 : BoolProperty(default=False)
    pos_as3 : BoolProperty(default=False)
    pos_as4 : BoolProperty(default=False)
    pos_as5 : BoolProperty(default=False)
    pos_as6 : BoolProperty(default=False)
    pos_as7 : BoolProperty(default=False)
    pos_as8 : BoolProperty(default=False)
    pos_as9 : BoolProperty(default=False)
    pos_as10 : BoolProperty(default=False)
    pos_as11 : BoolProperty(default=False)
    pos_as12 : BoolProperty(default=False)
    pos_as13 : BoolProperty(default=False)
    pos_as14 : BoolProperty(default=False)
    pos_as15 : BoolProperty(default=False)
    pos_as16 : BoolProperty(default=False)

    pos_a1 : BoolProperty(default=False)
    pos_a2 : BoolProperty(default=False)
    pos_a3 : BoolProperty(default=False)
    pos_a4 : BoolProperty(default=False)
    pos_a5 : BoolProperty(default=False)
    pos_a6 : BoolProperty(default=False)
    pos_a7 : BoolProperty(default=False)
    pos_a8 : BoolProperty(default=False)
    pos_a9 : BoolProperty(default=False)
    pos_a10 : BoolProperty(default=False)
    pos_a11 : BoolProperty(default=False)
    pos_a12 : BoolProperty(default=False)
    pos_a13 : BoolProperty(default=False)
    pos_a14 : BoolProperty(default=False)
    pos_a15 : BoolProperty(default=False)
    pos_a16 : BoolProperty(default=False)

    pos_gs1 : BoolProperty(default=False)
    pos_gs2 : BoolProperty(default=False)
    pos_gs3 : BoolProperty(default=False)
    pos_gs4 : BoolProperty(default=False)
    pos_gs5 : BoolProperty(default=False)
    pos_gs6 : BoolProperty(default=False)
    pos_gs7 : BoolProperty(default=False)
    pos_gs8 : BoolProperty(default=False)
    pos_gs9 : BoolProperty(default=False)
    pos_gs10 : BoolProperty(default=False)
    pos_gs11 : BoolProperty(default=False)
    pos_gs12 : BoolProperty(default=False)
    pos_gs13 : BoolProperty(default=False)
    pos_gs14 : BoolProperty(default=False)
    pos_gs15 : BoolProperty(default=False)
    pos_gs16 : BoolProperty(default=False)

    pos_g1 : BoolProperty(default=False)
    pos_g2 : BoolProperty(default=False)
    pos_g3 : BoolProperty(default=False)
    pos_g4 : BoolProperty(default=False)
    pos_g5 : BoolProperty(default=False)
    pos_g6 : BoolProperty(default=False)
    pos_g7 : BoolProperty(default=False)
    pos_g8 : BoolProperty(default=False)
    pos_g9 : BoolProperty(default=False)
    pos_g10 : BoolProperty(default=False)
    pos_g11 : BoolProperty(default=False)
    pos_g12 : BoolProperty(default=False)
    pos_g13 : BoolProperty(default=False)
    pos_g14 : BoolProperty(default=False)
    pos_g15 : BoolProperty(default=False)
    pos_g16 : BoolProperty(default=False)

    pos_fs1 : BoolProperty(default=False)
    pos_fs2 : BoolProperty(default=False)
    pos_fs3 : BoolProperty(default=False)
    pos_fs4 : BoolProperty(default=False)
    pos_fs5 : BoolProperty(default=False)
    pos_fs6 : BoolProperty(default=False)
    pos_fs7 : BoolProperty(default=False)
    pos_fs8 : BoolProperty(default=False)
    pos_fs9 : BoolProperty(default=False)
    pos_fs10 : BoolProperty(default=False)
    pos_fs11 : BoolProperty(default=False)
    pos_fs12 : BoolProperty(default=False)
    pos_fs13 : BoolProperty(default=False)
    pos_fs14 : BoolProperty(default=False)
    pos_fs15 : BoolProperty(default=False)
    pos_fs16 : BoolProperty(default=False)

    pos_f1 : BoolProperty(default=False)
    pos_f2 : BoolProperty(default=False)
    pos_f3 : BoolProperty(default=False)
    pos_f4 : BoolProperty(default=False)
    pos_f5 : BoolProperty(default=False)
    pos_f6 : BoolProperty(default=False)
    pos_f7 : BoolProperty(default=False)
    pos_f8 : BoolProperty(default=False)
    pos_f9 : BoolProperty(default=False)
    pos_f10 : BoolProperty(default=False)
    pos_f11 : BoolProperty(default=False)
    pos_f12 : BoolProperty(default=False)
    pos_f13 : BoolProperty(default=False)
    pos_f14 : BoolProperty(default=False)
    pos_f15 : BoolProperty(default=False)
    pos_f16 : BoolProperty(default=False)

    pos_e1 : BoolProperty(default=False)
    pos_e2 : BoolProperty(default=False)
    pos_e3 : BoolProperty(default=False)
    pos_e4 : BoolProperty(default=False)
    pos_e5 : BoolProperty(default=False)
    pos_e6 : BoolProperty(default=False)
    pos_e7 : BoolProperty(default=False)
    pos_e8 : BoolProperty(default=False)
    pos_e9 : BoolProperty(default=False)
    pos_e10 : BoolProperty(default=False)
    pos_e11 : BoolProperty(default=False)
    pos_e12 : BoolProperty(default=False)
    pos_e13 : BoolProperty(default=False)
    pos_e14 : BoolProperty(default=False)
    pos_e15 : BoolProperty(default=False)
    pos_e16 : BoolProperty(default=False)

    pos_ds1 : BoolProperty(default=False)
    pos_ds2 : BoolProperty(default=False)
    pos_ds3 : BoolProperty(default=False)
    pos_ds4 : BoolProperty(default=False)
    pos_ds5 : BoolProperty(default=False)
    pos_ds6 : BoolProperty(default=False)
    pos_ds7 : BoolProperty(default=False)
    pos_ds8 : BoolProperty(default=False)
    pos_ds9 : BoolProperty(default=False)
    pos_ds10 : BoolProperty(default=False)
    pos_ds11 : BoolProperty(default=False)
    pos_ds12 : BoolProperty(default=False)
    pos_ds13 : BoolProperty(default=False)
    pos_ds14 : BoolProperty(default=False)
    pos_ds15 : BoolProperty(default=False)
    pos_ds16 : BoolProperty(default=False)

    pos_d1 : BoolProperty(default=False)
    pos_d2 : BoolProperty(default=False)
    pos_d3 : BoolProperty(default=False)
    pos_d4 : BoolProperty(default=False)
    pos_d5 : BoolProperty(default=False)
    pos_d6 : BoolProperty(default=False)
    pos_d7 : BoolProperty(default=False)
    pos_d8 : BoolProperty(default=False)
    pos_d9 : BoolProperty(default=False)
    pos_d10 : BoolProperty(default=False)
    pos_d11 : BoolProperty(default=False)
    pos_d12 : BoolProperty(default=False)
    pos_d13 : BoolProperty(default=False)
    pos_d14 : BoolProperty(default=False)
    pos_d15 : BoolProperty(default=False)
    pos_d16 : BoolProperty(default=False)

    pos_cs1 : BoolProperty(default=False)
    pos_cs2 : BoolProperty(default=False)
    pos_cs3 : BoolProperty(default=False)
    pos_cs4 : BoolProperty(default=False)
    pos_cs5 : BoolProperty(default=False)
    pos_cs6 : BoolProperty(default=False)
    pos_cs7 : BoolProperty(default=False)
    pos_cs8 : BoolProperty(default=False)
    pos_cs9 : BoolProperty(default=False)
    pos_cs10 : BoolProperty(default=False)
    pos_cs11 : BoolProperty(default=False)
    pos_cs12 : BoolProperty(default=False)
    pos_cs13 : BoolProperty(default=False)
    pos_cs14 : BoolProperty(default=False)
    pos_cs15 : BoolProperty(default=False)
    pos_cs16 : BoolProperty(default=False)

    pos_c1 : BoolProperty(default=False)
    pos_c2 : BoolProperty(default=False)
    pos_c3 : BoolProperty(default=False)
    pos_c4 : BoolProperty(default=False)
    pos_c5 : BoolProperty(default=False)
    pos_c6 : BoolProperty(default=False)
    pos_c7 : BoolProperty(default=False)
    pos_c8 : BoolProperty(default=False)
    pos_c9 : BoolProperty(default=False)
    pos_c10 : BoolProperty(default=False)
    pos_c11 : BoolProperty(default=False)
    pos_c12 : BoolProperty(default=False)
    pos_c13 : BoolProperty(default=False)
    pos_c14 : BoolProperty(default=False)
    pos_c15 : BoolProperty(default=False)
    pos_c16 : BoolProperty(default=False)

    octave : IntProperty(name="Octave", default=4, min=0,max=10)
    length : EnumProperty(
        items=(
            ("0.25", "Quarter", "Quarter Beat"),
            ("0.5", "Half", "Half Beat"),
            ("1", "One Beat", "One Beat"),
            ("2", "Two Beats", "Two Beats"),
            ("4", "Four Beats", "Four Beats"),
            ("8", "Eight Beats", "Eight Beats"),
            ("16", "Sixteen Beats", "Sixteen Beats"),
        ),
        name="Length",
        default="1",
    )
    volume : FloatProperty(name="Volume", min=0, max=1, default=0.5)
    reverse : BoolProperty(name="Reverse", default=False)

    def init(self, context):
        super().init(context)
        self.inputs.new("NodeSocketBool", "Process")
        self.outputs.new("cm_socket.note", "Note Data")

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.label(text="B")
        for i in range(1, 17):
            row.prop(self, "pos_b"+str(i))
        row = layout.row()
        row.label(text="AS")
        for i in range(1, 17):
            row.prop(self, "pos_as"+str(i))
        row = layout.row()
        row.label(text="A")
        for i in range(1, 17):
            row.prop(self, "pos_a"+str(i))
        row = layout.row()
        row.label(text="GS")
        for i in range(1, 17):
            row.prop(self, "pos_gs"+str(i))
        row = layout.row()
        row.label(text="G")
        for i in range(1, 17):
            row.prop(self, "pos_g"+str(i))
        row = layout.row()
        row.label(text="FS")
        for i in range(1, 17):
            row.prop(self, "pos_fs"+str(i))
        row = layout.row()
        row.label(text="F")
        for i in range(1, 17):
            row.prop(self, "pos_f"+str(i))
        row = layout.row()
        row.label(text="E")
        for i in range(1, 17):
            row.prop(self, "pos_e"+str(i))
        row = layout.row()
        row.label(text="DS")
        for i in range(1, 17):
            row.prop(self, "pos_ds"+str(i))
        row = layout.row()
        row.label(text="D")
        for i in range(1, 17):
            row.prop(self, "pos_d"+str(i))
        row = layout.row()
        row.label(text="CS")
        for i in range(1, 17):
            row.prop(self, "pos_cs"+str(i))
        row = layout.row()
        row.label(text="C")
        for i in range(1, 17):
            row.prop(self, "pos_c"+str(i))
        row = layout.row()
        for i in range(17):
            if i == 0:
                row.label(text="")
            else:
                row.label(text=str(i))
        layout.separator()
        row = layout.row()
        row.prop(self, "octave")
        row.prop(self, "length")
        row = layout.row()
        row.prop(self, "volume")
        row.prop(self, "reverse")

    def execute(self):
        cm = bpy.context.scene.cm_pg
        process = connected_node_output(self, 0)
        if process is None:
            sockets = self.inputs.keys()
            process = get_socket_values(self, sockets, self.inputs)[0]
        if isinstance(process, dict):
            if "bool" in process.keys():
                process = process["bool"]
            else:
                return None
        if not process:
            return None

        if (
            (cm.note_den == "16" and self.length in ["0.25", "0.5"]) or
            (cm.note_den == "32" and self.length in ["0.5"])
            ):
            print(f"Cannot use {self.length} Beat for {cm.note_den} Note Denominator")
            return None
        anim_start_frame = cm.offset
        frame_current = bpy.context.scene.frame_current
        frame_start = bpy.context.scene.frame_start
        if frame_current < anim_start_frame:
            return None

        anim_frame = frame_current - anim_start_frame
        if self.length == "2":
            anim_frame = anim_frame / 2
        elif self.length == "4":
            anim_frame = anim_frame / 4
        elif self.length == "8":
            anim_frame = anim_frame / 8
        elif self.length == "16":
            anim_frame = anim_frame / 16
        else:
            anim_frame = anim_frame

        anim_cycle = float((anim_frame % 16) + 1)

        if anim_cycle.is_integer():
            anim_cycle = int(anim_cycle)
            note_dur = float(self.length) / float(cm.note_den)
            if len(str(anim_cycle)) == 1:
                vars = [k for k in dir(self) if k.startswith("pos_")
                and k[-1] == str(anim_cycle)
                and k[-2] is not "1"]
            else:
                vars = [k for k in dir(self) if k.startswith("pos_")
                and k[-2:] == str(anim_cycle)]
            out_notes = []
            for v in vars:
                if eval("self." + v):
                    output = {}
                    note = v.split("_")[1]
                    if "s" in note:
                        note = note[0:2] + str(self.octave)
                    else:
                        note = note[0] + str(self.octave)
                    output["note_name"] = note
                    output["note_freq"] = 0
                    output["note_vol"] = self.volume
                    output["note_dur"] = note_dur
                    output["note_rev"] = self.reverse
                    out_notes.append(output)
            return out_notes

    def output(self):
        return self.execute()
