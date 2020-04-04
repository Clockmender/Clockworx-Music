import bpy

class CM_OT_NoteEditPosition(bpy.types.Operator):
    bl_idname = "cm_audio.note_edit_position"
    bl_label = "Note Location"
    bl_description = "Position View to Note Location"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        cm = bpy.context.scene.cm_pg
        cm_node = context.node
        input = cm_node.execute()
        if isinstance(input, dict):
            if "vector_loc" in input.keys():
                collection = input["collection"]
                vector_loc = input["vector_loc"]
            else:
                self.report({"ERROR"}, "No Vector Input")
                return {"FINISHED"}
        else:
            self.report({"ERROR"}, "Invalid Input")
            return {"FINISHED"}

        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].region_3d.view_location = vector_loc
        self.report({"INFO"}, "View Centred")
        return {"FINISHED"}
