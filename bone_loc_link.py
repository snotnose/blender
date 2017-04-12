import bpy

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
    for bone in amt.bones:
        if bone.select == True:
            run_script = True
            selected_bones.append(bone)
    
    if run_script == True:
        #bpy.ops.object.mode_set(mode='EDIT') 
        for bone in selected_bones:
            
            bpy.ops.armature.select_all(action='DESELECT')
            amt.edit_bones[bone.name].select = True
            amt.edit_bones[bone.name].select_head = True
            amt.edit_bones[bone.name].select_tail = True
            
            #create location bone
            bpy.ops.armature.duplicate()
            bpy.ops.transform.resize(value=(0.5, 0.5, 0.5), constraint_axis=(False, False, False), constraint_orientation='NORMAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
            loc_bone = bpy.context.selected_bones[0]
            loc_bone.name = ('MCH-loc-'+ bone.name)
            loc_bone.head = bone.head_local
            obj.pose.bones[loc_bone.name].custom_shape = None
            amt.layers[31] = True
            select_layer(loc_bone, 31)
            
            #create parent bone
            bpy.ops.armature.duplicate()
            bpy.ops.transform.resize(value=(0.5, 0.5, 0.5), constraint_axis=(False, False, False), constraint_orientation='NORMAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
            parent_bone = bpy.context.selected_editable_bones[0]
            parent_bone.name = ('MCH-parent-'+ bone.name)
            parent_bone.head = bone.head_local
            obj.pose.bones[parent_bone.name].custom_shape = None
            amt.layers[30] = True
            select_layer(parent_bone, 30)
            
            amt.edit_bones[bone.name].parent = amt.edit_bones[loc_bone.name]
            amt.edit_bones[loc_bone.name].parent = amt.edit_bones['Master']
            bpy.ops.object.mode_set(mode='POSE') 
            loc = obj.pose.bones[loc_bone.name].constraints.new('COPY_LOCATION')
            loc.target = obj
            loc.subtarget = parent_bone.name
            bpy.ops.object.mode_set(mode = 'EDIT') 
            
    else:
        print('no bones')    
    bpy.ops.object.mode_set(mode = current_mode) 
    