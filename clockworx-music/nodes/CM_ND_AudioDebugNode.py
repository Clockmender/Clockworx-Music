import bpy
from .._base.base_node import CM_ND_BaseNode
from ..cm_functions import connected_node_output


class CM_ND_AudioDebugNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.debug_node"
    bl_label = "Display Info"
    bl_icon = "SPEAKER"
    bl_width_default = 220

    num_entries : bpy.props.IntProperty(name="Entries #")
    output : bpy.props.StringProperty(name="Output", default="")
    text_input_1 : bpy.props.StringProperty(name="Out-1", default="")
    text_input_2 : bpy.props.StringProperty(name="Out-2", default="")
    text_input_3 : bpy.props.StringProperty(name="Out-3", default="")
    text_input_4 : bpy.props.StringProperty(name="Out-4", default="")
    text_input_5 : bpy.props.StringProperty(name="Out-5", default="")
    out_term : bpy.props.BoolProperty(name="View in Terminal", default=False)

    def init(self, context):
        self.inputs.new("cm_socket.generic", "Input")

    def draw_buttons(self, context, layout):
        layout.label(text=f"Number of entries: {self.num_entries}", icon = "INFO")
        layout.prop(self, "output")
        layout.prop(self, "text_input_1", text="")
        layout.prop(self, "text_input_2", text="")
        layout.prop(self, "text_input_3", text="")
        layout.prop(self, "text_input_4", text="")
        layout.prop(self, "text_input_5", text="")
        layout.context_pointer_set("audionode", self)
        layout.operator("cm_audio.display_audio")
        layout.prop(self, "out_term")

    def function(self):
        input = connected_node_output(self, 0)
        index = 0
        is_list = False
        self.text_input_1 = ""
        self.text_input_2 = ""
        self.text_input_3 = ""
        self.text_input_4 = ""
        self.text_input_5 = ""
        if isinstance(input, list):
            self.num_entries = len(input)
            if self.out_term:
                print("Viewer: '{}'".format(self.name))
                print("  ")
                ind = 0
                for v in input:
                    print(f"Item {ind}: {v}")
                    ind = ind + 1
            else:
                self.output = str(input)
            is_list = True
            if len(input) > 0:
                input = input[0]
        if isinstance(input, dict):
            self.num_entries = len(input.keys())
            if self.out_term:
                print("Viewer: '{}'".format(self.name))
                print("  ")
                for key,value in input.items():
                    if isinstance(value, list):
                        print(f"Key: {key}")
                        ind = 0
                        for v in value:
                            print(f"Item {ind}: {v}")
                            ind = ind + 1
                    else:
                        print("Key : {} , Value : {}".format(key,value))
            if "collections" in input.keys():
                collections = input["collections"]
                if not isinstance(collections, list):
                    collections = [collections]
            elif "objects" in input.keys():
                objects = input["objects"]
                if not isinstance(objects, list):
                    objects = [objects]
            if not is_list:
                self.output = str(input)
            for i in input.keys():
                if index == 0:
                    self.text_input_1 = f"{i}: {input[i]}"
                if index == 1:
                    self.text_input_2 = f"{i}: {input[i]}"
                if index == 2:
                    self.text_input_3 = f"{i}: {input[i]}"
                if index == 3:
                    self.text_input_4 = f"{i}: {input[i]}"
                if index == 4:
                    self.text_input_5 = f"{i}: {input[i]}"
                index = index + 1
        else:
            if self.out_term:
                print(input)
            self.output = str(input)

    def info(self, context):
        self.function()

    def execute(self):
        self.function()
