import bpy
from bpy.props import (
    EnumProperty,
    StringProperty,
    IntProperty,
)
from ..cm_functions import (
    get_socket_values,
    get_chord_ind,
    get_freq,
    osc_generate,
    )


class CM_ND_AudioChordNode(bpy.types.Node):
    bl_idname = "cm_audio.chord_node"
    bl_label = "Chord Generator"
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
    message : StringProperty(name="Message")
    num_notes : IntProperty(name="Notes #", default=3, min=3, max=5)

    def init(self, context):
        self.inputs.new("cm_socket.text", "Note")
        self.inputs.new("cm_socket.float", "Volume")
        self.inputs.new("cm_socket.float", "Length (B)")
        self.inputs.new("cm_socket.bool", "Reverse")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "gen_type")
        if self.message != "":
            layout.prop(self, "message", text="")
        layout.prop(self, "num_notes")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sockets = self.inputs.keys()
        input_values = get_socket_values(self, sockets, self.inputs)
        index_list = get_chord_ind(input_values[0], self.num_notes)
        input_values.insert(1, 0)
        bps = cm.bpm / 60
        duration = input_values[3] * (1 / bps)
        for i in range(0, self.num_notes):
            input_values[1] = get_freq(index_list[i])
            snd = osc_generate(input_values, self.gen_type, cm.samples)
            snd = snd.volume(input_values[2])
            snd = snd.limit(0, duration)
            snd = snd.rechannel(cm.sound_channels)
            if i == 0:
                sound = snd
            else:
                sound = sound.mix(snd)
        if input_values[4]:
            sound = sound.reverse()
        return sound
