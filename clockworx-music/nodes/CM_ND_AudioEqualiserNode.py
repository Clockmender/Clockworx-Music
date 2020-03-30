import bpy
import aud
from bpy.props import (
    FloatProperty,
    IntProperty,
)
from ..cm_functions import connected_node_sound

class CM_ND_AudioEqualiserNode(bpy.types.Node):
    bl_idname = "cm_audio.equaliser_node"
    bl_label = "8 Channel Equaliser"
    bl_width_default = 600
    bl_icon = "SPEAKER"

    vol1 : FloatProperty(default=0.5,min=0,max=2,step=2)
    vol2 : FloatProperty(default=0.5,min=0,max=2,step=2)
    vol3 : FloatProperty(default=0.5,min=0,max=2,step=2)
    vol4 : FloatProperty(default=0.5,min=0,max=2,step=2)
    vol5 : FloatProperty(default=0.5,min=0,max=2,step=2)
    vol6 : FloatProperty(default=0.5,min=0,max=2,step=2)
    vol7 : FloatProperty(default=0.5,min=0,max=2,step=2)
    vol8 : FloatProperty(default=0.5,min=0,max=2,step=2)

    spl1 : IntProperty(default=10)
    spl2 : IntProperty(default=100)
    spl3 : IntProperty(default=400)
    spl4 : IntProperty(default=1000)
    spl5 : IntProperty(default=2000)
    spl6 : IntProperty(default=3500)
    spl7 : IntProperty(default=5500)
    spl8 : IntProperty(default=10000)

    q_factor : FloatProperty(name="Q Factor", default=0.5, min = 0.001, max=1, step=2)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio Collection")

    def draw_buttons(self, context, layout):
        colm = layout.column()
        box = colm.box()

        row = box.row()
        row.label(text="Volumes",icon="OUTLINER_OB_SPEAKER")
        row = box.row()
        for i in range(1,9):
            col = row.column()
            col.label(text="Ch "+str(i))
        row = box.row()
        for i in range(1,9):
            col = row.column()
            col.prop(self,"vol"+str(i))

        row = colm.row()
        row.label(text="")
        box = colm.box()
        row = box.row()
        row.label(text="Frequency Splits (Think Quadratic Scales)",icon="PARTICLE_POINT")
        row = colm.row()
        for i in range(1,9):
            col = row.column()
            col.prop(self,"spl"+str(i))

        row = colm.row()
        row.label(text="")
        row = colm.row()
        split = row.split(factor=0.30, align=True)
        split.prop(self, "q_factor")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        input = connected_node_sound(self, 0)
        if isinstance(input, dict):
            if "sound" in input.keys():
                sound = input["sound"]
                if isinstance(sound, aud.Sound):
                    # Filter the sounds
                    snd1 = sound.highpass(self.spl1, self.q_factor)
                    snd1 = sound.lowpass(self.spl2-1, self.q_factor)
                    snd1 = snd1.volume(self.vol1)

                    snd2 = sound.highpass(self.spl2, self.q_factor)
                    snd2 = snd2.lowpass(self.spl3-1, self.q_factor)
                    snd2 = snd2.volume(self.vol2)

                    snd3 = sound.highpass(self.spl3, self.q_factor)
                    snd3 = snd3.lowpass(self.spl4-1, self.q_factor)
                    snd3 = snd3.volume(self.vol3)

                    snd4 = sound.highpass(self.spl4, self.q_factor)
                    snd4 = snd4.lowpass(self.spl5-1, self.q_factor)
                    snd4 = snd4.volume(self.vol4)

                    snd5 = sound.highpass(self.spl5, self.q_factor)
                    snd5 = snd5.lowpass(self.spl6-1, self.q_factor)
                    snd5 = snd5.volume(self.vol5)

                    snd6 = sound.highpass(self.spl6, self.q_factor)
                    snd6 = snd6.lowpass(self.spl7-1, self.q_factor)
                    snd6 = snd6.volume(self.vol6)

                    snd7 = sound.highpass(self.spl7, self.q_factor)
                    snd7 = snd7.lowpass(self.spl8-1, self.q_factor)
                    snd7 = snd7.volume(self.vol7)

                    snd8 = sound.highpass(self.spl8+1, self.q_factor)
                    snd8 = snd8.volume(self.vol8)
                    # mix the sounds together
                    sound_o = snd1.mix(snd2)
                    sound_o = sound_o.mix(snd3)
                    sound_o = sound_o.mix(snd4)
                    sound_o = sound_o.mix(snd5)
                    sound_o = sound_o.mix(snd6)
                    sound_o = sound_o.mix(snd7)
                    sound_o = sound_o.mix(snd8)

                    sound_dict = {}
                    sound_dict["sound"] = sound_o
                    sound_dict["snd1"] = snd1
                    sound_dict["snd2"] = snd2
                    sound_dict["snd3"] = snd3
                    sound_dict["snd4"] = snd4
                    sound_dict["snd5"] = snd5
                    sound_dict["snd6"] = snd6
                    sound_dict["snd7"] = snd7
                    sound_dict["snd8"] = snd8

                    return sound_dict
        return None

    def output(self):
        return self.get_sound()
