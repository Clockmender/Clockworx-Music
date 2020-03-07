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
from math import pi
from mathutils import Vector, Euler
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
                if cm.midi_debug:
                    print('Dev 1: ' + str(pgm.get_device_info(0)))
                    print(str(buffer1[0]))
                cm.midi_buffer["buffer1"] = buffer1
            if self.midi_input2 is not None:
                buffer2 = pgm.Input.read(self.midi_input2, self.num_packets)
                if len(buffer2) > 0:
                    if cm.midi_debug:
                        print('Dev 2: ' + str(pgm.get_device_info(1)))
                        print(str(buffer2[0]))
                    cm.midi_buffer["buffer2"] = buffer2
        return [cm.midi_buffer["buffer1"], cm.midi_buffer["buffer2"]]


class CM_ND_MidiAnimNode(bpy.types.Node):
    bl_idname = "cm_audio_midi_anim_node"
    bl_label = "MIDI Animate (1)"
    bl_width_default = 150
    """ Animate One Object from MIDI Data"""

    message : StringProperty(name="")
    midi_type : IntProperty(name="Type", default=0)
    midi_id : IntProperty(name="ID", default=0)
    midi_value : FloatProperty(name="Value", default=0.0)
    object_name : StringProperty(name="Object", default="")
    anim_type: EnumProperty(
        items=(
            ("loc", "Location", "Animate Location"),
            ("rot", "Rotation", "Animate Rotation"),
            ("scl", "Scale", "Animate Scale"),
        ),
        name="Animate:",
        default="loc",
        description="Animation Type",
    )
    factor_x : FloatProperty(name="Factor X", default=1)
    factor_y : FloatProperty(name="Factor Y", default=1)
    factor_z : FloatProperty(name="Factor Z", default=1)
    factors : FloatVectorProperty(name="", subtype="XYZ", default=(1,1,1))
    con_px : IntProperty(name="X", default=32)
    con_py : IntProperty(name="Y", default=48)
    con_pz : IntProperty(name="Y", default=64)
    con_mx : IntProperty(name="-X", default=33)
    con_my : IntProperty(name="-Y", default=49)
    con_mz : IntProperty(name="-Y", default=65)
    lx_bool : BoolProperty(name="X", default=False)
    ly_bool : BoolProperty(name="Y", default=False)
    lz_bool : BoolProperty(name="Z", default=False)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Midi Data")
        self.outputs.new("cm_socket.sound", "Midi Data")

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, "object_name")
        row.operator("cm_audio.get_target", text="", icon="EYEDROPPER")
        box = layout.box()
        box.prop(self, "anim_type")
        row = box.row()
        row.prop(self, "factors")
        box.label(text="Controls")
        row = box.row()
        row.prop(self, "con_px")
        row.prop(self, "con_py")
        row.prop(self, "con_pz")
        row = box.row()
        row.prop(self, "con_mx")
        row.prop(self, "con_my")
        row.prop(self, "con_mz")
        row = box.row()
        row.label(text="Anime Axes for Keys")
        row = box.row()
        row.prop(self, "lx_bool")
        row.prop(self, "ly_bool")
        row.prop(self, "lz_bool")

    def get_midi(self):
        cm = bpy.context.scene.cm_pg
        buffer_in = connected_node_midi(self, 0)

        def off_set():
            a_offset = self.midi_value
            x_loc = 0
            y_loc = 0
            z_loc = 0
            if self.midi_type == 176:
                # This is just test stuff
                if self.midi_id == self.con_px:
                    x_loc = a_offset * self.factors.x
                elif self.midi_id == self.con_py:
                    y_loc = a_offset * self.factors.y
                elif self.midi_id == self.con_pz:
                    z_loc = a_offset * self.factors.z
                elif self.midi_id == self.con_mx:
                    x_loc = a_offset * -self.factors.x
                elif self.midi_id == self.con_my:
                    y_loc = a_offset * -self.factors.y
                elif self.midi_id == self.con_mz:
                    z_loc = a_offset * -self.factors.z
            elif self.midi_type == 144:
                if self.lx_bool:
                    x_loc = a_offset * self.factors.x
                if self.ly_bool:
                    y_loc = a_offset * self.factors.y
                if self.lz_bool:
                    z_loc = a_offset * self.factors.z

            return (
                Vector((x_loc, y_loc, z_loc)),
                Euler(((x_loc * pi / 180), (y_loc * pi / 180), (z_loc * pi / 180))),
                Vector(((1 + x_loc), (1 + y_loc), (1 + z_loc)))
                )

        if len(buffer_in[0]) > 0:
            buffer1 = buffer_in[0]
            self.midi_type = buffer1[0][0][0]
            self.midi_id = buffer1[0][0][1]
            self.midi_value = buffer1[0][0][2] / 127
            if self.object_name != "":
                tgt_obj = bpy.data.objects[self.object_name]
                if tgt_obj is not None:
                    vector_delta, euler_delta, scale_delta = off_set()
                    tgt_obj = bpy.data.objects[self.object_name]
                    if tgt_obj is not None:
                        if self.anim_type == "loc":
                            tgt_obj.delta_location = vector_delta
                        elif self.anim_type == "rot":
                            tgt_obj.delta_rotation_euler = euler_delta
                        else:
                            tgt_obj.delta_scale = scale_delta

        return [cm.midi_buffer["buffer1"], cm.midi_buffer["buffer2"]]


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
            self.midi_type = buffer1[0][0][0]
            self.midi_id = buffer1[0][0][1]
            self.midi_value = buffer1[0][0][2] / 127
            output = ([cm.midi_buffer["buffer1"][0][0][0],
                cm.midi_buffer["buffer1"][0][0][1],
                cm.midi_buffer["buffer1"][0][0][2] / 127
                ])
        else:
            output = [0,0,0]
        return output
