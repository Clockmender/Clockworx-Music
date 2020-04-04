import bpy
from bpy.props import (
    IntProperty,
    )
from ..cm_functions import connected_node_midi

class CM_ND_MidiHandlerNode(bpy.types.Node):
    bl_idname = "cm_audio_midi_midi_handler"
    bl_label = "MIDI Event Handler"
    bl_width_default = 150

    velocity : IntProperty(name="Velocity", default=100, min=-1, max=127,
        description="Velocity for Keys (-1 for Keyboard)")

    def init(self, context):
        self.inputs.new("cm_socket.midi", "Midi Data")
        self.outputs.new("cm_socket.midi", "[Key, Control] Data")

    def draw_buttons(self, context, layout):
        layout.prop(self, "velocity")

    def get_midi(self):
        cm = bpy.context.scene.cm_pg
        buffer_in = connected_node_midi(self, 0)
        if buffer_in is not None:
            for b in buffer_in:
                #if there is data
                if len(b) > 0 and len(b[0]) > 0:
                    if b[0][0] == 144:
                        if self.velocity == -1:
                            cm.midi_data["notes"][b[0][1]] = b[0][2]
                        elif b[0][2] == 0:
                            cm.midi_data["notes"][b[0][1]] = 0
                        else:
                            cm.midi_data["notes"][b[0][1]] = self.velocity
                    elif b[0][0] == 176:
                        cm.midi_data["params"][b[0][1]] = b[0][2]

            if cm.midi_debug:
                print(str(cm.midi_data["notes"]))
                print(str(cm.midi_data["params"]))
            return [cm.midi_data["notes"], cm.midi_data["params"]]
        else:
            return None

    def output(self):
        output = self.get_midi()
        return {"MIDI Handler": output}
