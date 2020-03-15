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
from .cm_functions import (
    view_lock,
    run_midi_always,
    start_clock,
    )


class CM_OT_PlayAudioNodeOperator(bpy.types.Operator):
    bl_idname = "cm_audio.play_audio"
    bl_label = "Play Audio"

    @classmethod
    def poll(cls, context):
        return context.audionode.get_sound() != None

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
        cm_node = context.node
        return ".flac" in cm_node.write_name

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
        context.audionode.info(context)
        return {"FINISHED"}


class CM_OT_DisplayMidiNodeOperator(bpy.types.Operator):
    bl_idname = "cm_audio.display_midi"
    bl_label = "Display Info"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        context.audionode.get_midi()
        return {"FINISHED"}


class CM_OT_ExecuteStartOperator(bpy.types.Operator):
    bl_idname = "cm_audio.execute_start"
    bl_label = "CM Execute Start"

    @classmethod
    def poll(cls, context):
        return start_clock not in bpy.app.handlers.frame_change_post

    def execute(self, context):
        cm = context.scene.cm_pg
        if start_clock not in bpy.app.handlers.frame_change_post:
            bpy.app.handlers.frame_change_post.append(start_clock)
        #if start_clock not in bpy.app.handlers.render_init:
        #    bpy.app.handlers.render_init.append(start_clock)
        return {"FINISHED"}


class CM_OT_ExecuteStopOperator(bpy.types.Operator):
    bl_idname = "cm_audio.execute_stop"
    bl_label = "CM Execute Stop"

    @classmethod
    def poll(cls, context):
        return start_clock in bpy.app.handlers.frame_change_post

    def execute(self, context):
        cm = context.scene.cm_pg
        if start_clock in bpy.app.handlers.frame_change_post:
            bpy.app.handlers.frame_change_post.remove(start_clock)
        #if start_clock in bpy.app.handlers.render_init:
        #    bpy.app.handlers.render_init.append(start_clock)
        return {"FINISHED"}


class CM_OT_MIDIStartOperator(bpy.types.Operator):
    bl_idname = "cm_audio.midi_start"
    bl_label = "CM Execute Start"

    @classmethod
    def poll(cls, context):
        return not bpy.app.timers.is_registered(run_midi_always)

    def execute(self, context):
        bpy.app.timers.register(run_midi_always)
        return {"FINISHED"}


class CM_OT_MIDIStopOperator(bpy.types.Operator):
    bl_idname = "cm_audio.midi_stop"
    bl_label = "CM Execute Stop"

    @classmethod
    def poll(cls, context):
        return bpy.app.timers.is_registered(run_midi_always)

    def execute(self, context):
        if bpy.app.timers.is_registered(run_midi_always):
            bpy.app.timers.unregister(run_midi_always)
        return {"FINISHED"}


class CM_OT_SetConstantsOperator(bpy.types.Operator):
    bl_idname = "cm_audio.set_constants"
    bl_label = "Set CM Constants"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        cm = context.scene.cm_pg
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
        cm = context.scene.cm_pg
        note_den = int(cm.note_den)
        fps = int((cm.bpm / 60 * note_den) * 100)
        bpy.context.scene.render.fps = fps
        bpy.context.scene.render.fps_base = 100
        cm.time_note_min = round((60 / cm.bpm) / note_den, 4)
        cm.duration_factor = round(note_den * cm.bpm / 600, 4)
        cm.message = "Parameters Set."
        return {"FINISHED"}

class CM_OT_impKeyb88(bpy.types.Operator):
    bl_idname = "cm_audio.impkeyb88"
    bl_label = "Import 88 key Keyboard"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self,context):
        cm = context.scene.cm_pg
        path = (str(bpy.utils.user_resource('SCRIPTS', "addons"))
            + '/clockworx-music/imports/88keys.dae')
        bpy.ops.wm.collada_import(filepath=path)
        cm.message1 = "Import 88 Key Board Completed"
        return {"FINISHED"}


