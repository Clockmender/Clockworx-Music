import bpy
import aud

from ..cm_functions import (
    connected_node_sound,
)


class CM_ND_AudioSlicerNode(bpy.types.Node):
    bl_idname = "cm_audio.slicer_node"
    bl_label = "Audio Slicer"
    bl_icon = "SPEAKER"

    slices_num : bpy.props.IntProperty(name="Slices #", default=5, min=2)
    slices_length : bpy.props.FloatProperty(name="Length (B)", default=1, min=0.001)
    slices_seq : bpy.props.StringProperty(name="", default="1,2,3,4,5",
        description="Playback Sequence - slice numbers from 1")
    slices_rev : bpy.props.StringProperty(name="", default="",
        description="Positions in Sequence to reverse")
    volume : bpy.props.FloatProperty(name="Volume", default=1, min=0.1)

    def init(self, context):
        self.inputs.new("cm_socket.sound", "Audio")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, "slices_num")
        row.prop(self, "slices_length")
        row = layout.row()
        split = row.split(factor=0.30, align=True)
        split.label(text="Sequence")
        split.prop(self, "slices_seq")
        row = layout.row()
        split = row.split(factor=0.30, align=True)
        split.label(text="Reversals")
        split.prop(self, "slices_rev")
        row = layout.row()
        split = row.split(factor=0.30, align=True)
        split.label(text="")
        split.prop(self, "volume")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sound = connected_node_sound(self, 0)
        sound_out = None
        if sound == None or self.slices_num < 2 or "," not in self.slices_seq:
            return None
        length = self.slices_length * (60 / cm.bpm)
        start = 0
        stop = start + length
        params = []
        for i in range(self.slices_num):
            params.append([start, stop])
            start = start + length
            stop = stop + length
        first = True
        reversals = self.slices_rev.split(",")
        ind_r = 1
        for r in self.slices_seq.split(","):
            # FIXME Check it's an integer
            ind = int(r) - 1
            start = params[ind][0]
            stop = params[ind][1]
            if first:
                sound_out = sound.limit(start, stop).volume(self.volume)
                if str(ind_r) in reversals:
                    sound_out = sound_out.reverse().volume(self.volume)
                first = False
            else:
                snd = sound.limit(start, stop).volume(self.volume)
                if str(ind_r) in reversals:
                    snd = snd.reverse().volume(self.volume)
                sound_out = sound_out.join(snd)
            ind_r = ind_r + 1
        return sound_out
