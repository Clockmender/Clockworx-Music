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
import os
import aud
import bpy
from pathlib import Path
from .cm_functions import view_lock


class CM_OT_PlayAudioNodeOperator(bpy.types.Operator):
    bl_idname = "cm_audio.play_audio"
    bl_label = "Play Audio"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        sound = context.audionode.get_sound()
        if sound != None:
            aud.Device().play(sound)
        return {"FINISHED"}


class CM_OT_StopAudioNodeOperator(bpy.types.Operator):
    bl_idname = "cm_audio.stop_audio"
    bl_label = "Stop Audio"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        sound = context.audionode.get_sound()
        if sound != None:
            aud.Device().stopAll()
        return {"FINISHED"}


class CM_OT_WriteAudioNodeOperator(bpy.types.Operator):
    bl_idname = "cm_audio.write_audio"
    bl_label = "Write Audio"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        cm_node = context.node
        cm = context.scene.cm_pg
        path = bpy.path.abspath(cm_node.write_name)
        my_file = Path(path)
        if my_file.is_file():
            os.remove(path)
        sound = context.audionode.get_sound()
        snd_out = sound.write(path, aud.RATE_16000, aud.CHANNELS_STEREO,
            aud.FORMAT_FLOAT32, aud.CONTAINER_FLAC, aud.CODEC_FLAC)
        if cm_node.add_file:
            bps = cm.bpm / 60
            fps = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base
            frame = ((cm_node.time_off * (1 / bps)) * fps) + cm.offset
            scene = context.scene
            if not scene.sequence_editor:
                scene.sequence_editor_create()
            soundstrip = scene.sequence_editor.sequences.new_sound(
                "Sound", path, cm_node.sequence_channel, frame,
            )
            soundstrip.show_waveform = True
            if cm_node.strip_name != "":
                soundstrip.name = cm_node.strip_name
        return {"FINISHED"}


class CM_OT_DisplayAudioNodeOperator(bpy.types.Operator):
    bl_idname = "cm_audio.display_audio"
    bl_label = "Display Info"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        context.audionode.execute()
        return {"FINISHED"}


def start_clock(scene):
    for nodetree in [
        n for n in bpy.data.node_groups if n.rna_type.name == "Clockworx Music Editor"
        ]:
        for n in nodetree.nodes:
            if (hasattr(n, "execute")):
                n.execute()


class CM_OT_ExecuteStartOperator(bpy.types.Operator):
    bl_idname = "cm_audio.execute_start"
    bl_label = "CM Execute Start"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = context.scene
        cm = scene.cm_pg
        if "start_clock" not in bpy.app.handlers.frame_change_post:
            bpy.app.handlers.frame_change_post.append(start_clock)
        #view_lock()
        return {"FINISHED"}


class CM_OT_ExecuteStopOperator(bpy.types.Operator):
    bl_idname = "cm_audio.execute_stop"
    bl_label = "CM Execute Stop"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = context.scene
        cm = scene.cm_pg
        if "start_clock" in bpy.app.handlers.frame_change_post:
            bpy.app.handlers.frame_change_post.remove(start_clock)
        return {"FINISHED"}


class CM_OT_SetConstantsOperator(bpy.types.Operator):
    bl_idname = "cm_audio.set_constants"
    bl_label = "Set CM Constants"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = context.scene
        cm = scene.cm_pg
        cm_node = context.node
        cm.bpm = cm_node.bpm
        cm.time_sig_num = cm_node.time_sig_num
        cm.time_sig_den = cm_node.time_sig_den
        cm.samples = cm_node.samples
        if cm_node.note_den in [1, 2, 4, 8, 16, 32, 64]:
            fps = int((cm_node.bpm / 60 * cm_node.note_den) * 100)
            bpy.context.scene.render.fps = fps
            bpy.context.scene.render.fps_base = 100
            cm.note_den = cm_node.note_den
            cm.time_note_min = round((60 / cm_node.bpm) / cm_node.note_den, 4)
            cm.duration_factor = round(cm_node.note_den * cm_node.bpm / 600, 4)
            cm_node.message = ""
        else:
            cm_node.message = "Note Den must be 1,2,4,8,16,32 or 64"
        cm_node.message = "Parameters Set."
        return {"FINISHED"}


class CM_OT_SetConstantsMenu(bpy.types.Operator):
    bl_idname = "cm_audio.set_constants_menu"
    bl_label = "Setup Blend File Parameters"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = context.scene
        cm = scene.cm_pg
        note_den = int(cm.note_den)
        fps = int((cm.bpm / 60 * note_den) * 100)
        bpy.context.scene.render.fps = fps
        bpy.context.scene.render.fps_base = 100
        cm.time_note_min = round((60 / cm.bpm) / note_den, 4)
        cm.duration_factor = round(note_den * cm.bpm / 600, 4)
        cm.message = "Parameters Set."
        return {"FINISHED"}
