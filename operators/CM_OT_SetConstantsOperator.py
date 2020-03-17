import bpy

class CM_OT_SetConstantsOperator(bpy.types.Operator):
    bl_idname = "cm_audio.set_constants"
    bl_label = "Set CM Constants"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        cm = context.scene.cm_pg
        cm_node = context.node
        cm.bpm = cm_node.bpm
        cm.time_sig_num = cm_node.time_sig_num
        cm.time_sig_den = cm_node.time_sig_den
        cm.samples = cm_node.samples
        if cm_node.note_den in [1, 2, 4, 8, 16, 32, 64]:
            fps = int((cm_node.bpm / 60 * cm_node.note_den) * 100)
            bpy.context.scene.render.fps = fps
            bpy.context.scene.render.fps_base = 100
            cm.note_den = cm_node.note_den
            cm.time_note_min = round((60 / cm_node.bpm) / cm_node.note_den, 4)
            cm.duration_factor = round(cm_node.note_den * cm_node.bpm / 600, 4)
            cm_node.message = ""
        else:
            cm_node.message = "Note Den must be 1,2,4,8,16,32 or 64"
        cm_node.message = "Parameters Set."
        return {"FINISHED"}
