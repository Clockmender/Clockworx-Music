import bpy
import aud
from ..cm_functions import get_socket_values

class CM_ND_AudioFileNode(bpy.types.Node):
    bl_idname = "cm_audio.file_node"
    bl_label = "Sound File"
    bl_icon = "SPEAKER"

    file_name_prop: bpy.props.StringProperty(subtype="FILE_PATH", name="File", default="//")

    def init(self, context):
        self.inputs.new("cm_socket.float", "Volume")
        self.inputs.new("cm_socket.float", "Start (B)")
        self.inputs.new("cm_socket.float", "Length (B)")
        self.inputs.new("cm_socket.bool", "Reverse")
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        layout.prop(self, "file_name_prop")

    def get_sound(self):
        cm = bpy.context.scene.cm_pg
        sockets = self.inputs.keys()
        input_values = get_socket_values(self, sockets, self.inputs)
        cm = bpy.context.scene.cm_pg
        sound = aud.Sound.file(bpy.path.abspath(self.file_name_prop))
        sound = sound.volume(input_values[0])
        start = input_values[1] * (60 / cm.bpm)
        stop = start + (input_values[2] * (60 / cm.bpm))
        sound = sound.limit(start, stop)
        if input_values[3]:
            sound = sound.reverse()
        sound = sound.rechannel(cm.sound_channels)
        return sound
