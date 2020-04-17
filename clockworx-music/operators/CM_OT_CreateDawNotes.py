import bpy
from mathutils import Vector
from ..cm_functions import (
    analyse_midi_file,
    get_note,
    get_index,
    )

class CM_OT_CreateDawNotes(bpy.types.Operator):
    bl_idname = "cm_audio.create_daw_notes"
    bl_label = "Create DAW Notes in 3D View"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        cm_node = context.node
        return ".csv" in cm_node.midi_file_name

    def execute(self, context):
        cm = context.scene.cm_pg
        cm_node = context.node
        input = cm_node.function()
        if "collections" in input.keys():
            collection = input["collections"]
            if collection is not None:
                layer_collection = bpy.context.view_layer.layer_collection.children[collection.name]
                bpy.context.view_layer.active_layer_collection = layer_collection
            else:
                self.report({"INFO"}, "Using Active Collection")
        if "material" in input.keys():
            material = input["material"]
        else:
            material = None
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
                        onOff = 1.0 if in_l[2] == "Note_on_c" else 0.0
                        frame = (
                            int(in_l[1])
                            * (60 * fps)
                            / (cm.data_dict.get("BPM") * cm.data_dict.get("Pulse"))
                        )
                        frame = frame + cm.offset
                        offset = round(frame * 0.1, 2)
                        if noteName not in cm.event_dict.keys():
                            cm.event_dict[noteName] = [[offset, onOff]]
                        else:
                            cm.event_dict[noteName].append([offset, onOff])

            xLoc = 0
            for k in cm.event_dict.keys():
                y_pos = (get_index(k) + 3) / 10
                notes = cm.event_dict.get(k)
                num_notes = int(len(notes) / 2)
                for r in range(num_notes):
                    x_pos = notes[r * 2][0]
                    size = notes[(r * 2) + 1][0] - notes[r * 2][0]
                    dur = int(size * 10)
                    name = f"note_{k}-{dur}"
                    mesh = bpy.data.meshes.new("note")
                    obj = bpy.data.objects.new(name, mesh)
                    if material is not None:
                        obj.data.materials.append(material)
                    collection.objects.link(obj)
                    bpy.context.view_layer.objects.active = obj
                    obj.location = Vector((x_pos, y_pos, 0))

                    verts = [( 0.0, 0.0,  0.0),
                             ( size, 0.0,  0.0),
                             ( size, 0.1,  0.0),
                             ( 0.0, 0.1,  0.0),
                             ]
                    edges = []
                    faces = [[0, 1, 2, 3]]

                    mesh.from_pydata(verts, [], faces)
                    obj.select_set(state = False)

        return {"FINISHED"}
