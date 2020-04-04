import bpy
from bpy.props import (
    IntProperty,
    FloatProperty,
    StringProperty,
    BoolProperty,
    EnumProperty,
    FloatVectorProperty,
)
from ..cm_functions import connected_node_midi


class CM_ND_MidiAccumNode(bpy.types.Node):
    bl_idname = "cm_audio_midi_accum"
    bl_label = "MIDI Accumulator"
    bl_width_default = 150

    #factor: FloatProperty(name="Factor", default=1.0, description="Multiplication Factor")
    con_plus: IntProperty(name="Plus", default=59, min=-1, max=127)
    con_minus: IntProperty(name="Minus", default=58, min=-1, max=127)

    def init(self, context):
        self.inputs.new("cm_socket.midi", "Midi Data")
        self.outputs.new("cm_socket.midi", "[Accumulated Floats]")

    def draw_buttons(self, context, layout):
        #layout.prop(self, "factor")
        layout.prop(self, "con_plus")
        layout.prop(self, "con_minus")
        layout.operator("cm_audio.reset_accu", text="Reset to 0", icon="CANCEL")

    def get_midi(self):
        cm = bpy.context.scene.cm_pg
        buffer_in = connected_node_midi(self, 0)
        if buffer_in is not None:
            for b in buffer_in:
                if self.con_plus != self.con_minus:
                    # if there is data
                    if len(b) > 0 and len(b[0]) > 0:
                        if b[0][0] == 144:
                            if b[0][1] == self.con_plus:
                                cm.midi_data["notes_cu"][self.con_plus] = round(
                                    (cm.midi_data["notes_cu"][self.con_plus] +
                                    (b[0][2] / 127)), 5
                                )
                            elif b[0][1] == self.con_minus:
                                cm.midi_data["notes_cu"][self.con_plus] = round(
                                    (cm.midi_data["notes_cu"][self.con_plus]
                                     - (b[0][2] / 127)), 5
                                )
                        elif b[0][0] == 176:
                            if b[0][1] == self.con_plus:
                                cm.midi_data["params_cu"][self.con_plus] = round(
                                    (cm.midi_data["params_cu"][self.con_plus]
                                     + (b[0][2] / 127)), 5
                                )
                            elif b[0][1] == self.con_minus:
                                cm.midi_data["params_cu"][self.con_plus] = round(
                                    (cm.midi_data["params_cu"][self.con_plus]
                                     - (b[0][2] / 127)), 5
                                )
                else:
                    print("Two Controls are the same ID")

            if cm.midi_debug:
                print(str(cm.midi_data["notes_cu"]))
                print(str(cm.midi_data["params_cu"]))
            return [cm.midi_data["notes_cu"][self.con_plus], cm.midi_data["params_cu"][self.con_plus]]
        else:
            return None


        def output(self):
            output = self.get_midi()
            return {"MIDI Handler": output}
