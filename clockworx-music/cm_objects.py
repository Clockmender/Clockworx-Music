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
from math import pi
from mathutils import Vector, Euler

from bpy.props import (
    IntProperty,
    FloatProperty,
    FloatVectorProperty,
    PointerProperty,
    EnumProperty,
    StringProperty,
    BoolProperty,
)
from .cm_sockets import (
    CM_SK_AudioNodeSocket,
    CM_SK_FloatNodeSocket,
    CM_SK_IntNodeSocket,
    CM_SK_BoolNodeSocket,
    CM_SK_TextNodeSocket,
)
from .cm_functions import (
    get_index,
    get_freq,
    osc_generate,
    view_lock,
)

def start_piano(scene):
    for nodetree in [
        n for n in bpy.data.node_groups if n.rna_type.name == "Clockworx Music Editor"
        ]:
        for n in nodetree.nodes:
            if (hasattr(n, "evaluate")):
                n.evaluate()


class CM_OT_GetName(bpy.types.Operator):
    """Set from Active Obect"""

    bl_idname = "cm_audio.get_name"
    bl_label = ""

    def execute(self, context):
        cm_node = context.node
        obj = context.view_layer.objects.active
        if obj is not None:
            cm_node.control_name = obj.name
        return {"FINISHED"}


class CM_OT_GetTarget(bpy.types.Operator):
    """Set from Active Obect"""

    bl_idname = "cm_audio.get_target"
    bl_label = ""

    def execute(self, context):
        cm_node = context.node
        obj = context.view_layer.objects.active
        if obj is not None:
            cm_node.object_name = obj.name
        return {"FINISHED"}


class CM_OT_GetSuffix(bpy.types.Operator):
    """Set from Active Obect"""

    bl_idname = "cm_audio.get_suffix"
    bl_label = ""

    def execute(self, context):
        cm_node = context.node
        obj = context.view_layer.objects.active
        if obj is not None:
            cm_node.suffix = obj.name.split("_")[2]
        return {"FINISHED"}


class CM_OT_UnlockView(bpy.types.Operator):
    bl_idname = "cm_audio.unlock_view"
    bl_label = "Unlock"

    def execute(self, context):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].region_3d.lock_rotation = False
        return {"FINISHED"}


class CM_OT_EvaluatePiano(bpy.types.Operator):
    bl_idname = "cm_audio.evaluate_piano"
    bl_label = "Play & Write Notes to Pointer"

    def execute(self, context):
        view_lock()
        bpy.app.handlers.frame_change_post.append(start_piano)
        bpy.ops.screen.animation_play(reverse=False, sync=False)
        return {"FINISHED"}


class CM_OT_EvaluateNotes(bpy.types.Operator):
    bl_idname = "cm_audio.evaluate_notes"
    bl_label = "Write Notes to Pointer"

    def execute(self, context):
        view_lock()
        scene = bpy.context.scene
        cm = bpy.context.scene.cm_pg
        cm_node = context.node
        collection = bpy.data.collections.get(cm_node.collection)
        if collection is not None:
            pointer = bpy.data.objects[cm_node.pointer]
            if pointer is not None:
                pointer["sound"] = {}
                obj_list = [o for o in collection.objects if "note" in o.name]
                num = 0
                for obj in obj_list:
                    freq = get_freq(int((obj.location.y * 10) + 9))
                    length = obj.dimensions.x * 10 * cm.time_note_min
                    delay = obj.location.x * 10 * cm.time_note_min
                    # FIXME for frame number
                    frame = int(obj.location.x * 10)
                    pointer["sound"][f"{frame}-{num}"] = [freq, delay, length]
                    num = num + 1
        return {"FINISHED"}


class CM_ND_ObjectLocNode(bpy.types.Node):
    bl_idname = "cm_audio.object_loc_node"
    bl_label = "Animate Objects"
    bl_icon = "SPEAKER"

    control_name : StringProperty(name="Control", default="")
    factor_x : FloatProperty(name="Factor X", default=1)
    factor_y : FloatProperty(name="Factor Y", default=1)
    factor_z : FloatProperty(name="Factor Z", default=1)
    lx_bool : BoolProperty(name="X", default=False)
    ly_bool : BoolProperty(name="Y", default=False)
    lz_bool : BoolProperty(name="Z", default=False)
    object_name : StringProperty(name="Target", default="")
    animate_group : BoolProperty(name="Animate List", default=False)
    suffix : StringProperty(name="Suffix", default="obj")
    message : StringProperty(name="Info")
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


    def draw_buttons(self, context, layout):
        box = layout.box()
        box.prop(self, "anim_type")
        row = box.row()
        row.prop(self, "control_name")
        row.operator("cm_audio.get_name", text="", icon="EYEDROPPER")
        row = box.row()
        box.prop(self, "factor_x")
        box.prop(self, "factor_y")
        box.prop(self, "factor_z")
        row = box.row()
        row.prop(self, "lx_bool")
        row.prop(self, "ly_bool")
        row.prop(self, "lz_bool")
        row = box.row()
        row.prop(self, "object_name")
        row.operator("cm_audio.get_target", text="", icon="EYEDROPPER")
        layout.label(text="")
        box = layout.box()
        box.prop(self, "message", text="")
        box.prop(self, "animate_group")
        row = box.row()
        row.prop(self, "suffix")
        row.operator("cm_audio.get_suffix", text="", icon="EYEDROPPER")

    def execute(self):
        def off_set(obj):
            a_offset = obj.matrix_world.decompose()[0].z
            x_loc = 0
            y_loc = 0
            z_loc = 0
            if self.lx_bool:
                x_loc = a_offset * self.factor_x
            if self.ly_bool:
                y_loc = a_offset * self.factor_y
            if self.lz_bool:
                z_loc = a_offset * self.factor_z
            return (
                Vector((x_loc, y_loc, z_loc)),
                Euler(((x_loc * pi / 18), (y_loc * pi / 18), (z_loc * pi / 18))),
                Vector(((1 + x_loc), (1 + y_loc), (1 + z_loc)))
                )

        if not self.animate_group:
            self.message = "List Function Inactive"
            obj = bpy.data.objects[self.control_name]
            if obj is not None:
                vector_delta, euler_delta, scale_delta = off_set(obj)
                tgt_obj = bpy.data.objects[self.object_name]
                if tgt_obj is not None:
                    if self.anim_type == "loc":
                        tgt_obj.delta_location = vector_delta
                    elif self.anim_type == "rot":
                        tgt_obj.delta_rotation_euler = euler_delta
                    else:
                        tgt_obj.delta_scale = scale_delta

        else:
            search = self.control_name.split("_")[1]
            self.message = f"Using: '{search}' to find Controls"
            objs_list = ([o for o in bpy.data.objects
                if len(o.name.split("_")) == 2
                and o.name.split("_")[1] == search]
                )
            for obj in objs_list:
                vector_delta, euler_delta, scale_delta = off_set(obj)
                tgt_obj = bpy.data.objects[f"{obj.name}_{self.suffix}"]
                if self.anim_type == "loc":
                    tgt_obj.delta_location = vector_delta
                elif self.anim_type == "rot":
                    tgt_obj.delta_rotation_euler = euler_delta
                else:
                    tgt_obj.delta_scale = scale_delta


