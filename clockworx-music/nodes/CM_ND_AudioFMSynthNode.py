import bpy
import aud
from bpy.props import (
   EnumProperty,
   BoolProperty,
   FloatProperty,
   StringProperty,
)

from ..cm_functions import (
    osc_generate,
    get_socket_values,
    get_index,
    get_note,
    get_freq,
    get_chord,
    eval_data,
    )

enum = (
    ("sine", "Sine", "Sine Waveform"),
    ("triangle", "Triangle", "Triangle Waveform"),
    ("square", "Square", "Square Waveform"),
    ("sawtooth", "Sawtooth", "Sawtooth Waveform"),
)

class CM_ND_AudioFMSynthNode(bpy.types.Node):
    bl_idname = "cm_audio.fm_synth"
    bl_label = "FM Synthesiser"
    bl_width_default = 450

    message   : StringProperty()
    osc1: EnumProperty(
        items=enum,
        name="Waveform",
        default="sine",
        description="Waveform for Sound",
    )
    osc2: EnumProperty(
        items=enum,
        name="Waveform",
        default="sine",
        description="Waveform for Sound",
    )
    osc3: EnumProperty(
        items=enum,
        name="Waveform",
        default="sine",
        description="Waveform for Sound",
    )
    osc4: EnumProperty(
        items=enum,
        name="Waveform",
        default="sine",
        description="Waveform for Sound",
    )
    dir2      : BoolProperty(name="Up 2",default=True)
    dir3      : BoolProperty(name="Up 3",default=True)
    dir4      : BoolProperty(name="Up 4",default=True)
    vol1      : FloatProperty(name="Vol 1",default=1,min=0,max=2)
    vol2      : FloatProperty(name="Vol 2",default=1,min=0,max=2)
    vol3      : FloatProperty(name="Vol 3",default=1,min=0,max=2)
    vol4      : FloatProperty(name="Vol 4",default=1,min=0,max=2)
    #sto1      : FloatProperty(name="Off 1",default=0,min=0,max=1)
    sto2      : FloatProperty(name="Del 2",default=0,min=0,max=1)
    sto3      : FloatProperty(name="Del 3",default=0,min=0,max=1)
    sto4      : FloatProperty(name="Del 4",default=0,min=0,max=1)

    # Object bits:
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

    def draw_buttons(self, context, layout):
        row = layout.row()
        col1 = row.column()
        col1.prop(self, "osc1")
        col1.prop(self, "vol1")
        #col1.prop(self,"sto1")

        col2 = row.column()
        col2.prop(self, "osc2")
        col2.prop(self, "vol2")
        col2.prop(self,"sto2")
        col2.prop(self, "dir2")

        col3 = row.column()
        col3.prop(self, "osc3")
        col3.prop(self, "vol3")
        col3.prop(self,"sto3")
        col3.prop(self, "dir3")

        col4 = row.column()
        col4.prop(self, "osc4")
        col4.prop(self, "vol4")
        col4.prop(self,"sto4")
        col4.prop(self, "dir4")

        layout.label(text=self.message,icon="NONE")
        box = layout.box()
        row = box.row()
        row.prop(self, "control_name")
        row.operator("cm_audio.get_name", text="", icon="STYLUS_PRESSURE")
        row.prop(self, "anim_type")
        row = box.row()
        row.prop(self, "control_axis")
        row.prop(self, "trigger_value")

    def init(self, context):
        self.inputs.new("cm_socket.text", "Note") # 0
        self.inputs.new("cm_socket.float", "Frequency") # 1
        self.inputs.new("cm_socket.float", "Master Volume") # 2
        self.inputs.new("cm_socket.float", "Length (B)") # 3
        self.inputs.new("cm_socket.bool", "Reverse") # 4
        self.inputs.new("cm_socket.sound", "Note Data")
        self.outputs.new("cm_socket.sound", "Audio")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sockets = self.inputs.keys()
        input_values = get_socket_values(self, sockets, self.inputs)
        data = eval_data(input_values, 5)
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
                    data[0] = note_name

        vol1 = self.vol1 * data[2]
        vol2 = self.vol2 * data[2]
        vol3 = self.vol3 * data[2]
        vol4 = self.vol4 * data[2]
        if data[0] == "" and data[1] == 0:
            sound_out = None
        else:
            bps = cm.bpm / 60
            index = get_index(data[0])
            note_name = get_note(index, 0)
            freq_list = get_chord(note_name, -4)
            # Carrier Signal
            sound_1 = osc_generate([0, freq_list[3]], self.osc1, cm.samples)
            sound_1 = sound_1.limit(0, (data[3] / bps)).volume(self.vol1)

            r = 4 if self.dir2 else 2
            sound_2 = osc_generate([0, freq_list[r]], self.osc2, cm.samples)
            sound_2 = sound_2.limit(0, (data[3] / bps)).volume(self.vol2)
            sound_2 = sound_2.delay(self.sto2)
            sound_2 = sound_1.modulate(sound_2)

            r = 5 if self.dir3 else 1
            sound_3 = osc_generate([0, freq_list[r]], self.osc3, cm.samples)
            sound_3 = sound_3.limit(0, (data[3] / bps)).volume(self.vol3)
            sound_3 = sound_3.delay(self.sto3)
            sound_3 = sound_1.modulate(sound_3)

            r = 6 if self.dir4 else 0
            sound_4 = osc_generate([0, freq_list[r]], self.osc4, cm.samples)
            sound_4 = sound_4.limit(0, (data[3] / bps)).volume(self.vol4)
            sound_4 = sound_4.delay(self.sto4)
            sound_4 = sound_1.modulate(sound_4)

            sound_out = sound_1.mix(sound_2).mix(sound_3).mix(sound_4)
            sound_out = sound_out.volume(data[2]).rechannel(cm.sound_channels)
            if input_values[4]:
                sound_out = sound_out.reverse()
        return sound_out
