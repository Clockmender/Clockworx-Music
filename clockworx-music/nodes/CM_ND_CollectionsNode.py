import bpy
from bpy.props import (
    StringProperty,
    IntProperty,
)

class CM_ND_CollectionsNode(bpy.types.Node):
    bl_idname = "cm_audio.collections_node"
    bl_label = "Collection(s)"
    bl_icon = "SPEAKER"

    search : StringProperty(name="Search", default="")
    ret_num : IntProperty(name="Index", default=-1, min=-1,
        description="-1 = All")
    message : StringProperty()

    def draw_buttons(self, context, layout):
        layout.prop(self, "search")
        layout.prop(self, "ret_num")
        layout.label(text=self.message, icon="INFO")

    def init(self, context):
        self.outputs.new("cm_socket.collection", "Collections")

    def execute(self):
        collections = [c for c in bpy.data.collections if self.search in c.name]
        if len(collections) > 0:
            if len(collections) == 1:
                self.message = f"'{collections[0].name}' Returned"
            else:
                self.message = "List Returned"
            if self.ret_num == -1:
                return {"collections": collections}
            elif len(collections) > self.ret_num:
                self.message = f"'{collections[self.ret_num].name}' Returned"
                return {"collections": collections[self.ret_num]}

        self.message = "Nothing Returned"
        return None

    def output(self):
        return self.execute()
