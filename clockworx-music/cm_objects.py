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
    bl_label = "Animate Object's Location"
    bl_icon = "SPEAKER"

    control_name : StringProperty(name="Control", default="")
    object_loc : FloatVectorProperty(name="Location", subtype="XYZ", default=(0,0,0))
    factor : FloatProperty(name="Factor", default=0)
    axis_c : IntProperty(name="Control Axis", min=0, max=2, default=2)
    axis_t : IntProperty(name="Target Axis", min=0, max=2, default=2)
    object_name : StringProperty(name="Target", default="")
    animate_group : BoolProperty(name="Animate List", default=False)
    suffix : StringProperty(name="Suffix", default="obj")
    offset : FloatProperty(name="Offset (D)", default=0)
    message : StringProperty(name="Info")

    def draw_buttons(self, context, layout):
        box = layout.box()
        box.prop(self, "control_name")
        row = box.row()
        split = row.split(factor=0.35, align=True)
        split.label(text="Location")
        split.prop(self, "object_loc", text="")
        box.prop(self, "axis_c")
        box.prop(self, "factor")
        box.prop(self, "offset")
        box.prop(self, "object_name")
        box.prop(self, "axis_t")
        layout.label(text="")
        box = layout.box()
        box.prop(self, "message", text="")
        box.prop(self, "animate_group")
        box.prop(self, "suffix")


    def execute(self):
        if not self.animate_group:
            self.message = "List Function Inactive"
            obj = bpy.data.objects[self.control_name]
            if obj is not None:
                self.object_loc = obj.matrix_world.decompose()[0]
                tgt = bpy.data.objects[self.object_name]
                if tgt is not None:
                    tgt.location[self.axis_t] = (
                        (self.object_loc[self.axis_c] * self.factor) + self.offset
                        )
        else:
            search = self.control_name.split("_")[1]
            self.message = f"Using: {search} to find Controls"
            objs_list = ([o for o in bpy.data.objects
                if len(o.name.split("_")) == 2
                and o.name.split("_")[1] == search]
                )
            for obj in objs_list:
                tgt = bpy.data.objects[f"{obj.name}_{self.suffix}"]
                if tgt is not None:
                    tgt.location[self.axis_t] = (
                        (obj.location[self.axis_c] * self.factor) + self.offset
                        )


class CM_ND_ObjectRotNode(bpy.types.Node):
    bl_idname = "cm_audio.object_rot_node"
    bl_label = "Animate Object's Rotation"
    bl_icon = "SPEAKER"

    control_name : StringProperty(name="Control", default="")
    object_rot : FloatVectorProperty(name="Rotation", subtype="XYZ", default=(0,0,0))
    factor : FloatProperty(name="Factor", default=0)
    axis_c : IntProperty(name="Control Axis", min=0, max=2, default=2)
    axis_t : IntProperty(name="Target Axis", min=0, max=2, default=2)
    object_name : StringProperty(name="Target", default="")
    animate_group : BoolProperty(name="Animate List", default=False)
    suffix : StringProperty(name="Suffix", default="obj")
    offset : FloatProperty(name="Offset (D)", default=0)
    message : StringProperty(name="Info")

    def draw_buttons(self, context, layout):
        box = layout.box()
        box.prop(self, "control_name")
        row = box.row()
        split = row.split(factor=0.35, align=True)
        split.label(text="Rotation")
        split.prop(self, "object_rot", text="")
        box.prop(self, "axis_c")
        box.prop(self, "factor")
        box.prop(self, "offset")
        box.prop(self, "object_name")
        box.prop(self, "axis_t")
        layout.label(text="")
        box = layout.box()
        box.prop(self, "message", text="")
        box.prop(self, "animate_group")
        box.prop(self, "suffix")

    def execute(self):
        if not self.animate_group:
            self.message = "List Function Inactive"
            obj = bpy.data.objects[self.control_name]
            if obj is not None:
                self.object_rot = obj.matrix_world.decompose()[0]
                tgt = bpy.data.objects[self.object_name]
                if tgt is not None:
                    rot_ang = (self.object_rot[self.axis_c] * self.factor) * pi / 180
                    tgt.rotation_euler[self.axis_t] = (rot_ang + (self.offset * pi / 180))
        else:
            search = self.control_name.split("_")[1]
            self.message = f"Using: {search} to find Controls"
            objs_list = ([o for o in bpy.data.objects
                if len(o.name.split("_")) == 2
                and o.name.split("_")[1] == search
                ])
            for obj in objs_list:
                tgt = bpy.data.objects[f"{obj.name}_{self.suffix}"]
                if tgt is not None:
                    rot_ang = (obj.location[self.axis_c] * self.factor) * pi / 180
                    tgt.rotation_euler[self.axis_t] = (rot_ang + (self.offset * pi / 180))

class CM_ND_PianoRollNode(bpy.types.Node):
    bl_idname = "cm_audio.piano_roll_node"
    bl_label = "Evaluate Piano Roll"
    bl_icon = "SPEAKER"

    collection : StringProperty(name="Pianoroll", default="",
        description="Name of Collection containing the notes")
    pointer : StringProperty(name="Pointer", default="Pointer",
        description='Name of Pointer Object, this will store the sound "Recipe"')
    frame_num: bpy.props.IntProperty(name="Frame")
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
        layout.prop(self, "frame_num")
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
                snd = snd.volume(1)
                snd = snd.limit(0, data[2]).delay(data[1]).rechannel(cm.sound_channels)
                if first:
                    sound = snd
                    first = False
                else:
                    sound = sound.mix(snd)
        return sound
