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

    importlib.reload(cm_sockets)
    importlib.reload(cm_nodes)
    importlib.reload(cm_filter_nodes)
    importlib.reload(cm_operators)
    importlib.reload(cm_functions)
    importlib.reload(cm_midi_bake)
    importlib.reload(cm_objects)
    importlib.reload(cm_menus)
else:
    from . import cm_sockets
    from . import cm_nodes
    from . import cm_filter_nodes
    from . import cm_operators
    from . import cm_functions
    from . import cm_midi_bake
    from . import cm_objects
    from . import cm_menus


import aud
import bpy
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
    type_bool : BoolProperty(name="Time (True) or Beats", default=True)
    data_dict = {}
    event_dict = {}
    time_dict = {}
    message1 : StringProperty(name="")
    col_name : StringProperty(name="Collection", default="")
    suffix_obj : StringProperty(name="Suffix", default="key")
    bridge_len : FloatProperty(name = "Bridge Length", min=0.5,max=1.0)
    scale_f : FloatProperty(name = "Scale Factor", min=0.5, max=1)


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
        NodeItem("cm_audio.midi_bake_node"),
    ]),
        AudioIONodeCategory("AUDIO_PROP_CATEGORY", "Constants/Info", items = [
        NodeItem("cm_audio.text_node"),
        NodeItem("cm_audio.float_node"),
        NodeItem("cm_audio.int_node"),
        NodeItem("cm_audio.bool_node"),
        NodeItem("cm_audio.debug_node"),
        NodeItem("cm_audio.info_node"),
        NodeItem("cm_audio.sound_info_node"),
        NodeItem("cm_audio.frame_node"),
        NodeItem("cm_audio.time_node"),
        NodeItem("cm_audio.beats_node"),
    ]),
    AudioIONodeCategory("AUDIO_IO_CATEGORY", "Input/Output", items = [
        NodeItem("cm_audio.sound_node"),
        NodeItem("cm_audio.chord_node"),
        NodeItem("cm_audio.arpeggio_node"),
        NodeItem("cm_audio.file_node"),
        NodeItem("cm_audio.output_node"),
        NodeItem("cm_audio.write_node"),
    ]),
    AudioFilterNodeCategory("AUDIO_FILTER_CATEGORY", "Filter", items = [
    # Commented out don't work with Blender < 2.8
        NodeItem("cm_audio.accumulator_node"),
        NodeItem("cm_audio.delay_node"),
        NodeItem("cm_audio.echo_node"),
        NodeItem("cm_audio.envelope_node"),
        NodeItem("cm_audio.fader_node"),
        NodeItem("cm_audio.highpass_node"),
        NodeItem("cm_audio.limit_node"),
        NodeItem("cm_audio.lowpass_node"),
        NodeItem("cm_audio.modulate_node"),
        NodeItem("cm_audio.pitch_node"),
        NodeItem("cm_audio.resample_node"),
        NodeItem("cm_audio.reverse_node"),
        NodeItem("cm_audio.volume_node"),
    ]),
    AudioSequenceNodeCategory("AUDIO_SEQUENCE_CATEGORY", "Sequence", items = [
        NodeItem("cm_audio.join_node"),
        NodeItem("cm_audio.sequence_node"),
        NodeItem("cm_audio.loop_node"),
        NodeItem("cm_audio.mix_node"),
        NodeItem("cm_audio.pingpong_node"),
        NodeItem("cm_audio.slicer_node"),
    ]),
        AudioSequenceNodeCategory("AUDIO_OBJECT_CATEGORY", "Objects", items = [
        NodeItem("cm_audio.object_loc_node"),
        NodeItem("cm_audio.piano_roll_node"),
    ]),
]

