import bpy

class CM_OT_NoteMovePosition(bpy.types.Operator):
    bl_idname = "cm_audio.note_move_position"
    bl_label = "Move Note"
    bl_description = "Move Selected Note"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        cm = bpy.context.scene.cm_pg
        cm_node = context.node
        note_name = f"{cm_node.note_list}{cm_node.octave}"
        input = cm_node.execute()
        if isinstance(input, dict):
            if "vector_loc" in input.keys():
                collection = input["collection"]
                vector_loc = input["vector_loc"]
                duration = input["note_dur"] * int(cm.note_den)
                size = duration / 10
            else:
                self.report({"ERROR"}, "No Vector Input")
                return {"FINISHED"}
        else:
            self.report({"ERROR"}, "Invalid Input")
            return {"FINISHED"}

        objs = context.view_layer.objects.selected
        if len(objs) == 1:
            obj = objs[0]
            if "note" in obj.name:
                obj.location = vector_loc
                if cm_node.resize:
                    obj.dimensions.x = size
                    obj.name = f"note-{duration}"
                self.report({"INFO"}, "Note Moved")
                return {"FINISHED"}
            else:
                self.report({"ERROR"}, "Selected Object is not a Note")
        else:
            self.report({"ERROR"}, "Select only 1 Note")
            return {"FINISHED"}
