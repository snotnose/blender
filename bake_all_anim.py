import bpy

old_actions = list(bpy.data.actions)
flag = True

for obj in bpy.context.selected_objects:
    if obj.type != 'ARMATURE':
        flag = False
    if obj == bpy.context.active_object:
        armature = obj
    else:
        rig = obj

#check that only 2 armatures are selected with one activated
if flag == True and len(bpy.context.selected_objects) == 2:

    for act in old_actions:
        bpy.context.active_object.select = False
        rig.select = True
        bpy.context.scene.objects.active = rig
        bpy.ops.object.posemode_toggle()
        bpy.context.object.animation_data.action = act
        #store the original name of the action
        name = act.name
        #rename the old action from the control rig
        bpy.context.object.animation_data.action.name = act.name + "_control"
        
        bpy.ops.object.posemode_toggle()
        bpy.context.active_object.select = False
        armature.select = True
        bpy.context.scene.objects.active = armature
        
        bpy.ops.nla.bake(frame_start=act.frame_range[0], frame_end=act.frame_range[1], only_selected=False, visual_keying=True, bake_types={'POSE'})
        
        #store the new action with the name of the original action
        bpy.context.object.animation_data.action.name = name
        bpy.context.object.animation_data.action.use_fake_user = True
    
    #remove all the old actions   
    for old_act in old_actions:
        for act in bpy.data.actions:
            if old_act == act:
                act.user_clear()
    
    #remove constraints from armature    
    armature.select = True
    bpy.ops.object.posemode_toggle()
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.constraints_clear()
    
else:
    print('You have to select 2 Armatures for baking')