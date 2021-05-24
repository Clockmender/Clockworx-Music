import bpy
import aud
from .._base.base_node import CM_ND_BaseNode
from bpy.props import (
   FloatProperty,
   BoolProperty,
   IntProperty,
)
from bpy.types import NodeSocketFloat
from ..cm_functions import (
    connected_node_sound,
    connected_node_output,
    get_socket_values,
    mix_dry_wet,
)

class CM_ND_AudioIirFirFilter(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.iir_fir_node"
    bl_label = "IIR/FIR Filter"
    bl_width_default = 220

    typeB : BoolProperty(name="IIR/FIR",default=True)
    a : FloatProperty(name='B1')
    b : FloatProperty(name='B2')
    c : FloatProperty(name='B3')
    d : FloatProperty(name='B4')
    e : FloatProperty(name='B5')
    f : FloatProperty(name='B6')

    g : FloatProperty(name='A1', min=0, max=1)
    h : FloatProperty(name='A2')
    i : FloatProperty(name='A3')
    j : FloatProperty(name='A4')
    k : FloatProperty(name='A5')
    l : FloatProperty(name='A6')

    filter_n: IntProperty(name="Number of Filter Values", default=6, min=1, max=6)

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.sound", "Audio")
        self.inputs.new("NodeSocketFloat", "Dry Volume")
        self.inputs.new("NodeSocketFloat", "Wet Volume")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, "filter_n")
        row.prop(self, "typeB")
        colm = layout.column()

        row = colm.row()
        row.label(text="FIR Sequence")
        row = colm.row()
        col = row.column()
        col.prop(self, "a")
        col = row.column()
        col.prop(self, "b")
        row = colm.row()
        col = row.column()
        col.prop(self, "c")
        col = row.column()
        col.prop(self, "d")
        row = colm.row()
        col = row.column()
        col.prop(self, "e")
        col = row.column()
        col.prop(self, "f")

        row = colm.row()
        row.label(text="IIR Sequence")
        row = colm.row()
        col = row.column()
        col.prop(self, "g")
        col = row.column()
        col.prop(self, "h")
        row = colm.row()
        col = row.column()
        col.prop(self, "i")
        col = row.column()
        col.prop(self, "j")
        row = colm.row()
        col = row.column()
        col.prop(self, "k")
        col = row.column()
        col.prop(self, "l")

    def get_sound(self):
        sockets = self.inputs.keys()
        input_values = get_socket_values(self, sockets, self.inputs)
        if connected_node_output(self, 1) is not None:
            dry_vol = connected_node_output(self, 1)["float"]
        else:
            dry_vol = input_values[1]

        if connected_node_output(self, 2) is not None:
            wet_vol = connected_node_output(self, 2)["float"]
        else:
            wet_vol = input_values[2]

        input = connected_node_sound(self, 0)
        if isinstance(input, dict):
            if "sound" in input.keys():
                sound_d = input["sound"]
                sound_w = input["sound"]
                if isinstance(sound_w, aud.Sound):
                    if (
                        any([self.a != 0, self.b != 0,self.c != 0,
                        self.d != 0, self.e != 0, self.f != 0,
                        self.g != 0, self.h != 0,self.i != 0,
                        self.j != 0, self.k != 0, self.l != 0])
                        ):

                        filterSi = [self.a, self.b, self.c, self.d, self.e, self.f]
                        filterSf = [self.g, self.h, self.i, self.j, self.k, self.l]
                        while len(filterSi) > self.filter_n:
                            filterSi.pop(-1)
                        while len(filterSf) > self.filter_n:
                            filterSf.pop(-1)
                        tupleSi = tuple(filterSi)
                        tupleSf = tuple(filterSf)
                        if self.typeB:
                            sound_w = sound_w.filter(tupleSi,tupleSf)
                        else:
                            sound_w = sound_w.filter(tupleSi)
                        sound = mix_dry_wet(sound_d, sound_w, dry_vol, wet_vol)
                        return {"sound": sound}
                    else:
                        return {"sound": sound_d}
        return None
