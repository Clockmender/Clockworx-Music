# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****
#
# -----------------------------------------------------------------------
# Author: Alan Odom (Clockmender) Copyright (c) 2019
# -----------------------------------------------------------------------
#
import bpy
import pygame.midi as pgm
from bpy.props import (
    IntProperty,
    FloatProperty,
    StringProperty,
    BoolProperty,
    EnumProperty,
    FloatVectorProperty,
    )
from .cm_functions import (
    connected_node_midi,
    start_clock,
    run_midi_always,
    start_midi,
    off_set,
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
        self.outputs.new("cm_socket.sound", "Midi Data")

    def draw_buttons(self, context, layout):
        cm_pg = context.scene.cm_pg
        layout.prop(self, "is_pygame_init")
        layout.prop(self, "num_packets")

    def get_midi(self):
        buffer1 = []
        buffer2 = []
        cm = bpy.context.scene.cm_pg

        if self.is_pygame_init:
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


class CM_ND_MidiHandlerNode(bpy.types.Node):
    bl_idname = "cm_audio_midi_midi_handler"
    bl_label = "MIDI Multi-Event Handler"
    bl_width_default = 150

    velocity : IntProperty(name="Velocity", default=100, min=-1, max=127,
        description="Velocity for Keys (-1 for Keyboard)")

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Midi Data")
        self.outputs.new("cm_socket.sound", "[Key, Control] Data")

    def draw_buttons(self, context, layout):
        layout.prop(self, "velocity")

    def get_midi(self):
        cm = bpy.context.scene.cm_pg
        buffer_in = connected_node_midi(self, 0)
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


class CM_ND_MidiAccumNode(bpy.types.Node):
    bl_idname = "cm_audio_midi_accum"
    bl_label = "MIDI Multi-Event Accumulator"
    bl_width_default = 150

    factor : FloatProperty(name="Factor", default=1.0,
        description="Multiplication Factor")
    con_plus : IntProperty(name="Plus", default=59, min=-1, max=127)
    con_minus : IntProperty(name="Minus", default=58, min=-1, max=127)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Midi Data")
        self.outputs.new("cm_socket.sound", "[Accumulated Floats]")

    def draw_buttons(self, context, layout):
        layout.prop(self, "factor")
        layout.prop(self, "con_plus")
        layout.prop(self, "con_minus")
        layout.operator("cm_audio.reset_accu", text="Reset to 0", icon="CANCEL")

    def get_midi(self):
        cm = bpy.context.scene.cm_pg
        buffer_in = connected_node_midi(self, 0)
        for b in buffer_in:
            #if there is data
            if len(b) > 0 and len(b[0]) > 0:
                if b[0][0] == 144:
                    if [b[0][1]] == self.con_plus:
                        cm.midi_data["notes_cu"] = round((cm.midi_data["notes_cu"] +
                            (b[0][2] / 127 * self.factor / 2)),5)
                    elif [b[0][1]] == self.con_minus:
                        cm.midi_data["notes_cu"] = round((cm.midi_data["notes_cu"] -
                            (b[0][2] / 127 * self.factor / 2)),5)
                elif b[0][0] == 176:
                    if b[0][1] == self.con_plus:
                        cm.midi_data["params_cu"] = round((cm.midi_data["params_cu"] +
                            (b[0][2] / 127 * self.factor / 2)),5)
                    elif b[0][1] == self.con_minus:
                        cm.midi_data["params_cu"] = round((cm.midi_data["params_cu"] -
                            (b[0][2] / 127 * self.factor) / 2),5)

        if cm.midi_debug:
            print(str(cm.midi_data["notes_cu"]))
            print(str(cm.midi_data["params_cu"]))
        return [cm.midi_data["notes_cu"], cm.midi_data["params_cu"]]


class CM_ND_MidiAnimNode(bpy.types.Node):
    bl_idname = "cm_audio_midi_anim_node"
    bl_label = "MIDI Object Animate"
    bl_width_default = 150
    """Multi-Animate One Object from MIDI Key, or Controls Data"""

    message : StringProperty(name="")
    object_name : StringProperty(name="Object", default="")
    anim_type: EnumProperty(
        items=(
            ("loc", "Location", "Animate Location"),
            ("rot", "Rotation", "Animate Rotation"),
            ("scl", "Scale", "Animate Scale"),
        ),
        name="Animate",
        default="loc",
        description="Animation Type",
    )
    midi_type: EnumProperty(
        items=(
            ("key", "Keys", "Use MIDI Keys"),
            ("con", "Controls", "Use MIDI Controls"),
        ),
        name="MIDI",
        default="key",
        description="MIDI Type",
    )
    factors : FloatVectorProperty(name="", subtype="XYZ", default=(1,1,1))
    con_px : IntProperty(name="X", default=32, min=-1, max=127)
    con_py : IntProperty(name="Y", default=48, min=-1, max=127)
    con_pz : IntProperty(name="Z", default=64, min=-1, max=127)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "[Key, Control] Data")
        self.outputs.new("cm_socket.sound", "[Key, Control] Data")

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, "object_name")
        row.operator("cm_audio.get_target", text="", icon="STYLUS_PRESSURE")
        box = layout.box()
        box.prop(self, "anim_type")
        box.prop(self, "midi_type")
        row = box.row()
        row.prop(self, "factors")
        box.label(text="Controls")
        row = box.row()
        row.prop(self, "con_px")
        row.prop(self, "con_py")
        row.prop(self, "con_pz")

    def get_midi(self):
        cm = bpy.context.scene.cm_pg
        buffer_in = connected_node_midi(self, 0)

        if self.object_name != "" and buffer_in is not None:
            tgt_obj = bpy.data.objects[self.object_name]
            if tgt_obj is not None:
                values = []
                if self.midi_type == "con":
                    num = 1
                else:
                    num = 0
                if self.con_px >= 0:
                    values.append(buffer_in[num][self.con_px] / 127)
                else:
                    values.append(0)
                if self.con_py >= 0:
                    values.append(buffer_in[num][self.con_py] / 127)
                else:
                    values.append(0)
                if self.con_pz >= 0:
                    values.append(buffer_in[num][self.con_pz] / 127)
                else:
                    values.append(0)

                vector_delta, euler_delta, scale_delta = off_set(values, self.factors)
                if self.anim_type == "loc":
                    tgt_obj.delta_location = vector_delta
                elif self.anim_type == "rot":
                    tgt_obj.delta_rotation_euler = euler_delta
                else:
                    tgt_obj.delta_scale = scale_delta

        return [cm.midi_data["notes"], cm.midi_data["params"]]


