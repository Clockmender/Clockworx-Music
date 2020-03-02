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
    bl_idname = "CM_PT_Menu"
    bl_label = "CMN Operations"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "CMN"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return True #name == "Clockworx Music Editor"

    def draw(self, context):
        cm_pg = context.scene.cm_pg
        layout = self.layout
        box = layout.box()
        box.label(text="Execution")
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
