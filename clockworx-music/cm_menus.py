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
# Author: Alan Odom (Clockmender), Rune Morling (ermo) Copyright (c) 2019
# -----------------------------------------------------------------------
#
import bpy
from bpy.types import Panel
from bpy.props import (
    IntProperty,
    FloatProperty,
    PointerProperty,
    EnumProperty,
    StringProperty,
    BoolProperty,
)

class CM_PT_PanelDesign(Panel):
    bl_idname = "CM_PT_Menu_Node"
    bl_label = "CMN Operations"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "CMN"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == "cm_AudioNodeTree" and
            context.area.type == "NODE_EDITOR")

    def draw(self, context):
        layout = self.layout
        cm_pg = context.scene.cm_pg
        box = layout.box()
        box.label(text="Execution on Frame Change")
        row = box.row()
        row.operator("cm_audio.execute_start", text="Start", icon="PLAY")
        row.operator("cm_audio.execute_stop", text="Stop", icon="SNAP_FACE")
        layout.label(text="CM Constants")
        layout.prop(cm_pg, "bpm")
        layout.prop(cm_pg, "time_sig_num")
        layout.prop(cm_pg, "time_sig_den")
        layout.prop(cm_pg, "samples")
        row = layout.row()
        split = row.split(factor=0.70, align=True)
        split.label(text="Note Denominator")
        split.prop(cm_pg, "note_den", text="")
        layout.operator("cm_audio.set_constants_menu", icon="PLAY_SOUND")
        layout.label(text="Other CM Parameters")
        layout.prop(cm_pg, "offset")
        row = layout.row()
        row.prop(cm_pg, "sound_channels")
        row.prop(cm_pg, "mid_c")
        layout.prop(cm_pg, "type_bool")
        layout.prop(cm_pg, "message")


class CM_PT_PanelView(Panel):
    bl_idname = "CM_PT_Menu_View"
    bl_label = "CMN Operations"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "CMN"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        cm_pg = context.scene.cm_pg
        layout = self.layout
        box = layout.box()
        box.label(text="Imports")
        box.operator("cm_audio.impkeyb88", icon="FILE_NEW")
        box.operator("cm_audio.impkeyb61", icon="FILE_NEW")
        box.prop(cm_pg, "bridge_len")
        box.prop(cm_pg, "scale_f")
        box.operator("cm_audio.impfrets", icon="FILE_NEW")
        box = layout.box()
        box.label(text="Utilities")
        row = box.row()
        split = row.split(factor=0.4, align=True)
        split.label(text="Collection")
        split.prop(cm_pg, "col_name", text="")
        row = box.row()
        split = row.split(factor=0.4, align=True)
        split.label(text="Suffix")
        split.prop(cm_pg, "suffix_obj", text="")
        box.operator("cm_audio.rename_objs", icon = "PREFERENCES")
        row = layout.row()
        row.prop(cm_pg, "message1")
        row = layout.row()
        row.operator("cm_audio.lock_view", icon="URL", text="")
        row.label(text="View Lock (Pianoroll)")
        row.operator("cm_audio.unlock_view", icon="WORLD", text="")
