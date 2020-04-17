import bpy
import aud
from bpy.types import (
    NodeSocketString,
    NodeSocketFloat,
    NodeSocketBool,
)
from .._base.base_node import CM_ND_BaseNode
from bpy.props import (
    EnumProperty,
    StringProperty,
    IntProperty,
)
from ..cm_functions import (
    osc_generate,
    get_socket_values,
    connected_node_output,
    get_chord,
    eval_data,
    )


class CM_ND_AudioArpeggioNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.arpeggio_node"
    bl_label = "Arpeggio Oscillator"
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
        super().init(context)
        self.inputs.new("cm_socket.note", "Note Data")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "gen_type")
        layout.prop(self, "num_notes")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        input = connected_node_output(self, 0)
        if input is None:
            return None
        else:
            if isinstance(input, dict):
                input = [input]

        first = True
        sound_out = None
        for notes in input:
            data = eval_data(notes)
            if data is None or data[0] == "":
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
            if first:
                sound_out = sound
                first = False
            else:
                sound_out = sound_out.mix(sound)
            sound_out = sound_out.rechannel(cm.sound_channels)
        return {"sound": sound_out}

    def output(self):
        return self.get_sound()
