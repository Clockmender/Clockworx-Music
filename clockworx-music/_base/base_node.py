import bpy

class CM_ND_BaseNode:

    def insert_link(self, link):
        # Note that this function is called BEFORE the new link is inserted into the node tree
        # So you can't delete the link in this function!
        node_tree = self.id_data
        if link not in node_tree.new_links:
            node_tree.new_links.append(link)

    def init(self, context):
        # Initialise node with data
        self.use_custom_color = True
        self.set_color()

    def set_color(self):
        if "object_" in self.bl_idname or "objects_" in self.bl_idname:
            #self.use_custom_color = True
            self.color = (0.4, 0.3, 0.4)
        elif "sound_" in self.bl_idname:
            self.color = (0.3, 0.4, 0.4)
        elif "midi_" in self.bl_idname:
            self.color = (0.4, 0.4, 0.3)
        elif "collections_" in self.bl_idname:
            self.color = (0.3, 0.4, 0.3)
        elif "bone" in self.bl_idname:
            self.color = (0.3, 0.3, 0.4)
        elif "shapekey_" in self.bl_idname:
            self.color = (0.1, 0.4, 0.1)
        elif "material_" in self.bl_idname:
            self.color = (0.1, 0.25, 0.35)
        elif "record" in self.bl_idname:
            self.color = (0.5, 0.1, 0.1)
        else:
            self.color = (0.4, 0.35, 0.3)
