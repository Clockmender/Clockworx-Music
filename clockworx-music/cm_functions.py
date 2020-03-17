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
import aud
import bpy
import os
from mathutils import Quaternion, Vector, Euler
from math import pi


def connected_node(node, socket):
    """ Get Connected Node from Socket Num"""
    for link in node.id_data.links:
        if link.to_socket == node.inputs[socket]:
            return link.from_node
    return None

def connected_node_info(node, socket):
    """Get Return from info() Function"""
    node = connected_node(node, socket)
    if node == None:
        return None
    return node.info(bpy.context)

def connected_node_sound(node, socket):
    """Get Return from get_sound() Function"""
    node = connected_node(node, socket)
    if node == None:
        return None
    return node.get_sound()

def connected_node_midi(node, socket):
    """Get Return from get_midi() Function"""
    node = connected_node(node, socket)
    if node == None:
        return None
    return node.get_midi()

def view_lock():
    """Lock the View Rotation & Scale for DAW"""
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces[0].region_3d.view_rotation = Quaternion((1, 0, 0, 0))
            area.spaces[0].region_3d.lock_rotation = True
            view_distance = area.spaces[0].region_3d.view_distance
            if not (8 < view_distance < 12):
                area.spaces[0].region_3d.view_distance = 10


def get_socket_values(node, sockets, node_inputs):
    """Get Values from Input Sockets"""
    inputs = []
    for i in range(len(sockets)):
        socket = connected_node(node, i)
        if socket:
            if len(socket.values()) > 0:
                inputs.append(socket.values()[0])
            else:
                inputs.append(None)
        else:
            inputs.append(node_inputs[sockets[i]].value)
    return inputs


def start_clock(scene):
    """Run Execute Function in Nodes"""
    for nodetree in [
        n for n in bpy.data.node_groups if n.rna_type.name == "Clockworx Music Editor"
        ]:
        for n in nodetree.nodes:
            if (hasattr(n, "execute")):
                n.execute()

def start_piano(scene):
    for nodetree in [
        n for n in bpy.data.node_groups if n.rna_type.name == "Clockworx Music Editor"
        ]:
        for n in nodetree.nodes:
            if (hasattr(n, "evaluate")):
                n.evaluate()
                

def start_midi():
    """Run MIDI Function in Nodes"""
    for nodetree in [
        n for n in bpy.data.node_groups if n.rna_type.name == "Clockworx Music Editor"
        ]:
        for n in nodetree.nodes:
            if (hasattr(n, "get_midi")):
                n.get_midi()


def run_midi_always():
    """Run MIDI Function at Time Inteval"""
    cm = bpy.context.scene.cm_pg
    cm_pg = bpy.context.scene.cm_pg
    start_midi()
    return cm.midi_poll_time

def off_set(values, factors):
    x_loc = values[0] * factors.x
    y_loc = values[1] * factors.y
    z_loc = values[2] * factors.z

    return (
        Vector((x_loc, y_loc, z_loc)),
        Euler(((x_loc * pi / 180), (y_loc * pi / 180), (z_loc * pi / 180))),
        Vector(((1 + x_loc), (1 + y_loc), (1 + z_loc)))
        )

def analyse_midi_file(context):
    """Analyse MIDI File"""
    cm_node = context.node
    cm = context.scene.cm_pg
    cm_node.message1 = "Midi File Analysed: " + str(os.path.basename(cm_node.midi_file_name))
    cm_node.message2 = "Check/Load Sound File, Use Velocity, Easing & Offset"
    fps = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base
    cm.data_dict.clear()
    path = bpy.path.abspath(cm_node.midi_file_name)
    if ".csv" not in path:
        cm_node.message1 = "No CSV File specified"
        return
    with open(path) as f1:
        for line in f1:
            in_l = [elt.strip() for elt in line.split(",")]
            if in_l[2] == "Header":
                # Get Pulse variable.
                pulse = int(in_l[5])
                cm.data_dict["Pulse"] = pulse
            elif in_l[2] == "Tempo":
                if in_l[1] == "0":
                    # Get Initial Tempo.
                    tempo = in_l[3]
                    bpm = float(round((60000000 / int(tempo)), 3))
                    cm.data_dict["BPM"] = bpm
                    cm.data_dict["Tempo"] = [[0, tempo]]
                elif in_l[0] == "1" and in_l[2] == "Tempo":
                    # Add Tempo Changes & timings to Tempo Key in dataD.
                    frame = round(int(in_l[1]) * (60 * fps) / (bpm * pulse), 2)
                    cm.data_dict.get("Tempo").append([str(frame), in_l[3]])
            elif in_l[2] == "Time_signature":
                # Get Time Signature
                cm.data_dict["TimeSig"] = [int(in_l[3]), int(in_l[4])]
            elif (
                (in_l[2] == "Title_t") and (int(in_l[0]) > 1) and (in_l[3] != "Master Section")
            ):
                # Get Track Names & Numbers
                if in_l[0] == str(cm_node.midi_channel):
                    tName = in_l[3].strip('"')
                    cm.data_dict["Track Name"] = tName
                otName = in_l[3].strip('"')
                if "Tracks" not in cm.data_dict.keys():
                    cm.data_dict["Tracks"] = [[otName, int(in_l[0])]]
                    cm.channels = in_l[0]# + " - " + otName
                else:
                    cm.data_dict.get("Tracks").append([otName, int(in_l[0])])
                    cm.channels = cm.channels + "," + in_l[0]# + "&" + in_l[0] + " - " + otName

    cm_node.message2 = "Midi CSV File Analysed and Data Dictionary Built"
    return


