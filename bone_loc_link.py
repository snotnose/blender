import bpy

def duplicate_bone(bone, new_name, size):
    new_bone = amt.edit_bones.new(new_name + bone.name)
    new_bone.head = bone.head
    new_bone.tail = bone.head + (bone.tail - bone.head) * size
    new_bone.roll = bone.roll
    
    #bpy.context.object.pose.bones[new_bone.name].custom_shape = None

    return new_bone

def select_layer(bone, l):
    bone.layers[l] = True
    for i in range(len(loc_bone.layers)):
        if i == l:
            bone.layers[i] = True
        else:
            bone.layers[i] = False


obj = bpy.context.object

if obj.type == 'ARMATURE':
    current_mode = obj.mode
    bpy.ops.object.mode_set(mode = 'EDIT')        
    run_script = False
    amt = bpy.context.object.data
    selected_bones = []
    for bone in amt.edit_bones:
        if bone.select == True:
            run_script = True
            selected_bones.append(bone.name)
            print(bone, 'selected')
    
    
    if run_script == True:
         
       
        for i, bone in enumerate(selected_bones):
            bpy.ops.object.mode_set(mode = 'EDIT') 
            #create location bone
            loc_bone = duplicate_bone(amt.edit_bones[bone], 'MCH-loc-', 0.6)
            amt.layers[31] = True
            select_layer(loc_bone, 31)
            
            #create parent bone
            parent_bone = duplicate_bone(amt.edit_bones[bone], 'MCH-parent-', 0.3)
            amt.layers[30] = True
            select_layer(parent_bone, 30)
            
            #create constraints
            parent_bone.parent = amt.edit_bones[bone].parent
            amt.edit_bones[bone].parent = loc_bone
            loc_bone.parent = amt.edit_bones['Master']
            loc_name = loc_bone.name
            parent_name = parent_bone.name
            
            bpy.ops.object.mode_set(mode='POSE') 
            loc = obj.pose.bones[loc_name].constraints.new('COPY_LOCATION')
            loc.target = obj
            loc.subtarget = parent_name
            #bpy.ops.object.mode_set(mode = 'EDIT')
            
    else:
        print('no bones')    
    bpy.ops.object.mode_set(mode = current_mode)
    