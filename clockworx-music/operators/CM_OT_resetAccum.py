import bpy

class CM_OT_resetAccum(bpy.types.Operator):
    bl_idname = "cm_audio.reset_accu"
    bl_label = "Reset Accumulator"
    bl_description = "Reset This Node's Accumulated Values to 0"

    def execute(self, context):
        cm = bpy.context.scene.cm_pg
        cm_node = context.node
        cm.midi_data["notes_cu"][cm_node.con_plus] = 0
        cm.midi_data["params_cu"][cm_node.con_plus] = 0
        return {"FINISHED"}
