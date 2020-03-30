import bpy
from ..cm_functions import connected_node_output


class CM_ND_AudioDebugNode(bpy.types.Node):
    bl_idname = "cm_audio.debug_node"
    bl_label = "Display Input Values"
    bl_icon = "SPEAKER"
    bl_width_default = 220

    num_entries : bpy.props.IntProperty(name="Entries #")
    output : bpy.props.StringProperty(name="Output", default="")
    text_input_1: bpy.props.StringProperty(name="Out-1", default="")
    text_input_2: bpy.props.StringProperty(name="Out-2", default="")
    text_input_3: bpy.props.StringProperty(name="Out-3", default="")
    text_input_4: bpy.props.StringProperty(name="Out-4", default="")
    text_input_5: bpy.props.StringProperty(name="Out-5", default="")

    def init(self, context):
        self.inputs.new("cm_socket.generic", "Input")

    def draw_buttons(self, context, layout):
        layout.prop(self, "num_entries")
        layout.prop(self, "output")
        layout.prop(self, "text_input_1", text="")
        layout.prop(self, "text_input_2", text="")
        layout.prop(self, "text_input_3", text="")
        layout.prop(self, "text_input_4", text="")
        layout.prop(self, "text_input_5", text="")
        layout.context_pointer_set("audionode", self)
        layout.operator("cm_audio.display_audio")

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
            self.output = str(input)
            is_list = True
            if len(input) > 0:
                input = input[0]
        if isinstance(input, dict):
            if "collections" in input.keys():
                collections = input["collections"]
                if not isinstance(collections, list):
                    collections = [collections]
                self.num_entries = len(collections)
            elif "objects" in input.keys():
                objects = input["objects"]
                if not isinstance(objects, list):
                    objects = [objects]
                self.num_entries = len(objects)
            else:
                self.num_entries = len(input.keys())
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
            self.output = str(input)

    def info(self, context):
        self.function()

    def execute(self):
        self.function()
