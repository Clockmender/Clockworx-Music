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
bl_info = {
    "name": "Clockworx Music",
    "author": "Alan Odom (Clockmender)",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "Clockworx Node Tree > UI > PDT",
    "warning": "Don't do it, just don't even THINK of doing it!",
    "category": "Node",
}

# ----------------------------------------------
# Import modules
# ----------------------------------------------
if "bpy" in locals():
    import importlib

    importlib.reload(cm_functions)
else:
    from . import cm_functions


import aud
import bpy
import addon_utils
import importlib
import nodeitems_utils
from nodeitems_utils import NodeItem, NodeCategory
from bpy.types import PropertyGroup, Scene
from bpy.props import (
    IntProperty,
    FloatProperty,
    PointerProperty,
    StringProperty,
    BoolProperty,
    EnumProperty,
)


class AudioNodeTree(bpy.types.NodeTree):
    bl_description = "CM Audio Node Trees"
    bl_icon = "SOUND"
    bl_idname = "cm_AudioNodeTree"
    bl_label = "Clockworx Music Editor"
    bl_options = {"REGISTER", "UNDO"}

    def get_tree(self):
        return self.id_data

    def update(self):
        for socket in self.inputs:
            socket.update_value(None)
        for socket in self.outputs:
            socket.update_value(None)


class CMSceneProperties(PropertyGroup):
    """Contains all CM related properties."""

    bpm : IntProperty(name="BPM", default=60)
    time_sig_num : IntProperty(name="Time Sig N", default=4)
    time_sig_den : IntProperty(name="Time Sig D", default=4)
    #note_den : IntProperty(name="Note Denom.",min=1, default=16, max=64)
    note_den : EnumProperty(
        items=(
            ("1", "1", "1 Beat"),
            ("2", "2", "1/2 Beat"),
            ("4", "4", "1/4 Beat"),
            ("8", "8", "1/8 Beat"),
            ("16", "16", "1/16 Beat"),
            ("32", "32", "1/32 Beat"),
            ("64", "64", "1/64 Beat"),
        ),
        name="Note Denom",
        default="16",
        description="Note Denominator",
    )
    time_note_min : FloatProperty(name="Time_Note_Min", default=0)
    duration_factor : FloatProperty(name="Duration_Factor", default=0)
    sound_channels : IntProperty(name="Channels", default=2, min=1, max=9)
    samples : IntProperty(name="Samples", default=44100, min=6000)
    easing : FloatProperty(name="Note Easing", default=1.0, min=0.1, precision=1)
    spacing : FloatProperty(name="Note Spacing", default=0, min=0, precision=1)
    suffix : StringProperty(name = "Note Suffix")
    offset : IntProperty(name = "Offset - Anim Start Frame", default=1, min=-1000, max=10000)
    mid_c : BoolProperty(name = "Middle C = C4", default = True)
    channels : StringProperty()
    message : StringProperty(name="")
    message1 : StringProperty(name="")
    col_name : StringProperty(name="Collection", default="")
    suffix_obj : StringProperty(name="Suffix", default="key")
    bridge_len : FloatProperty(name = "Bridge Length", min=0.5,max=1.0)
    scale_f : FloatProperty(name = "Scale Factor", min=0.5, max=1)

    data_dict = {}
    event_dict = {}
    time_dict = {}
    # For MIDI Live
    midi_buffer = {}
    midi_buffer["buffer1"] = []
    midi_buffer["buffer2"] = []

    midi_data = {}
    note_buff = []
    param_buff = []
    note_buff_cu = []
    param_buff_cu = []
    for i in range(128):
        note_buff.append(0)
        param_buff.append(0)
        note_buff_cu.append(0)
        param_buff_cu.append(0)
    midi_data["notes"] = note_buff
    midi_data["params"] = param_buff
    midi_data["notes_cu"] = note_buff_cu
    midi_data["params_cu"] = param_buff_cu

    midi_poll_time : FloatProperty(name="Time", default=0.1, min=0.02, max=1)
    midi_debug : BoolProperty(name="Debug", default=False,
        description="Output MIDI Buffer to Console")


class AudioSetupNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "AudioNodeTree"


class AudioPropertiesNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "cm_AudioNodeTree"


class AudioIONodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "cm_AudioNodeTree"


class AudioFilterNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "cm_AudioNodeTree"


class AudioSequenceNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "cm_AudioNodeTree"

class AudioObjectNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "cm_AudioNodeTree"


