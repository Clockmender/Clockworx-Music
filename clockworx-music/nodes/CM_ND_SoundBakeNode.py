import bpy
import aud
from .._base.base_node import CM_ND_BaseNode

from bpy.props import (
    FloatProperty,
    IntProperty,
    BoolProperty,
    StringProperty,
)
from ..cm_functions import (
    get_values,
    connected_node_output,
)

class CM_ND_SoundBakeNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio_sound_bake_node"
    bl_label = "Bake Sound to Control Object"
    bl_width_default = 250
    """Bake Sound Data  to Control Object"""

    num_div : IntProperty(name="Divisions", default=5, min=1, max=20)
    max_freq : FloatProperty(name="Max Frequency", default=2000, precision=3, min=17.324, max=50000)
    min_freq : FloatProperty(name="Min Frequency", default=0, precision=3, min=0, max=30000)
    sound_file_name: StringProperty(subtype="FILE_PATH", name="File", default="//")
    sequence_channel : IntProperty(name="Channel", default=1, description="VSE Channel")
    attack : FloatProperty(name="Attack", default=0.005, precision=3, min=0.001, max = 2.0)
    release : FloatProperty(name="Release", default=0.2, precision=3, min=0.02, max = 5.0)
    threshold : FloatProperty(name="Threshold", default=0.0, precision=3, min=0.0, max = 1.0)
    sthreshold : FloatProperty(name="Square Threshold", precision=3, default=0.0, min=0.0, max=1.0)
    use_accumulate : BoolProperty(name="Use Accumulate", default=False)
    use_additive : BoolProperty(name="Use Additive", default=False)
    use_square : BoolProperty(name="Use Square", default=False)
    key_num : IntProperty(name="Control Key Number", default=1, min=1)

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.collection", "Collection")
        self.outputs.new("cm_socket.generic", "Data")

    def draw_buttons(self, context, layout):
        layout.label(text="Harmonic Frequency Breaks will be used.")
        box = layout.box()
        box.prop(self, "num_div")
        box.prop(self, "sound_file_name")
        box.prop(self, "max_freq")
        box.prop(self, "min_freq")
        box.prop(self, "attack")
        box.prop(self, "release")
        box.prop(self, "threshold")
        box.prop(self, "use_accumulate")
        box.prop(self, "use_additive")
        box.prop(self, "use_square")
        box.prop(self, "sthreshold")
        layout.separator()
        layout.prop(self, "key_num")
        layout.operator("cm_audio.create_sound_bake", icon="SOUND")
        row = layout.row()
        row.prop(self, "sequence_channel")
        row.operator("cm_audio.load_sound", icon="FILE_NEW")

    def execute(self):
        input = connected_node_output(self, 0)
        if isinstance(input, dict):
            objects = []
            if "collections" in input.keys():
                collections = input["collections"]
                if not isinstance(collections, list):
                    collection = collections
                else:
                    collection = None
        else:
            collection = None
        list_f, sum = get_values(self.num_div + 1)
        range_f = self.max_freq - self.min_freq
        breaks = []
        max_v = list_f[-1] - list_f[0]
        for r in range(len(list_f) - 1):
            frac = (list_f[r + 1] - list_f[0]) / max_v
            breaks.append(int((frac * range_f) + self.min_freq))
        output = {}
        output["file"] = self.sound_file_name
        output["collections"] = collection
        output["breaks"] = breaks
        output["range"] = range_f
        output["list_f"] = list_f
        return output

    def output(self):
        return self.execute()