class CM_OT_impKeyb61(bpy.types.Operator):
    bl_idname = "cm_audio.impkeyb61"
    bl_label = "Import 61 key Keyboard"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self,context):
        cm = context.scene.cm_pg
        path = (str(bpy.utils.user_resource('SCRIPTS', "addons"))
            + '/clockworx-music/imports/61keys.dae')
        bpy.ops.wm.collada_import(filepath=path)
        cm.message1 = "Import 61 Key Board Completed"
        return {"FINISHED"}

class CM_OT_impFrets(bpy.types.Operator):
    bl_idname = "cm_audio.impfrets"
    bl_label = "Build Fretboard"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        cm = context.scene.cm_pg
        path = (str(bpy.utils.user_resource('SCRIPTS', "addons")) +
            '/clockworx-music/imports/frets.dae')
        bpy.ops.wm.collada_import(filepath=path)
        cm.message1 = ''
        src_obj = bpy.context.view_layer.objects.get('Base-Mesh')
        src_obj.name = 'Bridge'
        src_obj.select_set(state=True)
        src_obj.scale = (cm.bridge_len, cm.bridge_len, cm.bridge_len)
        bpy.context.view_layer.objects.active = src_obj
        bpy.ops.object.transform_apply(location = False, scale = True, rotation = False)
        src_obj.select_set(state=False)
        scl = cm.scale_f
        xLoc = src_obj.location.x
        fret = cm.bridge_len

        fret_name = ['NUT','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12',
            'F13','F14','F15','F16','F17','F18','F19','F20','F21','F22','F23','F24']

        for i in range (0,25):
            bpy.ops.wm.collada_import(filepath=path)
            new_obj = bpy.context.view_layer.objects.get('Base-Mesh')
            new_obj.name = fret_name[i]
            new_obj.location.x = fret
            new_obj.scale.y = scl
            new_obj.select_set(state=True)
            bpy.context.view_layer.objects.active = new_obj
            bpy.ops.object.transform_apply(location = False, scale = True, rotation = False)
            new_obj.select_set(state=False)
            fret = fret * (0.5**(1/12))
            scl = (cm.scale_f + (((cm.bridge_len - fret) / cm.bridge_len)
                * (1 - cm.scale_f)))
        cm.message1 = "Fretboard Built in Active Collection"
        return {"FINISHED"}

class CM_OT_renMesh(bpy.types.Operator):
    bl_idname = "cm_audio.rename_objs"
    bl_label = "Rename Objects to Suffix"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        cm = context.scene.cm_pg
        if cm.col_name is not "" and cm.suffix_obj is not "":
            if bpy.data.collections.get(cm.col_name) is not None:
                for o in bpy.data.collections[cm.col_name].objects:
                    if "_" in o.name:
                        o.name = o.name.split("_")[0] + "_" + cm.suffix_obj
                    else:
                        o.name = o.name + "_" + cm.suffix_obj
                cm.message1 = ("Processed "
                    + str(len(bpy.data.collections[cm.col_name].objects))
                    + " Objects")
            else:
                cm.message1 = "Collection Does Not Exist"
                return
        else:
            cm.message1 = "Enter Collection/Siffix"
        return {"FINISHED"}


class CM_OT_UnlockView(bpy.types.Operator):
    bl_idname = "cm_audio.unlock_view"
    bl_label = "Unlock 3D View"

    @classmethod
    def poll(cls, context):
        test = True
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                test = area.spaces[0].region_3d.lock_rotation
        return test

    def execute(self, context):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].region_3d.lock_rotation = False
        return {"FINISHED"}


class CM_OT_lockView(bpy.types.Operator):
    bl_idname = "cm_audio.lock_view"
    bl_label = "Lock 3D View"

    @classmethod
    def poll(cls, context):
        test = True
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                test = area.spaces[0].region_3d.lock_rotation
        return not test

    def execute(self, context):
        view_lock()
        return {"FINISHED"}


class CM_OT_resetAccum(bpy.types.Operator):
    bl_idname = "cm_audio.reset_accu"
    bl_label = "Reset Accumulator"

    def execute(self, context):
        cm = bpy.context.scene.cm_pg
        cm.midi_data["notes_cu"] = 0
        cm.midi_data["params_cu"] = 0
        return {"FINISHED"}
