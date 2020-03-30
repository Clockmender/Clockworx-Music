import bpy
import aud
from bpy.props import (
    EnumProperty,
    StringProperty,
)
from ..cm_functions import (
    osc_generate,
    get_socket_values,
    connected_node_output,
    get_index,
    get_freq,
    eval_data,
    )


class CM_ND_AudioSoundNode(bpy.types.Node):
    bl_idname = "cm_audio.sound_node"
    bl_label = "Tone Oscillator"
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
        self.inputs.new("cm_socket.float", "Length (B)")
        self.inputs.new("cm_socket.bool", "Reverse")
        self.inputs.new("cm_socket.generic", "Note Data")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "gen_type")
        if self.message != "":
            layout.label(text=self.message, icon="INFO")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sockets = self.inputs.keys()
        input_values = get_socket_values(self, sockets, self.inputs)
        input = connected_node_output(self, 5)
        if input is None:
            output = {}
            output["note_name"] = input_values[0]
            output["note_freq"] = input_values[1]
            output["note_vol"] = input_values[2]
            output["note_dur"] = input_values[3]
            output["note_rev"] = input_values[4]
            input = [output]
        else:
            if isinstance(input, dict):
                input = [input]

        first = True
        sound_out = None
        for notes in input:
            data = eval_data(notes)
            if data[0] == "" and data[1] == 0:
                cm.message = "You MUST Give a Note Name or Frequency"
                return None
            data[0] = data[0].split(",")
            first_note = True
            for i in range(len(data[0])):
                index = get_index(data[0][i])
                if index in range(0, 107):
                    freq = get_freq(index)
                else:
                    freq = 0
                if freq > 0:
                    data[1] = freq
                sound = osc_generate(data, self.gen_type, cm.samples)
                sound = sound.volume(data[2])
                sound = sound.limit(0, (data[3] * (60 / cm.bpm)))
                sound = sound.rechannel(cm.sound_channels)
                if data[4]:
                    sound = sound.reverse()
                if first_note:
                    sound_list = sound
                    first_note = False
                else:
                    sound_list = sound_list.join(sound)
                if first:
                    sound_out = sound_list
                    first = False
                else:
                    sound_out = sound_out.mix(sound_list)
        return {"sound": sound_out}

    def output(self):
        return self.get_sound()
