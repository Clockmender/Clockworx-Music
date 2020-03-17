import bpy

class CM_OT_GetName(bpy.types.Operator):
    """Set from Active Obect"""

    bl_idname = "cm_audio.get_name"
    bl_label = ""

    def execute(self, context):
        cm_node = context.node
        obj = context.view_layer.objects.active
        if obj is not None:
            cm_node.control_name = obj.name
        return {"FINISHED"}
