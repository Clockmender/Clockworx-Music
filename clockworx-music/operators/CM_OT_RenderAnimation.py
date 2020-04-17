import bpy

class CM_OT_RenderAnimation(bpy.types.Operator):
    bl_idname = "cm_audio.render_animation"
    bl_label = "Render Animation"

    @classmethod
    def poll(cls, context):
        cm_node = context.node
        return cm_node.render_dir not in ["", "//"]

    def execute(self, context):
        scene = context.scene
        cm_node = context.node
        path = bpy.path.abspath(cm_node.render_dir)
        scene.render.filepath = path
        bpy.context.scene.frame_current = cm_node.strt_frame

        for i in range(cm_node.strt_frame, cm_node.stop_frame + 1):
            scene.frame_set(i)
            scene.render.filepath = f"{path}render{i}"
            bpy.ops.render.render(write_still = True)

        return {"FINISHED"}
