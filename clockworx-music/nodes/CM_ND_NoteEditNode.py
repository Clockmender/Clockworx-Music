import bpy
from .._base.base_node import CM_ND_BaseNode
from mathutils import Vector

from bpy.props import (
    StringProperty,
    IntProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
    BoolProperty,
)
from ..cm_functions import (
    check_note,
    connected_node_output,
    get_index,
)

class CM_ND_NoteEditNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio_note_edit_node"
    bl_label = "Edit Pianoroll"
    bl_width_default = 300
    """Edit Notes in the Pianoroll"""

    octave : IntProperty(name="Octave", min=-10, max=10)
    note_list : EnumProperty(
        items=(
            ("c", "C", "Note C"),
            ("cs", "CS", "Note CS"),
            ("d", "D", "Note D"),
            ("ds", "DS", "Note DS"),
            ("e", "E", "Note E"),
            ("f", "F", "Note F"),
            ("fs", "Fs", "Note FS"),
            ("g", "G", "Note G"),
            ("gs", "GS", "Note GS"),
            ("a", "A", "Note A"),
            ("as", "AS", "Note AS"),
            ("b", "B", "Note B"),
        ),
        name="Note Name",
        default="c",
        description="Note Denominator",
    )
    note_dur : FloatProperty(name="Note Length (B)", min=0.001, max=10)
    start_off : IntProperty(name="Start Offset", default=0, min=0)
    bar_num : IntProperty(name="Bar", default=1, min=1)
    offset : IntProperty(name="Offset", default=0)
    resize : BoolProperty(name="Resize", default=False)

    def draw_buttons(self, context, layout):
        box = layout.box()
        row = box.row()
        row.prop(self, "octave")
        row.prop(self, "note_list")
        row = box.row()
        row.label(text="Note Length in Beats")
        row.prop(self, "note_dur", text="")
        layout.label(text="")
        box = layout.box()
        row = box.row()
        row.label(text="Add Note Paramters:")
        row = box.row()
        row.prop(self,"start_off")
        row.prop(self, "bar_num")
        row.prop(self, "offset")
        row = box.row()
        row.operator("cm_audio.note_edit_position", icon="SOUND")
        row.operator("cm_audio.note_edit_place", icon="SOUND")
        row = box.row()
        row.operator("cm_audio.note_move_position", icon="SOUND")
        row.prop(self, "resize")
        row = box.row()
        split = row.split(factor=0.5, align=True)
        split.operator("cm_audio.note_copy_position", icon="SOUND")
        split.label(text="Offset by 'Bar'&'Octave'")

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.collection", "Collection")
        self.outputs.new("cm_socket.generic", "Note Info")

    def execute(self):
        cm = bpy.context.scene.cm_pg
        input = connected_node_output(self, 0)
        if isinstance(input, dict):
            objects = []
            if "collections" in input.keys():
                collection = input["collections"]
                if isinstance(collection, list):
                    return None
        output = {}
        # 1 beat in units
        note_name = f"{self.note_list}{self.octave}"
        test_note = check_note(note_name)
        if test_note:
            output["note_name"] = note_name
            valid = "Valid"
        else:
            output["note_name"] = ""
            valid = "Invalid"
        output["note_dur"] = self.note_dur
        output["note_vol"] = 1
        output["note_freq"] = 0
        output["note_rev"] = False
        output["collection"] = collection
        if cm.bar_len > 0:
            x_pos = (
                (self.start_off * 0.1) + (cm.bar_len * (self.bar_num - 1))
                + (self.offset * 0.1)
                )
            y_pos = (get_index(note_name) + 3) / 10
            vector_loc = Vector((x_pos, y_pos, 0))
            output["vector_loc"] = vector_loc
        else:
            return None
        return output

    def output(self):
        return self.execute()