note_list = [
    'c0','cs0','d0','ds0','e0','f0','fs0','g0','gs0','a0','as0','b0',
    'c1','cs1','d1','ds1','e1','f1','fs1','g1','gs1','a1','as1','b1',
    'c2','cs2','d2','ds2','e2','f2','fs2','g2','gs2','a2','as2','b2',
    'c3','cs3','d3','ds3','e3','f3','fs3','g3','gs3','a3','as3','b3',
    'c4','cs4','d4','ds4','e4','f4','fs4','g4','gs4','a4','as4','b4',
    'c5','cs5','d5','ds5','e5','f5','fs5','g5','gs5','a5','as5','b5',
    'c6','cs6','d6','ds6','e6','f6','fs6','g6','gs6','a6','as6','b6',
    'c7','cs7','d7','ds7','e7','f7','fs7','g7','gs7','a7','as7','b7',
    'c8','cs8','d8','ds8','e8','f8','fs8','g8','gs8','a8','as8','b8',
    'c9','cs9','d9','ds9','e9','f9','fs9','g9','gs9','a9','as9','b9',
    'c10','cs10','d10','ds10','e10','f10','fs10','g10','gs10','a10','as10','b10',
    ]

note_freq = [
    16.35160,17.32393,18.35405,19.44544,20.60172,21.82676,23.12465,24.49971,25.95654,27.5,29.13524,30.86771,
    32.70320,34.64783,36.70810,38.89087,41.20344,43.65353,46.24930,48.99943,51.91309,55.0,58.27047,61.73541,
    65.40639,69.29566,73.41619,77.78175,82.40689,87.30706,92.49861,97.99886,103.8262,110.0,116.5409,123.4708,
    130.8128,138.5913,146.8324,155.5635,164.8138,176.6141,184.9972,195.9977,207.6523,220.0,233.0819,246.9417,
    261.6526,277.1826,293.6648,311.1270,329.6276,349.2282,369.9944,391.9954,415.3047,440.0,466.1638,493.8833,
    523.2511,554.3653,587.3295,622.2540,659.2551,698.4565,739.9888,783.9909,830.6094,880.0,932.3275,987.7666,
    1046.502,1108.731,1174.659,1244.508,1318.510,1396.913,1479.978,1567.982,1661.219,1760.0,1864.655,1975.633,
    2093.005,2217.461,2349.016,2489.016,2637.020,2793.826,2959.955,3135.963,3322.438,3520.0,3729.310,3951.066,
    4186.009,4434.922,4698.636,4978.032,5274.041,5587.652,5919.911,6271.927,6644.875,7040.0,7458.620,7902.133,
    8372.018,8869.844,9397.272,9956.064,10548.08,11175.30,11839.82,12543.85,13289.75,14080.0,14917.24,15804.27,
    16744.04,17739.69,18794.54,19912.13,21096.16,22350.60,23679.64,25087.70,26579.50,28160.0,29834.48,31608.54]


def get_note(note_idx, offset):
    """Get Note Name from Index"""
    if (note_idx + offset) < len(note_list):
        return note_list[note_idx + offset]
    else:
        return "None"

def find_note(freq_index):
    """Find Note Index from Frequency"""
    idx = next((i for i, x in enumerate(note_freq) if x == freq_index), -1)
    note_name = noteList[idx] if idx > -1 else "Not a Note"
    return note_name

def get_index(note_name):
    """Get Not Index from Name"""
    index = next((i for i, x in enumerate(note_list) if x == note_name), -1)
    return index

def get_freq(index):
    """Get Frequency from Position in Frequencies"""
    if index < len(note_freq):
        return note_freq[index]
    else:
        return -1

