import bpy
import pygame.midi as pgm
from bpy.props import (
    IntProperty,
    BoolProperty,
    )

class CM_ND_MidiInitNode(bpy.types.Node):
    bl_idname = "cm_audio_midi_init_node"
    bl_label = "MIDI RealTime Data"
    bl_width_default = 150
    """Access MIDI Data from One or Two Controllers"""

    is_pygame_init: BoolProperty(name = "MIDI Input", default=True)
    num_packets : IntProperty(name="Packets", default=1,min=1)

    pgm.init()
    num_packets = 1
    midi_input = None
    midi_input2 = None
    mid_1_valid = True
    mid_dev_num = pgm.get_count()
    if mid_dev_num == 1:
        midi_info1 = str(pgm.get_device_info(0))
        if midi_info1.split(',')[2].strip() == '1':
            midi_input = pgm.Input(0)
        else:
            # Reduce mid_dev_num by 1 - this will now be 0 and trapped in the execute function
            mid_dev_num = mid_dev_num - 1
    elif mid_dev_num == 2:
        midi_info1 = str(pgm.get_device_info(0))
        midi_info2 = str(pgm.get_device_info(1))
        if midi_info1.split(',')[2].strip() == '1':
            midi_input = pgm.Input(0)
        else:
            # Reduce mid_dev_num by 1 and set midi_input 1 to invalid
            mid_dev_num = mid_dev_num - 1
            mid_1_valid = False
        if midi_info2.split(',')[2].strip() == '1':
            if mid_1_valid: # Set second midi_input to this pygame input
                midi_input2 = pgm.Input(1)
            else: # Set first midi_input to this pygame input (only this is valid)
                midi_input = pgm.Input(1)
        else:
            # Reduce mid_dev_num by 1
            mid_dev_num = mid_dev_num - 1
    else:
        # We only handle up to 2 interfaces for now
        message = 'None or More than 2, MIDI Interface(s)'
        # By now we should have a number for valid Midi Inputs

    def init(self, context):
        self.outputs.new("cm_socket.midi", "Midi Data")

    def draw_buttons(self, context, layout):
        cm_pg = context.scene.cm_pg
        layout.prop(self, "is_pygame_init")
        layout.prop(self, "num_packets")

    def get_midi(self):
        buffer1 = []
        buffer2 = []
        cm = bpy.context.scene.cm_pg

        if self.is_pygame_init and self.midi_input is not None:
            # messages are formatted this way: [[message type, note / parameter ID, velocity
            # / parameter value, ?], TimeStamp]
            buffer1 = pgm.Input.read(self.midi_input, self.num_packets)
            if len(buffer1) > 0:
                cm.midi_buffer["buffer1"] = [b[0] for b in buffer1]
                if cm.midi_debug:
                    print('Dev 1: ' + str(pgm.get_device_info(0)))
                    print(str(cm.midi_buffer["buffer1"]))

            if self.midi_input2 is not None:
                buffer2 = pgm.Input.read(self.midi_input2, self.num_packets)
                if len(buffer2) > 0:
                    cm.midi_buffer["buffer2"] = [b[0] for b in buffer2]
                    if cm.midi_debug:
                        print('Dev 2: ' + str(pgm.get_device_info(1)))
                        print(str(cm.midi_buffer["buffer2"]))

            return [cm.midi_buffer["buffer1"], cm.midi_buffer["buffer2"]]
        else:
            return None

    def output(self):
        return self.get_midi()
