import bpy
from .._base.base_node import CM_ND_BaseNode

from bpy.props import (
    IntProperty,
    FloatProperty,
    StringProperty,
    BoolProperty,
    EnumProperty,
)
from ..cm_functions import (
    connected_node_output,
    get_note,
)


class CM_ND_MidiBakeNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.midi_bake_node"
    bl_label = "MIDI Bake"
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
    sequence_channel : IntProperty(name="VSE Channel", default=1, description="VSE Channel")
    add_file : BoolProperty(name="Add to VSE", default=False)
    strip_name : StringProperty(name="Strip Name", default="")
    volume : FloatProperty(name="Volume", default=1.0)
    make_all : BoolProperty(name="Process All Channels", default=False)
    label_cont : BoolProperty(name="Label Controls", default=False)

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.collection", "Collection")
        self.inputs.new("cm_socket.material", "Material")
        self.outputs.new("cm_socket.generic", "Data")

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

        layout.separator()
        row = layout.row()
        split = row.split(factor=0.3, align=True)
        split.label(text="")
        split.operator("cm_audio.create_daw_notes", icon="FILE_NEW")

        layout.label(text="")
        if self.message1 != "":
            layout.label(text=self.message1, icon="INFO")
        if self.message2 != "":
            layout.label(text=self.message2, icon="INFO")

    def function(self):
        cm = bpy.context.scene.cm_pg
        input_1 = connected_node_output(self, 0)
        if isinstance(input_1, dict):
            if "collections" in input_1.keys():
                collections = input_1["collections"]
                if not isinstance(collections, list):
                    collection = collections
                else:
                    collection = None
        else:
            collection = None
        input_2 = connected_node_output(self, 1)
        if isinstance(input_2, dict):
            if "material" in input_2.keys():
                material = input_2["material"]
        else:
            material = None
        output = {}
        output["collections"] = collection
        output["midi_file"] = self.midi_file_name
        output["sound_file"] = self.sound_file_name
        output["write_file"] = self.write_name
        output["material"] = material
        output["event_dict"] = cm.event_dict
        return output

    def output(self):
        return self.function()
