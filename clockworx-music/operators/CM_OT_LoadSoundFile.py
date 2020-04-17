import bpy

class CM_OT_LoadSoundFile(bpy.types.Operator):
    bl_idname = "cm_audio.load_sound"
    bl_label = "Load Sound File to VSE"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        cm_node = context.node
        return cm_node.sound_file_name != "" and cm_node.sound_file_name != "//"

    def execute(self, context):
        cm_node = context.node
        cm = context.scene.cm_pg
        path = bpy.path.abspath(cm_node.sound_file_name)
        scene = context.scene
        if not scene.sequence_editor:
            scene.sequence_editor_create()
        soundstrip = scene.sequence_editor.sequences.new_sound(
            "Sound", path, cm_node.sequence_channel, cm.offset
        )
        soundstrip.show_waveform = True
        return {"FINISHED"}
