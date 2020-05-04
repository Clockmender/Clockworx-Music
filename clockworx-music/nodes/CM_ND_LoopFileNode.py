import bpy
import aud
from .._base.base_node import CM_ND_BaseNode
from ..cm_functions import get_socket_values, connected_node_output
from bpy.props import StringProperty

class CM_ND_LoopFileNode(bpy.types.Node, CM_ND_BaseNode):
    bl_idname = "cm_audio.loop_file_node"
    bl_label = "Loop Sounds"
    bl_icon = "SPEAKER"
    bl_width_min = 300

    c_file : StringProperty(subtype="FILE_PATH", name="C", default="//")
    cs_file : StringProperty(subtype="FILE_PATH", name="CS", default="//")
    d_file : StringProperty(subtype="FILE_PATH", name="D", default="//")
    ds_file : StringProperty(subtype="FILE_PATH", name="DS", default="//")
    e_file : StringProperty(subtype="FILE_PATH", name="E", default="//")
    f_file : StringProperty(subtype="FILE_PATH", name="F", default="//")
    fs_file : StringProperty(subtype="FILE_PATH", name="FS", default="//")
    g_file : StringProperty(subtype="FILE_PATH", name="G", default="//")
    gs_file : StringProperty(subtype="FILE_PATH", name="GS", default="//")
    a_file : StringProperty(subtype="FILE_PATH", name="A", default="//")
    as_file : StringProperty(subtype="FILE_PATH", name="AS", default="//")
    b_file : StringProperty(subtype="FILE_PATH", name="B", default="//")

    def init(self, context):
        super().init(context)
        self.inputs.new("cm_socket.note", "Note Data")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "b_file")
        layout.prop(self, "as_file")
        layout.prop(self, "a_file")
        layout.prop(self, "gs_file")
        layout.prop(self, "g_file")
        layout.prop(self, "fs_file")
        layout.prop(self, "f_file")
        layout.prop(self, "e_file")
        layout.prop(self, "ds_file")
        layout.prop(self, "d_file")
        layout.prop(self, "cs_file")
        layout.prop(self, "c_file")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        samples = cm.samples
        input = connected_node_output(self, 0)
        if input is None:
            return None
        else:
            if isinstance(input, dict):
                input = [input]

        first = True
        sound_out = None
        for notes in input:
            note_name = notes["note_name"]
            if "s" in note_name:
                note_name = note_name[0:2]
            else:
                note_name = note_name[0]
            vol = notes["note_vol"]
            rev = notes["note_rev"]
            sound_file = eval("self." + note_name + "_file")
            sound = aud.Sound.file(bpy.path.abspath(sound_file))
            sound = sound.resample(cm.samples, False).volume(vol).rechannel(cm.sound_channels)
            if rev:
                sound = sound.reverse()
            if first:
                sound_out = sound
                first = False
            else:
                sound_out = sound_out.mix(sound)

        return {"sound": sound_out}

    def output(self):
        return self.get_sound()
