import bpy
from ..cm_functions import run_midi_always

class CM_OT_MIDIStopOperator(bpy.types.Operator):
    bl_idname = "cm_audio.midi_stop"
    bl_label = "CM Execute Stop"

    @classmethod
    def poll(cls, context):
        return bpy.app.timers.is_registered(run_midi_always)

    def execute(self, context):
        if bpy.app.timers.is_registered(run_midi_always):
            bpy.app.timers.unregister(run_midi_always)
        return {"FINISHED"}
