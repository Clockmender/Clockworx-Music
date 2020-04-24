import bpy
import bmesh
from math import sin, cos, tan, pi
from mathutils import Vector

class CM_OT_WaveGenerator(bpy.types.Operator):
    bl_idname = "cm_audio.wave_generator"
    bl_label = "Generate Waves"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        cm = context.scene.cm_pg
        return cm.trig_obj is not None

    def execute(self, context):
        cm = context.scene.cm_pg
        x_inc = cm.trig_len / cm.trig_res
        if cm.trig_del:
            for v in cm.trig_obj.data.vertices:
                v.select = True
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.delete(type='VERT')
            bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(cm.trig_obj.data)

        for i in range((cm.trig_res * cm.trig_cycles) + 1):
            if cm.trig_type == "sin":
                z_val = sin((i / cm.trig_res) * pi) * cm.trig_amp
            elif cm.trig_type == "cos":
                z_val = cos((i / cm.trig_res) * pi) * cm.trig_amp
            else:
                z_val = tan((i / cm.trig_res) * pi) * cm.trig_amp
                if abs(z_val) > cm.trig_tanmax:
                    if z_val > 0:
                        z_val = cm.trig_tanmax
                    else:
                        z_val = -cm.trig_tanmax
            vert_loc = Vector(((i * x_inc), 0, z_val)) + Vector(cm.trig_off)
            vertex_new = bm.verts.new(vert_loc)
            bm.verts.ensure_lookup_table()
            if i > 0:
                bm.edges.new([bm.verts[-2], vertex_new])

        bmesh.update_edit_mesh(cm.trig_obj.data)
        bpy.ops.object.mode_set(mode='OBJECT')

        return {"FINISHED"}
