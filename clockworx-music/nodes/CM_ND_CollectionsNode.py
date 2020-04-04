import bpy
from bpy.props import (
    StringProperty,
    IntProperty,
)

class CM_ND_CollectionsNode(bpy.types.Node):
    bl_idname = "cm_audio.collections_node"
    bl_label = "Collection(s) Input"
    bl_icon = "SPEAKER"

    search : StringProperty(name="Search", default="")
    ret_num : IntProperty(name="Index", default=-1, min=-1,
        description="-1 = All")

    def draw_buttons(self, context, layout):
        layout.label(text="Search for Collection(s)")
        layout.prop(self, "search", text="")
        layout.prop(self, "ret_num")

    def init(self, context):
        self.outputs.new("cm_socket.collection", "Collection(s)")

    def execute(self):
        collections = [c for c in bpy.data.collections if self.search in c.name]
        if len(collections) > 0:
            if len(collections) == 1:
                return {"collections": collections[0]}
            if self.ret_num == -1:
                return {"collections": collections}
            elif len(collections) > self.ret_num:
                return {"collections": collections[self.ret_num]}

        return None

    def output(self):
        return self.execute()

    def get_midi(self):
        return self.execute()