categories = [
        AudioIONodeCategory("AUDIO_SETUP_CATEGORY", "Setup", items = [
        #NodeItem("cm_audio.control_node"),
        NodeItem("cm_audio.analyse_midi_node"),
        NodeItem("cm_audio.midi_bake_node"),
        NodeItem("cm_audio_midi_init_node"),
        NodeItem("cm_audio_midi_midi_handler"),
        NodeItem("cm_audio_midi_accum"),
    ]),
        AudioIONodeCategory("AUDIO_PROP_CATEGORY", "Constants/Info", items = [
        NodeItem("cm_audio.text_node"),
        NodeItem("cm_audio.float_node"),
        NodeItem("cm_audio.int_node"),
        NodeItem("cm_audio.bool_node"),
        NodeItem("cm_audio.debug_node"),
        NodeItem("cm_audio.info_node"),
        NodeItem("cm_audio.sound_info_node"),
        NodeItem("cm_audio.midi_note_node"),
        NodeItem("cm_audio.frame_node"),
        NodeItem("cm_audio.time_node"),
        NodeItem("cm_audio.beats_node"),
    ]),
    AudioIONodeCategory("AUDIO_IO_CATEGORY", "Input/Output", items = [
        NodeItem("cm_audio.note_node"),
        NodeItem("cm_audio.sound_node"),
        NodeItem("cm_audio.chord_node"),
        NodeItem("cm_audio.arpeggio_node"),
        NodeItem("cm_audio.file_node"),
        NodeItem("cm_audio.fm_synth"),
        NodeItem("cm_audio.output_node"),
        NodeItem("cm_audio.write_node"),
        NodeItem("cm_audio.player_node"),
    ]),
    AudioFilterNodeCategory("AUDIO_FILTER_CATEGORY", "Filter", items = [
    # Commented out don't work with Blender < 2.8
        NodeItem("cm_audio.accumulator_node"),
        NodeItem("cm_audio.compressor_node"),
        NodeItem("cm_audio.delay_node"),
        NodeItem("cm_audio.doppler_node"),
        NodeItem("cm_audio.echo_node"),
        NodeItem("cm_audio.envelope_node"),
        NodeItem("cm_audio.fader_node"),
        NodeItem("cm_audio.highpass_node"),
        NodeItem("cm_audio.limit_node"),
        NodeItem("cm_audio.lowpass_node"),
        NodeItem("cm_audio.modulate_node"),
        NodeItem("cm_audio.phaser_node"),
        NodeItem("cm_audio.pitch_node"),
        NodeItem("cm_audio.resample_node"),
        NodeItem("cm_audio.reverb_node"),
        NodeItem("cm_audio.reverse_node"),
        NodeItem("cm_audio.volume_node"),
    ]),
    AudioSequenceNodeCategory("AUDIO_SEQUENCE_CATEGORY", "Sequence", items = [
        NodeItem("cm_audio.join_node"),
        NodeItem("cm_audio.sequence_node"),
        NodeItem("cm_audio.loop_node"),
        NodeItem("cm_audio.mix_node"),
        NodeItem("cm_audio.mix_eight_node"),
        NodeItem("cm_audio.pingpong_node"),
        NodeItem("cm_audio.slicer_node"),
    ]),
        AudioSequenceNodeCategory("AUDIO_OBJECT_CATEGORY", "Objects", items = [
        NodeItem("cm_audio.object_loc_node"),
        NodeItem("cm_audio.object_sound_node"),
        NodeItem("cm_audio.piano_roll_node"),
        NodeItem("cm_audio_midi_anim_node"),
        NodeItem("cm_audio_float_anim_node"),
    ]),
]

def print_log(parent=None, child=None, func=None, msg=""):
    log = "Clockworx_music: "
    if (parent):
        log += parent + ": "
    if (child):
        log += child + ": "
    if (func):
        log += func + "(): "
    log += msg
    print(log)

def import_sockets(path="./"):
    out = []
    for i in bpy.path.module_names(path + "sockets"):
        out.append(getattr(importlib.import_module(".sockets." + i[0], __name__), i[0]))
        print_log("IMPORT SOCKET", msg=i[0])
    return out

def import_menus(path="./"):
    out = []
    for i in bpy.path.module_names(path + "menus"):
        out.append(getattr(importlib.import_module(".menus." + i[0], __name__), i[0]))
        print_log("IMPORT MENU", msg=i[0])
    return out

def import_operators(path="./"):
    out = []
    for i in bpy.path.module_names(path + "operators"):
        out.append(getattr(importlib.import_module(".operators." + i[0], __name__), i[0]))
        print_log("IMPORT OPERATOR", msg=i[0])
    return out

def import_nodes(path="./"):
    out = []
    for i in bpy.path.module_names(path + "nodes"):
        out.append(getattr(importlib.import_module(".nodes." + i[0], __name__), i[0]))
        print_log("IMPORT NODE", msg=i[0])
    return out

classes = [
    CMSceneProperties,
    AudioNodeTree,
    ]

path = repr([i for i in addon_utils.modules() if i.bl_info['name'] == "Clockworx Music"][0]).split("from '")[1].split("__init__.py'>")[0]
sockets = import_sockets(path)
classes.extend(sockets)
menus = import_menus(path)
classes.extend(menus)
operators = import_operators(path)
classes.extend(operators)
nodes = import_nodes(path)
classes.extend(nodes)


def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    Scene.cm_pg = PointerProperty(type=CMSceneProperties)

    nodeitems_utils.register_node_categories("AUDIO_CATEGORIES", categories)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    nodeitems_utils.unregister_node_categories("AUDIO_CATEGORIES")

    del Scene.cm_pg

if __name__ == "__main__":
  register()
