import bpy
import aud
from bpy.props import (
    EnumProperty,
    StringProperty,
    IntProperty,
)
from ..cm_functions import (
    osc_generate,
    get_socket_values,
    get_chord,
    eval_data,
    )


class CM_ND_AudioArpeggioNode(bpy.types.Node):
    bl_idname = "cm_audio.arpeggio_node"
    bl_label = "Arpeggio Generator"
    bl_icon = "SPEAKER"

    gen_type: EnumProperty(
        items=(
            ("sine", "Sine", "Sine Waveform"),
            ("triangle", "Triangle", "Triangle Waveform"),
            ("square", "Square", "Square Waveform"),
            ("sawtooth", "Sawtooth", "Sawtooth Waveform"),
            ("silence", "Silence", "Silence - no Waveform"),
        ),
        name="Waveform",
        default="sine",
        description="Waveform for Sound",
    )
    num_notes : IntProperty(name="Notes #", default=3, min=3, max=9)

    def init(self, context):
        self.inputs.new("cm_socket.text", "Note")
        self.inputs.new("cm_socket.float", "Volume")
        self.inputs.new("cm_socket.float", "Length (B)")
        self.inputs.new("cm_socket.bool", "Reverse")
        self.inputs.new("cm_socket.sound", "Note Data")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "gen_type")
        layout.prop(self, "num_notes")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sockets = self.inputs.keys()
        input_values = get_socket_values(self, sockets, self.inputs)
        input_values.insert(1, 0)
        data = eval_data(input_values, 5)
        if data[0] == "" and data[1] == 0:
            return None

        freq_list = get_chord(data[0], self.num_notes)
        duration = data[3] * (60 / cm.bpm)
        if data[4]:
            freq_list = freq_list[::-1]
        for r in range(len(freq_list)):
            snd = osc_generate([0, freq_list[r]], self.gen_type, cm.samples)
            snd = snd.limit(0, duration).volume(data[2])
            if r == 0:
                sound = snd
            else:
                sound = sound.join(snd)
        if data[4]:
            sound = sound.reverse()
        return sound
