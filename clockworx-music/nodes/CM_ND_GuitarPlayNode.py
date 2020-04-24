import bpy
from .._base.base_node import CM_ND_BaseNode
from bpy.props import (
    BoolProperty,
)
from ..cm_functions import connected_node_output
from mathutils import Vector

class CM_ND_GuitarPlayNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.midi_guitar_play_node"
    bl_label = "Guitar Play"
    bl_icon = "SPEAKER"
    bl_width_default = 200

    six_string : BoolProperty(name="6-String, or Bass", default=True)

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.guitar", "Guitar Data")
        self.inputs.new("cm_socket.collection", "Frets")
        self.inputs.new("cm_socket.object", "Note Loc Obj")
        self.inputs.new("cm_socket.object", "Plectrum Obj")

    def draw_buttons(self, context, layout):
        layout.prop(self, "six_string")

    def execute(self):
        cm = bpy.context.scene.cm_pg
        guitar_data = connected_node_output(self, 0)
        frets = connected_node_output(self, 1)
        if frets is None:
            return None
        if isinstance(frets, dict):
            if "collections" in frets.keys():
                frets = frets["collections"]
            else:
                return None

        note_obj = connected_node_output(self, 2)
        if note_obj is None:
            return None
        if isinstance(note_obj, dict):
            if "objects" in note_obj.keys():
                note_obj = note_obj["objects"]
            else:
                return None

        plect_obj = connected_node_output(self, 3)
        if plect_obj is None:
            return None
        if isinstance(plect_obj, dict):
            if "objects" in plect_obj.keys():
                plect_obj = plect_obj["objects"]
            else:
                return None

        if guitar_data is not None and frets is not None and plect_obj is not None:
            if isinstance(guitar_data, dict):
                if self.six_string:
                    guitar_data = guitar_data["six_s"]
                else:
                    guitar_data = guitar_data["bass"]
                string = guitar_data[0]
                fret = guitar_data[1]
                pfret_obj = frets.objects["F24"]

                if string == "null" or fret == "null":
                    if  bpy.context.scene.frame_current == bpy.context.scene.frame_start:
                        note_obj.location = frets.objects["NUT"].location
                    plect_obj.location = pfret_obj.location
                    return None

                fret_obj = frets.objects[fret]
                max_dim = max(fret_obj.dimensions)
                ind_dim = [i for i, j in enumerate(fret_obj.dimensions) if j == max_dim]
                note_loc = fret_obj.matrix_world.decompose()[0]
                max_plect = max(pfret_obj.dimensions)
                plec_loc = pfret_obj.matrix_world.decompose()[0]

                if self.six_string:
                    inc_f = max_dim / 12
                    inc_p = max_plect / 12
                else:
                    inc_f = max_dim / 8
                    inc_p = max_plect / 8
                if string.split("_")[0] == "El":
                    offset = inc_f * 5 if self.six_string else inc_f * 3
                    p_offset = inc_p * 5 if self.six_string else inc_p * 3
                if string.split("_")[0] == "A":
                    offset = inc_f * 3 if self.six_string else inc_f * 1
                    p_offset = inc_p * 3 if self.six_string else inc_p * 1
                if string.split("_")[0] == "D":
                    offset = inc_f * 1 if self.six_string else inc_f * -1
                    p_offset = inc_p * 1 if self.six_string else inc_p * -1
                if string.split("_")[0] == "G":
                    offset = inc_f * -1 if self.six_string else inc_f * -3
                    p_offset = inc_p * -1 if self.six_string else inc_p * -3
                if string.split("_")[0] == "B":
                    offset = inc_f * -3 if self.six_string else 0
                    p_offset = inc_p * -3 if self.six_string else 0
                if string.split("_")[0] == "Et":
                    offset = inc_f * -5 if self.six_string else 0
                    p_offset = inc_p * -5 if self.six_string else 0

                note_loc[ind_dim[0]] = note_loc[ind_dim[0]] + offset
                plec_loc[ind_dim[0]] = plec_loc[ind_dim[0]] + p_offset
                note_obj.location = note_loc
                plect_obj.location = plec_loc
        else:
            return None

    def output(self):
        return self.execute()
