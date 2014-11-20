bl_info = {
    "name": "Create Deform Armature from Rig",
    "author": "Tal Hershkovich",
    "version" : (0, 1),
    "blender" : (2, 72, 0),
    "location": "Create Deform Armature from Rig in spacebar menu",
    "description": "copies the deform bones of a rig into a deform armature with copy Transforms applied ",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Rigging/DeformArmature",
    "category": "Rigging"}
    
import bpy

def create_deform_armature(self, context):
    rig = bpy.context.active_object

    if rig.type == "ARMATURE":
        #create a duplicate
        bpy.ops.object.mode_set(mode='OBJECT')
        origin_name = rig.name
        bpy.ops.object.duplicate()
        bpy.context.active_object.name = origin_name+"_deform"
        rig_deform = bpy.context.object
        
        rig_deform.name = "Armature_deform"
        rig_deform.data.name = "Armature_deform"
        
        remove_bones = []
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.layers_show_all(all=True)
        
        for bone in rig_deform.data.edit_bones:
            if bone.use_deform == False:
                remove_bones.append(bone)
                      
        for bone in remove_bones:     
            rig_deform.data.edit_bones.remove(bone)
        
        #clear all constraints
        for bone in rig_deform.pose.bones:
            for constraint in bone.constraints:
                bone.constraints.remove(constraint)
                
        #assign transformation constraints with a target to the original rig relative bones
        for bone in rig_deform.pose.bones:
            constraint = bone.constraints.new(type='COPY_TRANSFORMS')
            constraint.target = bpy.data.objects[rig.name]
            constraint.subtarget = bone.name
            
    bpy.ops.object.mode_set(mode='OBJECT')

class DeformArmature(bpy.types.Operator):
    bl_idname = 'armature.copy_deform'
    bl_label = 'Create Deform Armature from Rig'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        create_deform_armature(self, context)
        return {'FINISHED'}
    
def register():
    
    bpy.utils.register_class(DeformArmature)
    
    
def unregister():
    bpy.utils.unregister_class(DeformArmature)
    

if __name__ == "__main__":  # only for live edit.
    register()

    