class CM_ND_FloatAnimNode(bpy.types.Node):
    bl_idname = "cm_audio_float_anim_node"
    bl_label = "Float Object Animate"
    bl_width_default = 150
    """Animate One Object from FLoat Data"""

    object_name : StringProperty(name="Object", default="")
    factors : FloatVectorProperty(name="", subtype="XYZ", default=(1,1,1))
    anim_type: EnumProperty(
        items=(
            ("loc", "Location", "Animate Location"),
            ("rot", "Rotation", "Animate Rotation"),
            ("scl", "Scale", "Animate Scale"),
        ),
        name="Animate",
        default="loc",
        description="Animation Type",
    )
    midi_type: EnumProperty(
        items=(
            ("key", "Keys", "Use MIDI Keys"),
            ("con", "Controls", "Use MIDI Controls"),
        ),
        name="MIDI",
        default="key",
        description="MIDI Type",
    )

    def init(self, context):
        self.inputs.new("cm_socket.sound", "[Key, Control] Data")
        self.outputs.new("cm_socket.sound", "[Key, Control] Data")

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, "object_name")
        row.operator("cm_audio.get_target", text="", icon="STYLUS_PRESSURE")
        box = layout.box()
        box.prop(self, "anim_type")
        box.prop(self, "midi_type")
        box.prop(self, "factors")

    def get_midi(self):
        cm = bpy.context.scene.cm_pg
        buffer_in = connected_node_midi(self, 0)

        if self.object_name != "" and buffer_in is not None:
            tgt_obj = bpy.data.objects[self.object_name]
            if tgt_obj is not None:
                values = []
                if self.midi_type == "con":
                    num = 1
                else:
                    num = 0
                values = []
                values.append(buffer_in[num] * self.factors.x)
                values.append(buffer_in[num] * self.factors.y)
                values.append(buffer_in[num] * self.factors.z)
                vector_delta, euler_delta, scale_delta = off_set(values, self.factors)
                if self.anim_type == "loc":
                    tgt_obj.delta_location = vector_delta
                elif self.anim_type == "rot":
                    tgt_obj.delta_rotation_euler = euler_delta
                else:
                    tgt_obj.delta_scale = scale_delta

        return [cm.midi_data["notes_cu"], cm.midi_data["params_cu"]]


class CM_ND_MidiNoteNode(bpy.types.Node):
    bl_idname = "cm_audio.midi_note_node"
    bl_label = "Midi Key Info"
    bl_icon = "SPEAKER"

    midi_type : IntProperty(name="Type", default=0)
    midi_id : IntProperty(name="ID", default=0)
    midi_value : FloatProperty(name="Value", default=0.0)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Midi Data")
        self.outputs.new("cm_socket.sound", "Key Data")

    def draw_buttons(self, context, layout):
        layout.prop(self, "midi_type")
        layout.prop(self, "midi_id")
        layout.prop(self, "midi_value")
        layout.context_pointer_set("audionode", self)
        layout.operator("cm_audio.display_midi", text="Update Display")

    def get_midi(self):
        cm = bpy.context.scene.cm_pg
        buffer_in = connected_node_midi(self, 0)
        buffer1 = buffer_in[0]
        if len(buffer_in[0]) > 0:
            self.midi_type = buffer1[0][0]
            self.midi_id = buffer1[0][1]
            self.midi_value = buffer1[0][2] / 127
            output = ([cm.midi_buffer["buffer1"][0][0],
                cm.midi_buffer["buffer1"][0][1],
                cm.midi_buffer["buffer1"][0][2] / 127
                ])
        else:
            output = [0,0,0]
        return output
