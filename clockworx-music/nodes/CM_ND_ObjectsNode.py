import bpy
from bpy.props import (
    StringProperty,
    IntProperty,
)
from ..cm_functions import connected_node_output

class CM_ND_ObjectsNode(bpy.types.Node):
    bl_idname = "cm_audio.objects_node"
    bl_label = "Object(s) from Collection"
    bl_icon = "SPEAKER"

    search : StringProperty(name="Search", default="")
    ret_num : IntProperty(name="Index", default=-1, min= -1,
        description="-1 = All")
    message : StringProperty()

    def draw_buttons(self, context, layout):
        layout.prop(self, "search")
        layout.prop(self, "ret_num")
        layout.label(text=self.message, icon="INFO")

    def init(self, context):
        self.inputs.new("cm_socket.collection", "Collections")
        self.outputs.new("cm_socket.object", "Objects")

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
                self.message = f"'{objects[0].name}' Returned"
            else:
                self.message = "List Returned"
            if self.ret_num == -1:
                return {"objects": objects}
            elif len(objects) > self.ret_num:
                self.message = f"'{objects[self.ret_num].name}' Returned"
                return {"objects": objects[self.ret_num]}

        self.message = "Nothing Returned"
        return None

    def output(self):
        return self.execute()
