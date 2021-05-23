import bpy

class CM_OT_CreateSoundControls(bpy.types.Operator):
    bl_idname = "cm_audio.create_sound_bake"
    bl_label = "Create Sound Bake Controls in 3D View"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        cm_node = context.node
        return cm_node.execute() is not None

    def execute(self, context):
        cm_node = context.node
        input = cm_node.execute()
        if "file" in input.keys():
            path = bpy.path.abspath(input["file"])
            collection = input["collections"]
            min_freq = cm_node.min_freq
            freq_l = input["breaks"]
            freq_l.insert(0, int(cm_node.min_freq))
            if collection is not None:
                layer_collection = bpy.context.view_layer.layer_collection.children[collection.name]
                bpy.context.view_layer.active_layer_collection = layer_collection
            x_loc = 0
            for i in range(0, len(freq_l) - 1):
                bpy.context.area.type = "VIEW_3D"
                bpy.ops.object.empty_add(
                    type="SINGLE_ARROW", location=(x_loc, 0, 0), radius=0.2
                )
                obj = bpy.context.active_object
                if x_loc == 0:
                    low_f = freq_l[i]
                else:
                    low_f = freq_l[i] + 1
                obj.name = f"{low_f}-{freq_l[i + 1]}_con{cm_node.key_num}"
                obj.keyframe_insert(
                    data_path="location", index=2, frame=0
                )
                bpy.context.area.type = "GRAPH_EDITOR"
                bpy.ops.graph.sound_bake(
                    filepath=path,
                    low=low_f,
                    high=freq_l[i + 1],
                    attack=cm_node.attack,
                    release=cm_node.release,
                    threshold=cm_node.threshold,
                    use_accumulate=cm_node.use_accumulate,
                    use_additive=cm_node.use_additive,
                    use_square=cm_node.use_square,
                    sthreshold=cm_node.sthreshold
                )
                obj.select_set(state = False)

                x_loc = x_loc + 0.1

            bpy.context.area.type = "NODE_EDITOR"
            self.report({"INFO"}, f"{len(freq_l) - 1} Controls Created")
            return {"FINISHED"}
        else:
            self.report({"ERROR"}, "No filename given")
            return {"FINISHED"}
