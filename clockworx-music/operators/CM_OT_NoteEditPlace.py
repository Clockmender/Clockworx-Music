import bpy

class CM_OT_NoteEditPlace(bpy.types.Operator):
    bl_idname = "cm_audio.note_edit_place"
    bl_label = "New Note"
    bl_description = "Place Note"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        cm = bpy.context.scene.cm_pg
        cm_node = context.node

        input = cm_node.execute()
        if isinstance(input, dict):
            if "collection" in input.keys() and "vector_loc" in input.keys():
                collection = input["collection"]
                vector_loc = input["vector_loc"]
            else:
                self.report({"ERROR"}, "No Collection/Vector Input")
                return {"FINISHED"}
        else:
            self.report({"ERROR"}, "Invalid Input")
            return {"FINISHED"}

        note_name = f"{cm_node.note_list}{cm_node.octave}"
        duration = input["note_dur"] * int(cm.note_den)
        size = duration / 10
        name = f"note-{duration}"
        mesh = bpy.data.meshes.new("note")
        obj = bpy.data.objects.new(name, mesh)
        objs = collection.objects
        if len(objs) > 0:
            if len(objs[0].material_slots) > 0:
                mat = objs[0].material_slots[0].material
                obj.data.materials.append(mat)
        collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj
        obj.location = vector_loc

        verts = [( 0.0, 0.0,  0.0),
                 ( size, 0.0,  0.0),
                 ( size, 0.1,  0.0),
                 ( 0.0, 0.1,  0.0),
                 ]
        edges = []
        faces = [[0, 1, 2, 3]]

        mesh.from_pydata(verts, [], faces)
        for o in context.view_layer.objects.selected:
            o.select_set(state = False)
        self.report({"INFO"}, "Note Placed")
        return {"FINISHED"}
