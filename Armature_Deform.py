import bpy

rig = bpy.context.active_object

if rig.type == "ARMATURE":
    #create a duplicate
    bpy.ops.object.mode_set(mode='OBJECT')
    origin_name = rig.name
    bpy.ops.object.duplicate()
    bpy.context.active_object.name = origin_name+"_deform"
    rig_deform = bpy.context.object
    

    remove_bones = []
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.layers_show_all(all=True)
    bpy.ops.armature.select_all(action='TOGGLE')
    
    for bone in bpy.data.armatures[rig_deform.data.name].bones:
        if bone.use_deform == False:
            remove_bones.append(bone)
                  
    for bone in remove_bones:
        bpy.ops.object.select_pattern(pattern = bone.name)
        bpy.ops.armature.delete()
    
    #clear all constraints
    bpy.ops.object.mode_set(mode='POSE')
    rig_deform.name = "rig_deform"
    bpy.ops.pose.select_all(action='TOGGLE')
    bpy.ops.pose.constraints_clear()
    bpy.ops.pose.select_all(action='TOGGLE')
    #assign transformation constraints to the original rig

    for bone in bpy.data.armatures[rig_deform.data.name].bones:
        rig_deform.data.bones[bone.name].select = True
        rig_deform.data.bones.active = bone
        bpy.ops.pose.constraint_add(type='COPY_TRANSFORMS')
        rig_deform.pose.bones[bone.name].constraints["Copy Transforms"].target = bpy.data.objects[rig.name]
        rig_deform.pose.bones[bone.name].constraints["Copy Transforms"].subtarget = bone.name

    



        
    
