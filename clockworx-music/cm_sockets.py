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
from bpy.props import (
    IntProperty,
    FloatProperty,
    PointerProperty,
    EnumProperty,
    StringProperty,
    IntProperty,
)

class CM_SK_AudioNodeSocket(bpy.types.NodeSocket):
    bl_idname = "cm_socket.sound"
    bl_label = "Sound Socket"

    def draw(self, context, layout, node, x):
        layout.label(text=self.name)

    def draw_color(self, context, node):
        return (1, 0.5, 0, 0.6)

class CM_SK_FloatNodeSocket(bpy.types.NodeSocket):
    bl_idname = "cm_socket.float"
    bl_label = "Float Socket"

    def prop_update(self, context):
        self.id_data.update()

    value: bpy.props.FloatProperty(default = 0.0, update=prop_update)

    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def draw_color(self, context, node):
        return (0.8, 0.8, 0.8, 0.6)


class CM_SK_IntNodeSocket(bpy.types.NodeSocket):
    bl_idname = "cm_socket.int"
    bl_label = "Integer Socket"

    def prop_update(self, context):
        self.id_data.update()

    value: bpy.props.IntProperty(default = 0, update=prop_update)

    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def draw_color(self, context, node):
        return (0.3, 0.7, 0.9, 0.6)


class CM_SK_BoolNodeSocket(bpy.types.NodeSocket):
    bl_idname = "cm_socket.bool"
    bl_label = "Boolean Node Socket"
    dataType = "Boolean"
    allowedInputTypes = ["Boolean"]

    def prop_update(self, context):
        self.id_data.update()

    value: bpy.props.BoolProperty(default = False, update=prop_update)

    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def draw_color(self, context, node):
        return (0.9, 0.9, 0.3, 0.6)

class CM_SK_TextNodeSocket(bpy.types.NodeSocket):
    bl_idname = "cm_socket.text"
    bl_label = "Text Socket"

    def prop_update(self, context):
        self.id_data.update()

    value: bpy.props.StringProperty(default = "", update=prop_update)

    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def draw_color(self, context, node):
        return (0.01, 0.9, 0.3, 0.6)


class CM_SK_GenericNodeSocket(bpy.types.NodeSocket):
    bl_idname = "cm_socket.generic"
    bl_label = "Generic Socket"

    def prop_update(self, context):
        self.id_data.update()

    value: bpy.props.StringProperty(default = "", update=prop_update)

    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def draw_color(self, context, node):
        return (0.6, 0.3, 0.3, 1.0)
