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
    eval_data,
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
        self.inputs.new("cm_socket.sound", "Note Data")
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
        input_values.insert(1, 0)
        data = eval_data(input_values, 5)
        if data[0] == "" and data[1] == 0:
            return None

        index_list = get_chord_ind(data[0], self.num_notes)
        duration = data[3] * (60 / cm.bpm)
        for i in range(0, self.num_notes):
            data[1] = get_freq(index_list[i])
            snd = osc_generate(data, self.gen_type, cm.samples)
            snd = snd.volume(data[2])
            snd = snd.limit(0, duration)
            snd = snd.rechannel(cm.sound_channels)
            if i == 0:
                sound = snd
            else:
                sound = sound.mix(snd)
        if data[4]:
            sound = sound.reverse()
        return sound
