import bpy
import aud
from bpy.props import (
    EnumProperty,
    StringProperty,
)
from ..cm_functions import (
    osc_generate,
    get_socket_values,
    get_index,
    get_freq,
    )


class CM_ND_AudioSoundNode(bpy.types.Node):
    bl_idname = "cm_audio.sound_node"
    bl_label = "Sound Generator"
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

    def init(self, context):
        self.inputs.new("cm_socket.text", "Note")
        self.inputs.new("cm_socket.float", "Frequency")
        self.inputs.new("cm_socket.float", "Volume")
        self.inputs.new("cm_socket.float", "Delay (B)")
        self.inputs.new("cm_socket.float", "Length (B)")
        self.inputs.new("cm_socket.bool", "Reverse")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "gen_type")
        if self.message != "":
            layout.prop(self, "message", text="")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sockets = self.inputs.keys()
        input_values = get_socket_values(self, sockets, self.inputs)
        input_values[0] = input_values[0].split(",")
        # notes are now a list
        first = True
        for i in range(len(input_values[0])):
            index = get_index(input_values[0][i])
            if index in range(0, 107):
                freq = get_freq(index)
            else:
                freq = 0
            if freq > 0:
                input_values[1] = freq
            sound = osc_generate(input_values, self.gen_type, cm.samples)
            sound = sound.volume(input_values[2])
            bps = cm.bpm / 60
            sound = sound.limit(0, (input_values[4] / bps))
            sound = sound.delay(input_values[3] / bps)
            sound = sound.rechannel(cm.sound_channels)
            if input_values[5]:
                sound = sound.reverse()
            if first:
                sound_out = sound
                first = False
            else:
                sound_out = sound_out.join(sound)
        return sound_out
