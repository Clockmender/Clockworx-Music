import bpy
from ..cm_functions import (
   view_lock,
   get_freq,
   )

class CM_OT_EvaluateNotes(bpy.types.Operator):
   bl_idname = "cm_audio.evaluate_notes"
   bl_label = "Write Notes to Pointer"
   bl_description = "Just Writes Notes to Pointer Object"

   def execute(self, context):
       view_lock()
       scene = bpy.context.scene
       cm = bpy.context.scene.cm_pg
       cm_node = context.node
       collection = bpy.data.collections.get(cm_node.collection)
       if collection is not None:
           pointer = bpy.data.objects[cm_node.pointer]
           if pointer is not None:
               pointer["sound"] = {}
               obj_list = [o for o in collection.objects if "note" in o.name]
               num = 0
               for obj in obj_list:
                   freq = get_freq(int((obj.location.y * 10) + 9))
                   length = obj.dimensions.x * 10 * cm.time_note_min
                   delay = obj.location.x * 10 * cm.time_note_min
                   # FIXME for frame number
                   frame = int(obj.location.x * 10)
                   pointer["sound"][f"{frame}-{num}"] = [freq, delay, length]
                   num = num + 1
       return {"FINISHED"}
