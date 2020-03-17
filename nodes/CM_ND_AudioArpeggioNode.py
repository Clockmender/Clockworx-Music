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
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "gen_type")
        layout.prop(self, "num_notes")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sockets = self.inputs.keys()
        input_values = get_socket_values(self, sockets, self.inputs)
        freq_list = get_chord(input_values[0], self.num_notes)
        bps = cm.bpm / 60
        duration = input_values[2] * (1 / bps)
        if input_values[3]:
            freq_list = freq_list[::-1]
        for r in range(len(freq_list)):
            snd = osc_generate([0, freq_list[r]], self.gen_type, cm.samples)
            snd = snd.limit(0, duration).volume(input_values[1])
            if r == 0:
                sound = snd
            else:
                sound = sound.join(snd)
        if input_values[3]:
            sound = sound.reverse()
        return sound
