import bpy
from mathutils import Vector

class CM_OT_NoteCopyPosition(bpy.types.Operator):
    bl_idname = "cm_audio.note_copy_position"
    bl_label = "Copy Note(s)"
    bl_description = "Copy Selected Note(s)"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        cm = bpy.context.scene.cm_pg
        cm_node = context.node
        input = cm_node.execute()
        if isinstance(input, dict):
            if "vector_loc" in input.keys():
                collection = input["collection"]
            else:
                self.report({"ERROR"}, "No Vector Input")
                return {"FINISHED"}
        else:
            self.report({"ERROR"}, "Invalid Input")
            return {"FINISHED"}

        objs = context.view_layer.objects.selected
        if len(objs) > 0:
            objs = context.view_layer.objects.selected
            bpy.ops.object.duplicate_move()
            obj_ds = bpy.context.view_layer.objects.selected
            off_x = cm_node.bar_num * cm.bar_len
            off_y = cm_node.octave * 1.2
            for ob in obj_ds:
                ob.location = ob.location + Vector((off_x, off_y, 0))
                ob.select_set(state = False)
            self.report({"INFO"}, "Notes Copied")
            return {"FINISHED"}

        self.report({"ERROR"}, "No Objects Selected")
        return {"FINISHED"}