classes = [
    CMSceneProperties,
    AudioNodeTree,
    cm_menus.CM_PT_PanelDesign,
    cm_menus.CM_PT_PanelView,
    cm_sockets.CM_SK_AudioNodeSocket,
    cm_sockets.CM_SK_FloatNodeSocket,
    cm_sockets.CM_SK_IntNodeSocket,
    cm_sockets.CM_SK_TextNodeSocket,
    cm_sockets.CM_SK_BoolNodeSocket,
    cm_sockets.CM_SK_GenericNodeSocket,
    cm_nodes.CM_ND_AudioTextNode,
    cm_nodes.CM_ND_AudioFloatNode,
    cm_nodes.CM_ND_AudioIntNode,
    cm_nodes.CM_ND_AudioBoolNode,
    cm_nodes.CM_ND_AudioFrameNode,
    cm_nodes.CM_ND_AudioTimeNode,
    cm_nodes.CM_ND_AudioBeatsNode,
    cm_nodes.CM_ND_AudioInfoNode,
    cm_nodes.CM_ND_SoundInfoNode,
    cm_nodes.CM_ND_AudioDebugNode,
    cm_nodes.CM_ND_AudioSoundNode,
    cm_nodes.CM_ND_AudioChordNode,
    cm_nodes.CM_ND_AudioFileNode,
    cm_nodes.CM_ND_AudioOutputNode,
    cm_nodes.CM_ND_AudioControlNode,
    cm_nodes.CM_ND_AudioWriteNode,
    cm_nodes.CM_ND_AudioArpeggioNode,
    cm_filter_nodes.CM_ND_AudioAccumulatorNode,
    cm_filter_nodes.CM_ND_AudioDelayNode,
    cm_filter_nodes.CM_ND_AudioEchoNode,
    cm_filter_nodes.CM_ND_AudioEnvelopeNode,
    cm_filter_nodes.CM_ND_AudioFaderNode,
    cm_filter_nodes.CM_ND_AudioHighpassNode,
    cm_filter_nodes.CM_ND_AudioLimitNode,
    cm_filter_nodes.CM_ND_AudioLoopNode,
    cm_filter_nodes.CM_ND_AudioLowpassNode,
    cm_filter_nodes.CM_ND_AudioPitchNode,
    cm_filter_nodes.CM_ND_AudioVolumeNode,
    cm_filter_nodes.CM_ND_AudioJoinNode,
    cm_filter_nodes.CM_ND_AudioSequenceNode,
    cm_filter_nodes.CM_ND_AudioMixNode,
    cm_filter_nodes.CM_ND_AudioModulateNode,
    cm_filter_nodes.CM_ND_AudioPingPongNode,
    cm_filter_nodes.CM_ND_AudioReverseNode,
    cm_filter_nodes.CM_ND_AudioResampleNode,
    cm_filter_nodes.CM_ND_AudioSlicerNode,
    cm_operators.CM_OT_PlayAudioNodeOperator,
    cm_operators.CM_OT_DisplayAudioNodeOperator,
    cm_operators.CM_OT_ExecuteStartOperator,
    cm_operators.CM_OT_ExecuteStopOperator,
    cm_operators.CM_OT_SetConstantsOperator,
    cm_operators.CM_OT_SetConstantsMenu,
    cm_operators.CM_OT_StopAudioNodeOperator,
    cm_operators.CM_OT_WriteAudioNodeOperator,
    cm_operators.CM_OT_impKeyb88,
    cm_operators.CM_OT_impKeyb61,
    cm_operators.CM_OT_impFrets,
    cm_operators.CM_OT_renMesh,
    cm_operators.CM_OT_UnlockView,
    cm_operators.CM_OT_lockView,
    cm_midi_bake.CM_ND_AudioMidiBakeNode,
    cm_midi_bake.CM_OT_LoadSoundFile,
    cm_midi_bake.CM_OT_CreateMIDIControls,
    cm_midi_bake.CM_OT_CreateMIDISound,
    cm_objects.CM_ND_ObjectLocNode,
    cm_objects.CM_ND_PianoRollNode,
    cm_objects.CM_OT_EvaluatePiano,
    cm_objects.CM_OT_EvaluateNotes,
    cm_objects.CM_OT_GetName,
    cm_objects.CM_OT_GetSuffix,
    cm_objects.CM_OT_GetTarget,
    ]


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
