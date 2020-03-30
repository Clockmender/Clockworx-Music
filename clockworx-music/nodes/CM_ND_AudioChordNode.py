import bpy
from bpy.props import (
    EnumProperty,
    StringProperty,
    IntProperty,
)
from ..cm_functions import (
    get_socket_values,
    connected_node_output,
    get_chord_ind,
    get_freq,
    osc_generate,
    eval_data,
    )


class CM_ND_AudioChordNode(bpy.types.Node):
    bl_idname = "cm_audio.chord_node"
    bl_label = "Chord Oscillator"
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
        self.inputs.new("cm_socket.generic", "Note Data")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "gen_type")
        if self.message != "":
            layout.label(text=self.message, icon="INFO")
        layout.prop(self, "num_notes")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sockets = self.inputs.keys()
        input_values = get_socket_values(self, sockets, self.inputs)
        input_values.insert(1, 0)
        input = connected_node_output(self, 4)
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
            if data[0] == "":
                cm.message = "You MUST Give a Note Name"
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
            if first:
                sound_out = sound
                first = False
            else:
                sound_out = sound_out.mix(sound)
        return {"sound": sound_out}

    def output(self):
        return self.get_sound()
