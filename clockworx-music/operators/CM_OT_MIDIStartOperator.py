import bpy
from ..cm_functions import run_midi_always

class CM_OT_MIDIStartOperator(bpy.types.Operator):
    bl_idname = "cm_audio.midi_start"
    bl_label = "CM Execute Start"

    @classmethod
    def poll(cls, context):
        return not bpy.app.timers.is_registered(run_midi_always)

    def execute(self, context):
        bpy.app.timers.register(run_midi_always)
        return {"FINISHED"}
