import bpy
import aud
from bpy.props import (
   FloatProperty,
   BoolProperty,
   IntProperty,
)
from ..cm_functions import (
    connected_node_sound,
)

class CM_ND_AudioIirFirFilter(bpy.types.Node):
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
        self.inputs.new("cm_socket.sound", "Audio")
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
        input = connected_node_sound(self, 0)
        if isinstance(input, dict):
            if "sound" in input.keys():
                sound = input["sound"]
                if isinstance(sound, aud.Sound):
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
                            sound = sound.filter(tupleSi,tupleSf)
                        else:
                            sound = sound.filter(tupleSi)
                        return {"sound": sound}
                    else:
                        return {"sound": sound}
        return None
