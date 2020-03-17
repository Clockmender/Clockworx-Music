import bpy

class CM_OT_GetTarget(bpy.types.Operator):
    """Set from Active Obect"""

    bl_idname = "cm_audio.get_target"
    bl_label = ""

    def execute(self, context):
        cm_node = context.node
        obj = context.view_layer.objects.active
        if obj is not None:
            cm_node.object_name = obj.name
        return {"FINISHED"}
