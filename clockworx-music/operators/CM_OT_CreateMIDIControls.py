import bpy
from ..cm_functions import (
    analyse_midi_file,
    get_note,
    )

class CM_OT_CreateMIDIControls(bpy.types.Operator):
    bl_idname = "cm_audio.create_midi"
    bl_label = "Create MIDI Controls in 3D View"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        cm_node = context.node
        return ".csv" in cm_node.midi_file_name

    def execute(self, context):
        cm_node = context.node
        input = cm_node.function()
        if "collections" in input.keys():
            collection = input["collections"]
            if collection is not None:
                layer_collection = bpy.context.view_layer.layer_collection.children[collection.name]
                bpy.context.view_layer.active_layer_collection = layer_collection
        cm = context.scene.cm_pg
        path = bpy.path.abspath(cm_node.midi_file_name)
        analyse_midi_file(context)
        fps = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base
        if cm_node.make_all:
            channel_list = cm.channels.split(",")
        else:
            channel_list = []
            channel_list.append(str(cm_node.midi_channel))
        max = 0
        for channel in channel_list:
            cm.event_dict.clear()
            with open(path) as f1:
                for line in f1:
                    in_l = [elt.strip() for elt in line.split(",")]
                    if (
                        (len(in_l) == 6)
                        and (in_l[2].split("_")[0] == "Note")
                        and (in_l[0] == channel)
                        ):
                        # taken above str(cm_node.midi_channel)
                        # Note events for the chosen channel
                        noteNum = int(in_l[4]) - 12 if cm.mid_c else int(in_l[4])
                        noteName = get_note(noteNum, 0)
                        if cm_node.use_vel:
                            velo = round(int(in_l[5]) / 127, 3)
                            onOff = velo if in_l[2] == "Note_on_c" else 0.0
                        else:
                            onOff = 1.0 if in_l[2] == "Note_on_c" else 0.0
                        # time would be value * 60 / bpm * Pulse
                        frame = (
                            int(in_l[1])
                            * (60 * fps)
                            / (cm.data_dict.get("BPM") * cm.data_dict.get("Pulse"))
                        )
                        # Check frame does not overlap last entry
                        # Note cannot start before previous same note has finished!
                        if noteName in cm.event_dict.keys():  # Is not the first note event
                            lastFrame = cm.event_dict.get(noteName)[-1][0]
                            if frame <= lastFrame:
                                frame = (
                                    lastFrame + cm.spacing if cm.spacing > 0 else lastFrame + cm.easing
                                )
                        frame = frame + cm.offset
                        if noteName not in cm.event_dict.keys():
                            cm.event_dict[noteName] = [[frame, onOff]]
                        else:
                            # Add records for events
                            if cm_node.squ_val:
                                if in_l[2] == "Note_on_c":
                                    cm.event_dict[noteName].append([(frame - cm.easing), 0.0])
                                else:
                                    if cm_node.use_vel:
                                        velo = cm.data_dict.get(noteName)[-1][1]
                                        cm.event_dict[noteName].append([(frame - cm.easing), velo])
                                    else:
                                        cm.event_dict[noteName].append([(frame - cm.easing), 1.0])
                            cm.event_dict[noteName].append([frame, onOff])
                # Make Control Empties.
                xLoc = 0
                for k in cm.event_dict.keys():
                    bpy.ops.object.empty_add(
                        type="SINGLE_ARROW", location=(xLoc, int(channel) / 10, 0), radius=0.03
                    )
                    bpy.context.active_object.name = f"{str(k)}_{cm_node.suffix}{channel}"
                    if cm_node.label_cont:
                        bpy.context.active_object.show_name = True
                    indV = True
                    for v in cm.event_dict.get(k):
                        frm = v[0]
                        val = v[1]
                        if indV:
                            # add keyframe just before first Note On
                            bpy.context.active_object.location.z = 0
                            bpy.context.active_object.keyframe_insert(
                                data_path="location", index=2, frame=frm - cm.easing
                            )
                            indV = False
                        bpy.context.active_object.location.z = val / 10
                        bpy.context.active_object.keyframe_insert(
                            data_path="location", index=2, frame=frm
                        )
                    bpy.context.active_object.select_set(state=False)
                    xLoc = xLoc + 0.1
                cm_node.message1 = "Process Complete"
                max = max + sum(len(v) for v in cm.event_dict.values())
            cm_node.message2 = f"Channel(s): {channel_list} Processed, Events: {max}"

        return {"FINISHED"}
