import bpy
from ..cm_functions import analyse_midi_file

class CM_OT_AnalyseMidiFile(bpy.types.Operator):
    bl_idname = "cm_audio.analyse_midi"
    bl_label = "Analyse Midi File"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        cm_node = context.node
        return ".csv" in cm_node.midi_file_name

    def execute(self, context):
        cm_node = context.node
        cm = context.scene.cm_pg
        path = bpy.path.abspath(cm_node.midi_file_name)
        analyse_midi_file(context)
        cm_node.pulse = cm.data_dict["Pulse"]
        cm_node.bpm = cm.data_dict["BPM"]
        cm_node.tempo = int(cm.data_dict["Tempo"][0][1])
        cm_node.time_sig = f"{cm.data_dict['TimeSig'][0]}:{cm.data_dict['TimeSig'][1]}"
        cm_node.track_name = cm.data_dict['Track Name']
        first = True
        for v in range(len(cm.data_dict['Tracks'])):
            if first:
                cm_node.tracks = cm.data_dict['Tracks'][v][0]
                first = False
            else:
                cm_node.tracks = cm_node.tracks + ", " + cm.data_dict['Tracks'][v][0]
        return {"FINISHED"}
