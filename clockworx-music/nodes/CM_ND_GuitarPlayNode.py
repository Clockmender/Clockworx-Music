import bpy
from .._base.base_node import CM_ND_BaseNode
from bpy.props import (
    BoolProperty,
    EnumProperty,
)
from ..cm_functions import connected_node_output
from mathutils import Vector

class CM_ND_GuitarPlayNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.midi_guitar_play_node"
    bl_label = "Guitar Play"
    bl_icon = "SPEAKER"
    bl_width_default = 200

    g_mode : EnumProperty(
        items=(
            ("six", "Six String", "Six String Guitar"),
            ("four", "Four String", "Bass Guitar"),
        ),
        name="Guitar Mode",
        default="six",
        description="Guitar Mode",

    )
    use_bones : BoolProperty(name="Use Bones", default=False)

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.guitar", "Guitar Data")
        self.inputs.new("cm_socket.collection", "Frets")
        self.inputs.new("cm_socket.object", "Note Location Object")
        self.inputs.new("cm_socket.bone", "Note Locatio Bone")
        self.inputs.new("cm_socket.object", "Plectrum Object")
        self.inputs.new("cm_socket.bone", "Plectrum Bone")

    def draw_buttons(self, context, layout):
        layout.prop(self, "g_mode")
        layout.prop(self, "use_bones")

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

        if not self.use_bones:
            note_obj = connected_node_output(self, 2)
            if note_obj is None:
                return None
            if isinstance(note_obj, dict):
                if "objects" in note_obj.keys():
                    note_obj = note_obj["objects"]
                else:
                    return None
            plect_obj = connected_node_output(self, 4)
            if plect_obj is None:
                return None
            if isinstance(plect_obj, dict):
                if "objects" in plect_obj.keys():
                    plect_obj = plect_obj["objects"]
                else:
                    return None
        else:
            note_obj = connected_node_output(self, 3)
            if note_obj is None:
                return None
            if isinstance(note_obj, dict):
                if "bones" in note_obj.keys():
                    note_obj = note_obj["bones"]
                    if isinstance(note_obj, list):
                        return None
                else:
                    return None
            plect_obj = connected_node_output(self, 5)
            if plect_obj is None:
                return None
            if isinstance(plect_obj, dict):
                if "bones" in plect_obj.keys():
                    plect_obj = plect_obj["bones"]
                    if isinstance(plect_obj, list):
                        return None
                else:
                    return None

        if guitar_data is not None and frets is not None:
            if isinstance(guitar_data, dict):
                if self.g_mode == "six":
                    guitar_data = guitar_data["six_s"]
                else:
                    guitar_data = guitar_data["bass"]
                string = guitar_data[0]
                fret = guitar_data[1]
                pfret_obj = [o for o in frets.objects if "F24" in o.name]
                if len(pfret_obj) > 0:
                    pfret_obj = pfret_obj[0]
                else:
                    return None

                nut_obj = [o for o in frets.objects if "NUT" in o.name]
                if len(nut_obj) > 0:
                    nut_obj = nut_obj[0]
                else:
                    return None

                if bpy.context.scene.frame_current <= bpy.context.scene.frame_start:
                    if not self.use_bones:
                        note_obj.location = nut_obj.location
                        plect_obj.location = pfret_obj.location
                    else:
                        note_obj.location = Vector((0, 0, 0))
                        plect_obj.location = Vector((0, 0, 0))
                    return None
                if string == "null" or fret == "null":
                    if not self.use_bones:
                        plect_obj.location = pfret_obj.location
                    else:
                        plect_obj.location = Vector((0, 0, 0))

                fret_obj = [o for o in frets.objects if fret in o.name]
                if len(fret_obj) > 0:
                    fret_obj = fret_obj[0]
                else:
                    return None

                max_dim = max(fret_obj.dimensions)
                min_dim = min(fret_obj.dimensions)
                ind_dim = [i for i, j in enumerate(fret_obj.dimensions) if j == max_dim]
                off_dim = [i for i, j in enumerate(fret_obj.dimensions) if j == min_dim]
                note_loc = fret_obj.matrix_world.decompose()[0]
                max_plect = max(pfret_obj.dimensions)
                plec_loc = pfret_obj.matrix_world.decompose()[0]

                if self.g_mode == "six":
                    inc_f = max_dim / 12
                    inc_p = max_plect / 12
                else:
                    inc_f = max_dim / 8
                    inc_p = max_plect / 8
                if string.split("_")[0] == "El":
                    offset = inc_f * 5 if self.g_mode == "six" else inc_f * 3
                    p_offset = inc_p * 5 if self.g_mode == "six" else inc_p * 3
                if string.split("_")[0] == "A":
                    offset = inc_f * 3 if self.g_mode == "six" else inc_f * 1
                    p_offset = inc_p * 3 if self.g_mode == "six" else inc_p * 1
                if string.split("_")[0] == "D":
                    offset = inc_f * 1 if self.g_mode == "six" else inc_f * -1
                    p_offset = inc_p * 1 if self.g_mode == "six" else inc_p * -1
                if string.split("_")[0] == "G":
                    offset = inc_f * -1 if self.g_mode == "six" else inc_f * -3
                    p_offset = inc_p * -1 if self.g_mode == "six" else inc_p * -3
                if string.split("_")[0] == "B":
                    offset = inc_f * -3 if self.g_mode == "six" else 0
                    p_offset = inc_p * -3 if self.g_mode == "six" else 0
                if string.split("_")[0] == "Et":
                    offset = inc_f * -5 if self.g_mode == "six" else 0
                    p_offset = inc_p * -5 if self.g_mode == "six" else 0

                plec_loc[ind_dim[0]] = plec_loc[ind_dim[0]] + p_offset
                if not self.use_bones:
                    note_loc[ind_dim[0]] = note_loc[ind_dim[0]] + offset
                    note_obj.location = note_loc
                    plect_obj.location = plec_loc
                else:
                    note_loc[off_dim[0]] = (fret_obj.location[off_dim[0]] -
                                            nut_obj.location[off_dim[0]])
                    note_loc[ind_dim[0]] = (fret_obj.location[ind_dim[0]] -
                                            nut_obj.location[ind_dim[0]] +
                                            offset)
                    note_obj.location = note_loc
                    plect_obj.location = plec_loc - pfret_obj.location
        else:
            return None
