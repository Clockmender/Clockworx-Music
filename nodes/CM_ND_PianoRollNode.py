import aud
import bpy

from bpy.props import (
    IntProperty,
    FloatProperty,
    EnumProperty,
    StringProperty,
)
from ..cm_functions import (
    osc_generate,
    get_freq,
)
from ..cm_functions import start_piano


class CM_ND_PianoRollNode(bpy.types.Node):
    bl_idname = "cm_audio.piano_roll_node"
    bl_label = "Evaluate Piano Roll"
    bl_icon = "SPEAKER"

    collection : StringProperty(name="Pianoroll", default="",
        description="Name of Collection containing the notes")
    pointer : StringProperty(name="Pointer", default="Pointer",
        description='Name of Pointer Object, this will store the sound "Recipe"')
    frame_num: bpy.props.IntProperty(name="Frame", description="System Variable, do not set")
    volume : FloatProperty(name="Volume", default=1, min=0.1)
    gen_type: EnumProperty(
        items=(
            ("sine", "Sine", "Sine Waveform"),
            ("triangle", "Triangle", "Triangle Waveform"),
            ("square", "Square", "Square Waveform"),
            ("sawtooth", "Sawtooth", "Sawtooth Waveform"),
            ("silence", "Silence", "Silence - no Waveform"),
        ),
        name="Waveform",
        default="sine",
        description="Waveform for Sound",
    )

    def init(self, context):
        self.outputs.new("cm_socket.sound", "Audio")

    def draw_buttons(self, context, layout):
        cm_pg = context.scene.cm_pg
        layout.prop(self, "collection")
        layout.prop(self, "pointer")
        row = layout.row()
        #row.prop(self, "frame_num")
        row.prop(self, "volume")
        layout.prop(self, "gen_type")
        layout.label(text="")
        layout.operator("cm_audio.evaluate_notes", icon="LONGDISPLAY")
        layout.operator("cm_audio.evaluate_piano", icon="LONGDISPLAY")
        layout.operator("cm_audio.evaluate_piano_stop", icon="CANCEL")

    def evaluate(self):
        snd = None
        scene = bpy.context.scene
        cm = bpy.context.scene.cm_pg
        self.frame_num = bpy.context.scene.frame_current
        if self.frame_num >= bpy.context.scene.frame_end:
            bpy.ops.screen.animation_cancel(restore_frame=True)
            bpy.app.handlers.frame_change_post.remove(start_piano)
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    area.spaces[0].region_3d.view_location.x = (
                        area.spaces[0].region_3d.view_location.x
                        -  (self.frame_num * 0.1))
        else:
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    area.spaces[0].region_3d.view_location.x = (
                        area.spaces[0].region_3d.view_location.x + 0.1)
        collection = bpy.data.collections.get(self.collection)
        if collection is not None:
            pointer = bpy.data.objects[self.pointer]
            if pointer is not None:
                if self.frame_num < cm.offset:
                    pointer.location.x = -0.1
                    pointer["sound"] = {}
                if self.frame_num >= cm.offset:
                    pointer.location.x = (self.frame_num - cm.offset) * 0.1
                if self.frame_num == bpy.context.scene.frame_end:
                    pointer.location.x = -0.1
                obj_list = ([o for o in collection.objects if "note" in o.name
                    and pointer.location.x - 0.001 < o.location.x < pointer.location.x + 0.001]
                    )
                num = 0
                for obj in obj_list:
                    freq = get_freq(int((obj.location.y * 10) + 9))
                    length = obj.dimensions.x * 10 * cm.time_note_min
                    delay = self.frame_num * cm.time_note_min
                    pointer["sound"][f"{self.frame_num}-{num}"] = [freq, delay, length]
                    snd = osc_generate([0,freq], self.gen_type, cm.samples)
                    snd = snd.limit(0, length).rechannel(cm.sound_channels)
                    snd = snd.volume(self.volume)
                    num = num + 1
                    aud.Device().play(snd)

    def get_sound(self):
        sound = None
        cm = bpy.context.scene.cm_pg
        pointer = bpy.data.objects[self.pointer]
        if len(pointer["sound"].keys()) > 0:
            keys = pointer["sound"].keys()
            first = True
            for key in keys:
                data = pointer["sound"][key]
                snd = osc_generate([0,data[0]], self.gen_type, cm.samples)
                snd = snd.volume(self.volume)
                snd = snd.limit(0, data[2]).delay(data[1]).rechannel(cm.sound_channels)
                if first:
                    sound = snd
                    first = False
                else:
                    sound = sound.mix(snd)
        return sound
