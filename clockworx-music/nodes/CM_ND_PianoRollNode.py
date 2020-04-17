import bpy
import aud
from .._base.base_node import CM_ND_BaseNode

from bpy.props import (
    IntProperty,
    FloatProperty,
    EnumProperty,
    StringProperty,
    BoolProperty,
)
from ..cm_functions import (
    connected_node_output,
    osc_generate,
    get_note,
    get_freq,
)
from ..cm_functions import start_piano


class CM_ND_PianoRollNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.piano_roll_node"
    bl_label = "Evaluate Piano Roll"
    bl_icon = "SPEAKER"

    frame_num: bpy.props.IntProperty(name="Frame", description="System Variable, do not set")
    volume : FloatProperty(name="Volume", default=1, min=0.1)
    note_rev: BoolProperty(name="Reverse", default=False)

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.collection", "Collection")
        self.outputs.new("cm_socket.note", "Note Data")

    def draw_buttons(self, context, layout):
        layout.prop(self, "volume")
        layout.prop(self, "note_rev")

    def execute(self):
        scene = bpy.context.scene
        cm = bpy.context.scene.cm_pg
        input = connected_node_output(self, 0)
        if isinstance(input, dict):
            objects = []
            if "collections" in input.keys():
                collections = input["collections"]
                if not isinstance(collections, list):
                    collection = collections
                else:
                    return None
        else:
            return None
        frame_num = bpy.context.scene.frame_current - bpy.context.scene.frame_start
        pointer = bpy.data.objects[cm.pointer]
        note_list = []
        if pointer is None:
            return None

        pointer_loc = pointer.location.x

        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].region_3d.view_location.x = pointer_loc + cm.view_offset

        if frame_num >= 0 and frame_num < bpy.context.scene.frame_end:
            pointer.location.x = frame_num * 0.1
        else:
            pointer.location.x = 0

        obj_list = ([o for o in collection.objects if "note" in o.name
            and pointer.location.x - 0.049 < o.location.x < pointer.location.x + 0.049]
            )
        num = 0
        if len(obj_list) > 0:
            for obj in obj_list:
                #get note_name
                note_name = get_note(int((obj.location.y * 10) + 9), 0)
                freq = get_freq(int((obj.location.y * 10) + 9))
                length = obj.dimensions.x * 10 * cm.time_note_min * cm.bpm / 60
                output = {}
                output["note_name"] = note_name
                output["note_freq"] = freq
                output["note_vol"] = round(self.volume, 5)
                output["note_dur"] = round(length, 5)
                output["note_rev"] = self.note_rev
                note_list.append(output)
                num = num + 1
        return note_list

    def output(self):
        return self.execute()
