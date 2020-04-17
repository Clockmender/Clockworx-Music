import bpy
from .._base.base_node import CM_ND_BaseNode

from bpy.props import (
    IntProperty,
)
from ..cm_functions import (
    connected_node_output,
    oops,
)

class CM_ND_ShapekeysNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.shapekey_node"
    bl_label = "Shapekey(s)"
    bl_icon = "SPEAKER"

    ret_num : IntProperty(name="Index", default=-1, min= -1,
        description="-1 = All")

    def draw_buttons(self, context, layout):
        layout.prop(self, "ret_num")

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.object", "Object")
        self.outputs.new("cm_socket.shapekey", "Shapekey(s)")

    def execute(self):
        cm = bpy.context.scene.cm_pg
        input = connected_node_output(self, 0)
        if input == None:
            return None
        if isinstance(input, dict):
            if "objects" in input.keys():
                objects = input["objects"]
                if isinstance(objects, list):
                    cm.error = "More Than 1 Input Object"
                    bpy.context.window_manager.popup_menu(oops, title="Error", icon="ERROR")
                    return None
                else:
                    object = objects
                    if object.type not in ("MESH", "CURVE", "LATTICE"):
                        cm.error = "Input Object is not a Mesh, Curve, or Lattice"
                        bpy.context.window_manager.popup_menu(oops, title="Error", icon="ERROR")
                        return None
            else:
                cm.error = "Input Object is not a Mesh, Curve, or Lattice"
                bpy.context.window_manager.popup_menu(oops, title="Error", icon="ERROR")
                return None

            reference = object.data.shape_keys.reference_key
            shapekey_list = list(object.data.shape_keys.key_blocks)[1:]

            if shapekey_list is not None:
                output = {}
                #output["object"] = object
                output['sk-basis'] = reference
                if self.ret_num == -1:
                    for i in range(1, len(shapekey_list) + 1):
                        shapekey = list(object.data.shape_keys.key_blocks)[i]
                        output[f"key-{shapekey.name}"] = shapekey
                    return output
                else:
                    if len(shapekey_list) > self.ret_num:
                        shapekey = list(object.data.shape_keys.key_blocks)[self.ret_num + 1]
                        output[f"key-{shapekey.name}"] = shapekey
                        return output
                    else:
                        max = len(shapekey_list) - 1
                        cm.error = f"Index Out Of Range, max: {max}"
                        bpy.context.window_manager.popup_menu(oops, title="Error", icon="ERROR")
                        return None
            else:
                cm.error = f"No Shapekey(s) Found"
                bpy.context.window_manager.popup_menu(oops, title="Error", icon="ERROR")
                return None

        cm.error = "Incorrect Input"
        bpy.context.window_manager.popup_menu(oops, title="Error", icon="ERROR")
        return None

    def output(self):
        return self.execute()

    def get_midi(self):
        return self.execute()

# active_shape_key_index
# key_blocks["fs3"].value
# shapekey.value = 1
