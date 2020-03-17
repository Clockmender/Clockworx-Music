import bpy
from bpy.props import (
    IntProperty,
    FloatProperty,
    StringProperty,
    BoolProperty,
    EnumProperty,
    )


class CM_ND_AudioMidiBakeNode(bpy.types.Node):
    bl_idname = "cm_audio.midi_bake_node"
    bl_label = "Clockworx MIDI Bake"
    bl_icon = "SPEAKER"

    use_vel : BoolProperty(name="Use MIDI Velocity", default=False)
    squ_val : BoolProperty(name="Use Square Waveforms", default=True)
    midi_channel: IntProperty(name="Midi Channel", default=2, min=2)
    time_off : FloatProperty(name="Offset (B)", default=0,
        description="Number of Beats offset from start of Song for Sound File")
    suffix : StringProperty(name="Obj Suffix", default="key")
    message1 : StringProperty()
    message2 : StringProperty()

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
    midi_file_name : StringProperty(subtype="FILE_PATH", name="Midi CSV file", default="//")
    sound_file_name : StringProperty(subtype="FILE_PATH", name="Sound file", default="//")
    write_name : StringProperty(subtype="FILE_PATH", name="Ouptut File Name", default="//")
    sequence_channel : IntProperty(name="Channel", default=1, description="VSE Channel")
    add_file : BoolProperty(name="Add to VSE", default=False)
    strip_name : StringProperty(name="Strip Name", default="")
    volume : FloatProperty(name="Volume", default=1.0)
    make_all : BoolProperty(name="All Channels", default=False)
    label_cont : BoolProperty(name="Label Controls", default=False)

    def draw_buttons(self, context, layout):
        cm_pg = context.scene.cm_pg
        layout.context_pointer_set("audionode", self)
        row = layout.row()
        row.prop(cm_pg, "mid_c")
        row.prop(self, "midi_channel")
        row = layout.row()
        row.prop(self, "use_vel")
        row.prop(self, "squ_val")

        layout.prop(self, "midi_file_name")
        layout.prop(self, "write_name")
        layout.prop(self, "sound_file_name")
        row = layout.row()
        row.prop(self, "label_cont")
        row.label(text="Control Suffix:")
        row.prop(self, "suffix", text="")
        layout.prop(self, "gen_type")
        row = layout.row()
        row.prop(self, "add_file")
        row.prop(self, "strip_name")
        row = layout.row()
        row.prop(self, "time_off")
        row.prop(self, "sequence_channel")
        row = layout.row()
        split = row.split(factor=0.50, align=True)
        split.label(text="")
        split.prop(self, "volume")
        layout.separator()
        row = layout.row()
        split = row.split(factor=0.3, align=True)
        split.prop(self, "make_all")
        split.operator("cm_audio.create_midi", icon="SOUND")
        row = layout.row()
        split = row.split(factor=0.3, align=True)
        split.label(text="")
        split.operator("cm_audio.create_sound", icon="SPEAKER")
        row = layout.row()
        split = row.split(factor=0.3, align=True)
        split.label(text="")
        split.operator("cm_audio.load_sound", icon="FILE_NEW")

        layout.label(text="")
        if self.message1 != "":
            layout.prop(self, "message1", text="")
        if self.message2 != "":
            layout.prop(self, "message2", text="")
