import bpy

class CM_OT_SetConstantsMenu(bpy.types.Operator):
    bl_idname = "cm_audio.set_constants_menu"
    bl_label = "Setup Blend File Parameters"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        cm = context.scene.cm_pg
        note_den = int(cm.note_den)
        fps = int((cm.bpm / 60 * note_den) * 100)
        bpy.context.scene.render.fps = fps
        bpy.context.scene.render.fps_base = 100
        cm.time_note_min = round((60 / cm.bpm) / note_den, 4)
        cm.duration_factor = round(note_den * cm.bpm / 600, 4)
        cm.bar_len = ((cm.time_sig_num / cm.time_sig_den) * int(cm.note_den) * 0.1)
        cm.message = "Parameters Set."
        return {"FINISHED"}