class CM_ND_PianoRollNode(bpy.types.Node):
    bl_idname = "cm_audio.piano_roll_node"
    bl_label = "Evaluate Piano Roll"
    bl_icon = "SPEAKER"

    collection : StringProperty(name="Pianoroll", default="",
        description="Name of Collection containing the notes")
    pointer : StringProperty(name="Pointer", default="Pointer",
        description='Name of Pointer Object, this will store the sound "Recipe"')
    frame_num: bpy.props.IntProperty(name="Frame")
    volume : FloatProperty(name="Volume", default=1, min=0.1)
    gen_type: EnumProperty(
        items=(
            ("sine", "Sine", "Sine Waveform"),
            ("triangle", "Triangle", "Triangle Waveform"),
            ("square", "Square", "Square Waveform"),
            ("sawtooth", "Sawtooth", "Sawtooth Waveform"),
            ("silence", "Silence", "Silence - no Waveform"),
        ),
        name="Waveform",
        default="sine",
        description="Waveform for Sound",
    )

    def init(self, context):
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        cm_pg = context.scene.cm_pg
        layout.prop(self, "collection")
        layout.prop(self, "pointer")
        #layout.prop(cm_pg, "time_note_min")
        row = layout.row()
        row.prop(self, "frame_num")
        row.prop(self, "volume")
        layout.prop(self, "gen_type")
        layout.label(text="")
        layout.operator("cm_audio.evaluate_piano", icon="LONGDISPLAY")
        layout.operator("cm_audio.evaluate_notes", icon="LONGDISPLAY")
        row = layout.row()
        row.operator("cm_audio.unlock_view", icon="WORLD", text="")

    def evaluate(self):
        snd = None
        scene = bpy.context.scene
        cm = bpy.context.scene.cm_pg
        self.frame_num = bpy.context.scene.frame_current
        if self.frame_num >= bpy.context.scene.frame_end:
            bpy.ops.screen.animation_cancel(restore_frame=True)
            bpy.app.handlers.frame_change_post.remove(start_piano)
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    area.spaces[0].region_3d.view_location.x = (
                        area.spaces[0].region_3d.view_location.x
                        -  (self.frame_num * 0.1))
        else:
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    area.spaces[0].region_3d.view_location.x = (
                        area.spaces[0].region_3d.view_location.x + 0.1)
        collection = bpy.data.collections.get(self.collection)
        if collection is not None:
            pointer = bpy.data.objects[self.pointer]
            if pointer is not None:
                if self.frame_num < cm.offset:
                    pointer.location.x = -0.1
                    pointer["sound"] = {}
                if self.frame_num >= cm.offset:
                    pointer.location.x = (self.frame_num - cm.offset) * 0.1
                if self.frame_num == bpy.context.scene.frame_end:
                    pointer.location.x = -0.1
                obj_list = ([o for o in collection.objects if "note" in o.name
                    and pointer.location.x - 0.001 < o.location.x < pointer.location.x + 0.001]
                    )
                num = 0
                for obj in obj_list:
                    freq = get_freq(int((obj.location.y * 10) + 9))
                    length = obj.dimensions.x * 10 * cm.time_note_min
                    delay = self.frame_num * cm.time_note_min
                    pointer["sound"][f"{self.frame_num}-{num}"] = [freq, delay, length]
                    snd = osc_generate([0,freq], self.gen_type, cm.samples)
                    snd = snd.limit(0, length).rechannel(cm.sound_channels)
                    snd = snd.volume(self.volume)
                    num = num + 1
                    aud.Device().play(snd)

    def get_sound(self):
        sound = None
        cm = bpy.context.scene.cm_pg
        pointer = bpy.data.objects[self.pointer]
        if len(pointer["sound"].keys()) > 0:
            keys = pointer["sound"].keys()
            first = True
            for key in keys:
                data = pointer["sound"][key]
                snd = osc_generate([0,data[0]], self.gen_type, cm.samples)
                snd = snd.volume(self.volume)
                snd = snd.limit(0, data[2]).delay(data[1]).rechannel(cm.sound_channels)
                if first:
                    sound = snd
                    first = False
                else:
                    sound = sound.mix(snd)
        return sound
