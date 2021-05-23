import bpy
import aud
from bpy.types import (
    NodeSocketFloat,
    NodeSocketBool,
)
from .._base.base_node import CM_ND_BaseNode
from ..cm_functions import (
    get_socket_values,
    get_freq,
    get_index,
    osc_generate,
)
from bpy.props import (
    StringProperty,
    FloatProperty,
    EnumProperty,
)

class CM_ND_AudioVocoderNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.vocoder_node"
    bl_label = "Vocoder"
    bl_icon = "SPEAKER"

    file_name_prop: bpy.props.StringProperty(subtype="FILE_PATH", name="File", default="//")
    gen_type: EnumProperty(
        items=(
            ("sine", "Sine", "Sine Waveform"),
            ("triangle", "Triangle", "Triangle Waveform"),
            ("square", "Square", "Square Waveform"),
            ("sawtooth", "Sawtooth", "Sawtooth Waveform"),
        ),
        name="Waveform",
        default="sine",
        description="Waveform for Sound",
    )
    note_name: StringProperty(name="Note", default="c4",
        description="Leave Blank for FB Frequency")
    fb_freq : FloatProperty(name="Fallback Frequency", default=10.0, min=0.1, max=10000)

    def init(self, context):
        super().init(context)
        self.inputs.new("NodeSocketFloat", "Volume")
        self.inputs.new("NodeSocketFloat", "Start (B)")
        self.inputs.new("NodeSocketFloat", "Length (B)")
        self.inputs.new("NodeSocketBool", "Reverse")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "file_name_prop")
        layout.prop(self, "gen_type")
        layout.prop(self, "note_name")
        layout.prop(self, "fb_freq")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sockets = self.inputs.keys()
        input_values = get_socket_values(self, sockets, self.inputs)
        cm = bpy.context.scene.cm_pg
        sound = aud.Sound.file(bpy.path.abspath(self.file_name_prop))
        sound = sound.resample(cm.samples, False)
        sound = sound.volume(input_values[0])
        start = input_values[1] * (60 / cm.bpm)
        stop = start + (input_values[2] * (60 / cm.bpm))
        sound = sound.limit(start, stop)
        if input_values[3]:
            sound = sound.reverse()
        sound = sound.rechannel(cm.sound_channels)
        # Modulate Sound
        index = get_index(self.note_name)
        if index in range(0, 107):
            freq = get_freq(index)
        else:
            freq = self.fb_freq
        sound_mod = osc_generate(["",freq], self.gen_type, cm.samples)
        sound_mod = sound_mod.volume(input_values[0])
        sound_mod = sound_mod.limit(start, stop)
        if input_values[3]:
            sound_mod = sound_mod.reverse()
        sound_mod = sound_mod.rechannel(cm.sound_channels)
        sound = sound.modulate(sound_mod)
        return {"sound": sound}

    def output(self):
        return self.get_sound()