def get_chord_ind(note_name, mode):
    """Build Chord Sequence from Note Name"""
    idx = next((i for i, x in enumerate(note_list) if x == note_name), -1)
    freq_list = []
    if len(note_name) >= 2 and note_name[1] == 's':
        if mode == 3:
            freq_list = [idx,idx+5,idx+8]
        elif mode == 4:
            freq_list = [idx,idx+5,idx+8,idx+11]
        elif mode == 5:
            freq_list = [idx,idx+5,idx+8,idx+11,idx+12]
    else:
        if mode == 3:
            freq_list = [idx,idx+4,idx+7]
        elif mode == 4:
            freq_list = [idx,idx+4,idx+7,idx+11]
        elif mode == 5:
            freq_list = [idx,idx+4,idx+7,idx+11,idx+12]
    return freq_list

def get_chord(note_name, mode):
    """Build Areggio Sequence from Note Name"""
    idx = next((i for i, x in enumerate(note_list) if x == note_name), -1)
    freq_list = []
    if len(note_name) >= 2 and note_name[1] == 's':
        if mode == 3:
            freq_list = [note_freq[idx],note_freq[idx+5],note_freq[idx+8]]
        elif mode == 4:
            freq_list = [note_freq[idx],note_freq[idx+5],note_freq[idx+8],note_freq[idx+11]]
        elif mode == -4:
            freq_list = [note_freq[idx-11],note_freq[idx-8],note_freq[idx-5],note_freq[idx],note_freq[idx+5],note_freq[idx+8],note_freq[idx+11]]
        elif mode == 5:
            freq_list = [note_freq[idx],note_freq[idx+5],note_freq[idx+8],note_freq[idx+11],note_freq[idx+12]]
        elif mode == 6:
            freq_list = [note_freq[idx],note_freq[idx+5],note_freq[idx+8],note_freq[idx+11],note_freq[idx+8],note_freq[idx+5]]
        elif mode == 7:
            freq_list = [note_freq[idx],note_freq[idx+5],note_freq[idx+8],note_freq[idx+11],note_freq[idx+8],note_freq[idx+5],note_freq[idx+1]]
        elif mode == 8:
            freq_list = [note_freq[idx],note_freq[idx+5],note_freq[idx+8],note_freq[idx+11],note_freq[idx+12],note_freq[idx+11],note_freq[idx+8],note_freq[idx+5]]
        elif mode == 9:
            freq_list = [note_freq[idx],note_freq[idx+5],note_freq[idx+8],note_freq[idx+11],note_freq[idx+12],note_freq[idx+11],note_freq[idx+8],note_freq[idx+5],note_freq[idx+1]]
    else:
        if mode == 3:
            freq_list = [note_freq[idx],note_freq[idx+4],note_freq[idx+7]]
        elif mode == 4:
            freq_list = [note_freq[idx],note_freq[idx+4],note_freq[idx+7],note_freq[idx+11]]
        elif mode == -4:
            freq_list = [note_freq[idx-11],note_freq[idx-7],note_freq[idx-4],note_freq[idx],note_freq[idx+4],note_freq[idx+7],note_freq[idx+11]]
        elif mode == 5:
            freq_list = [note_freq[idx],note_freq[idx+4],note_freq[idx+7],note_freq[idx+11],note_freq[idx+12]]
        elif mode == 6:
            freq_list = [note_freq[idx],note_freq[idx+4],note_freq[idx+7],note_freq[idx+11],note_freq[idx+7],note_freq[idx+4]]
        elif mode == 7:
            freq_list = [note_freq[idx],note_freq[idx+4],note_freq[idx+7],note_freq[idx+11],note_freq[idx+7],note_freq[idx+4],note_freq[idx]]
        elif mode == 8:
            freq_list = [note_freq[idx],note_freq[idx+4],note_freq[idx+7],note_freq[idx+11],note_freq[idx+12],note_freq[idx+11],note_freq[idx+7],note_freq[idx+4]]
        elif mode == 9:
            freq_list = [note_freq[idx],note_freq[idx+4],note_freq[idx+7],note_freq[idx+11],note_freq[idx+12],note_freq[idx+11],note_freq[idx+7],note_freq[idx+4],note_freq[idx]]

    return freq_list


def osc_generate(input_values, gen_type, samples):
    """Make Sound from Frequency, Type & Samples"""
    if gen_type == "sine":
        sound = aud.Sound.sine(input_values[1], samples)
    elif gen_type == "triangle":
        sound = aud.Sound.triangle(input_values[1], samples)
    elif gen_type == "square":
        sound = aud.Sound.square(input_values[1], samples)
    elif gen_type == "sawtooth":
        sound = aud.Sound.sawtooth(input_values[1], samples)
    else:
        sound = aud.Sound.silence().resample(samples, False)
    return sound
