import bpy
from .._base.base_node import CM_ND_BaseNode

from bpy.props import (
    StringProperty,
    IntProperty,
)
from ..cm_functions import (
    connected_node_output,
    oops,
)

class CM_ND_BonesNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.bones_node"
    bl_label = "Bone(s): Filtered"
    bl_icon = "SPEAKER"

    bone : StringProperty(name="Bone", default="")

    def draw_buttons(self, context, layout):
        layout.prop(self, "bone")

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.object", "Armature")
        self.outputs.new("cm_socket.bone", "Bone")

    def execute(self):
        cm = bpy.context.scene.cm_pg
        input = connected_node_output(self, 0)
        if input == None:
            return None
        if isinstance(input, dict):
            if "objects" in input.keys():
                objects = input["objects"]
                if isinstance(objects, list):
                    cm.error = "More Than 1 Input Armature"
                    bpy.context.window_manager.popup_menu(oops, title="Error", icon="ERROR")
                    return None
                else:
                    object = objects
                    if object.type != "ARMATURE":
                        cm.error = "Input Object is not an Armature"
                        bpy.context.window_manager.popup_menu(oops, title="Error", icon="ERROR")
                        return None
            else:
                cm.error = "Input is not an Object"
                bpy.context.window_manager.popup_menu(oops, title="Error", icon="ERROR")
                return None

            bone_list = [b for b in object.pose.bones if self.bone in b.name]
            if len(bone_list) == 1:
                bone = bone_list[0]
                cm.message = f"'{object.name}'-'{bone.name}' Returned"
                return {"bones": bone}
            elif len(bone_list) > 1:
                cm.message = f"List of Bones Returned"
                return{"bones": bone_list}
            else:
                cm.error = f"No Bone Found"
                bpy.context.window_manager.popup_menu(oops, title="Error", icon="ERROR")
                return None

        cm.error = "Incorrect Input"
        bpy.context.window_manager.popup_menu(oops, title="Error", icon="ERROR")
        return None

    def output(self):
        return self.execute()

    def get_midi(self):
        return self.execute()
