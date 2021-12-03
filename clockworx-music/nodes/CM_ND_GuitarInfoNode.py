import bpy
from bpy.props import (
   BoolProperty,
   StringProperty,
)
from .._base.base_node import CM_ND_BaseNode
from ..cm_functions import (
    get_fret_six,
    get_fret_four,
    connected_node_output,
    get_socket_values,
)

class CM_ND_GuitarInfoNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.midi_guitar_info_node"
    bl_label = "Guitar String Info"
    bl_icon = "SPEAKER"
    bl_width_default = 200

    suffix: StringProperty(name="Suffix", default="string")

    def draw_buttons(self, context, layout):
        layout.label(text="Six: 52-100 Bass: 40-79", icon="INFO")
        layout.prop(self, "suffix")

    def init(self, context):
        super().init(context)
        self.inputs.new("NodeSocketInt", "Note Index")
        self.outputs.new("cm_socket.guitar", "Guitar Data")

    def execute(self):
        cm = bpy.context.scene.cm_pg
        output = {}
        Idx = connected_node_output(self, 0)
        if Idx is not None:
            if isinstance(Idx, dict):
                if "int" in Idx.keys():
                    Idx = Idx["int"]
            else:
                return None
        else:
            sockets = self.inputs.keys()
            Idx = get_socket_values(self, sockets, self.inputs)[0]

        if not cm.mid_c:
            Idx = Idx + 12
        # 6 string
        if Idx >= 52 and Idx < 57:
            string = 'El'+'_'+self.suffix
        elif Idx >= 57 and Idx < 62:
            string = 'A'+'_'+self.suffix
        elif Idx >= 62 and Idx < 67:
            string = 'D'+'_'+self.suffix
        elif Idx >= 67 and Idx < 71:
            string = 'G'+'_'+self.suffix
        elif Idx >= 71 and Idx < 76:
            string = 'B'+'_'+self.suffix
        elif Idx >= 76 and Idx < 101:
            string = 'Et'+'_'+self.suffix
        else:
            string = 'null'
            fret = 'null'
        # Get Fret
        if string is not 'null':
            fret = get_fret_six(Idx, -52)
        # Bass
        if Idx >= 40 and Idx < 45:
            stringb = 'El'+'_'+self.suffix
        elif Idx >= 45 and Idx < 50:
            stringb = 'A'+'_'+self.suffix
        elif Idx >= 50 and Idx < 55:
            stringb = 'D'+'_'+self.suffix
        elif Idx >= 55 and Idx < 80:
            stringb = 'G'+'_'+self.suffix
        else:
            stringb = 'null'
            fretb = 'null'
        # Get Fret
        if stringb is not 'null':
            fretb = get_fret_four(Idx, -40)
        # Set Output List
        sixS = [string, fret]
        bass = [stringb, fretb]

        output["six_s"] = sixS
        output["bass"] = bass
        return output

    def output(self):
        return self.execute()
