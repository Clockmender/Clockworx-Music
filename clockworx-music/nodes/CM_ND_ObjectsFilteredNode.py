import bpy
from .._base.base_node import CM_ND_BaseNode

from bpy.props import (
    StringProperty,
    IntProperty,
)
from ..cm_functions import connected_node_output

class CM_ND_ObjectsFilteredNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.objects__filter_node"
    bl_label = "Object(s): Filtered"
    bl_icon = "SPEAKER"

    search : StringProperty(name="Search", default="")
    ret_num : IntProperty(name="Index", default=-1, min= -1,
        description="-1 = All")

    def draw_buttons(self, context, layout):
        layout.label(text="Search for Objects(s)")
        layout.prop(self, "search", text="")
        layout.prop(self, "ret_num")

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.collection", "Collection(s)")
        self.outputs.new("cm_socket.object", "Object(s)")

    def execute(self):
        input = connected_node_output(self, 0)
        if isinstance(input, dict):
            objects = []
            if "collections" in input.keys():
                collections = input["collections"]
                if not isinstance(collections, list):
                    collections = [collections]
                for col in collections:
                    objs = [o for o in col.objects if self.search in o.name]
                    objects.extend(objs)
        else:
            objects = [o for o in bpy.data.objects if self.search in o.name]
        if len(objects) > 0:
            if len(objects) == 1:
                return {"objects": objects[0]}
            elif self.ret_num == -1:
                return {"objects": objects}
            elif len(objects) > self.ret_num:
                return {"objects": objects[self.ret_num]}

        return None

    def output(self):
        return self.execute()

    def get_midi(self):
        return self.execute()
