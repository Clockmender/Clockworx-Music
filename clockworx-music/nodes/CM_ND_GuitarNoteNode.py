import bpy
from bpy.types import NodeSocketInt
from .._base.base_node import CM_ND_BaseNode
from bpy.props import (
    FloatProperty,
    IntProperty,
)
from ..cm_functions import (
    connected_node_output,
    get_index,
)

class CM_ND_GuitarNoteNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.midi_guitar_note_node"
    bl_label = "Guitar Note Info"
    bl_icon = "SPEAKER"
    bl_width_default = 200

    trigger : FloatProperty(name="Trigger Point", default=1, min=0.1)
    octave_shift : IntProperty(name="Octave Shift", default=0)

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.collection", "Controls")
        self.outputs.new("NodeSocketInt", "Note Index")

    def draw_buttons(self, context, layout):
        layout.prop(self, "trigger")
        layout.prop(self, "octave_shift")

    def execute(self):
        cm = bpy.context.scene.cm_pg
        output = 0
        controls = connected_node_output(self, 0)
        if controls is None:
            return None
        if isinstance(controls, dict):
            if "collections" in controls:
                controls = controls["collections"]
            else:
                return None
        else:
            return None

        act_controls = [c for c in controls.objects if c.location.z >= self.trigger]
        if len(act_controls) == 0:
            return None
        control = act_controls[0]
        cont_name = control.name
        if "_" in cont_name:
            note_name = cont_name.split("_")[0]
            output = get_index(note_name) + self.octave_shift * 12
            return {"int": output}
        else:
            return None

    def output(self):
        return self.execute()
