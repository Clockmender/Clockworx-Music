import bpy

class CM_OT_GetSuffix(bpy.types.Operator):
    """Set from Active Obect"""

    bl_idname = "cm_audio.get_suffix"
    bl_label = ""

    def execute(self, context):
        cm_node = context.node
        obj = context.view_layer.objects.active
        if obj is not None:
            cm_node.suffix = obj.name.split("_")[1]
        return {"FINISHED"}
