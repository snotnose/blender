#Select a chain of bones that has a single hierarchy in edit mode, and run the script to create a spline, hooks, and a new armature with only the selected spline bones. 
#Later I will connect the Original Armature to the hooks automatically as well, so it will be automatically the control rig

import bpy

selected = bpy.context.selected_bones


def createMesh(name, origin, verts, edges, faces):
    # Create mesh and object
    me = bpy.data.meshes.new(name)
    ob = bpy.data.objects.new(name, me)
    ob.location = origin
    ob.show_name = True
    # Link object to scene
    bpy.context.scene.objects.link(ob)
 
    # Create mesh from given verts, edges, faces. Either edges or
    # faces should be [], or you ask for problems
    me.from_pydata(verts, edges, faces)
 
    # Update mesh with new data
    me.update(calc_edges=True)
    return ob

def find_hierarchy():
    noparent= 0
    master = None
    child = None
    hierarchy = []
    hierarchy = list(selected)
    
    #find the one and only master parent of hierarchy
    for selection in selected:
        if selection.parent not in selected:
            noparent = noparent + 1
            master = selection
            #print(selection.name, 'not')
            
    if noparent == 1:
        for selection in selected:
            if selection.parent_index(master) == len(selected)-1:
                child = selection
                #print('child of everything is ',selection.name)
    elif noparent != 1 and child == None:
        hierarchy = None
        #print ('No hierarchy')
            
    if child != None:
        
        for bone in selected:
            index =  child.parent_index(bone)
            
            hierarchy[index] = bone

        hierarchy.reverse()

            
    return hierarchy


def create_hooks(obj):
    for spline in obj.data.splines:
        for point in spline.points:
            point.select = True
            bpy.ops.object.hook_add_newob()
            point.select = False

### main
obj = bpy.context.object
if obj.type == 'ARMATURE' and selected and len(selected) > 1:
    hierarchy = find_hierarchy()   
    if hierarchy != None:
        
        child = hierarchy[-1].name
        verts = []
        edges =[]
        for bone in hierarchy:
            verts.append(bone.head)
        verts.append(hierarchy[-1].tail)
        for i in range(len(verts)-1):
            edges.append((i, i+1))
        spline = createMesh(obj.name + '_spline', obj.location, verts, edges, [])
        
        #list unnecessary bones
        remove_bones = []
        for bone in obj.data.edit_bones:
            if bone not in selected:
                remove_bones.append(bone.name)
                print(bone)
                
        
        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.duplicate()
        bpy.context.active_object.name = obj.name +"_spline_deform"
        spline_armature = bpy.context.active_object
           
        bpy.ops.object.select_all(action='DESELECT')
        spline_armature.select = True
        bpy.ops.object.mode_set(mode='EDIT')
        
                
        for bone in remove_bones:
            spline_armature.data.edit_bones.remove(spline_armature.data.edit_bones[bone])
            
        
        #clear constraint
        for bone in spline_armature.pose.bones:
            #print(bone.name)
            for constraint in bone.constraints:
                bone.constraints.remove(constraint)
                #print(constraint, 'removed')
                 
        
        bpy.ops.object.mode_set(mode='OBJECT')    
        bpy.ops.object.select_all(action='DESELECT')
        
        #convert mesh to spline    
        spline.select = True
        bpy.context.scene.objects.active = spline
        bpy.ops.object.convert(target = 'CURVE')
        
        constraint = spline_armature.pose.bones[child].constraints.new(type='SPLINE_IK')
        constraint.target = spline
        constraint.chain_count = len(spline_armature.data.bones)
        
        bpy.ops.object.mode_set(mode='EDIT') 
        bpy.ops.curve.select_all(action='DESELECT')
        create_hooks(spline)
        bpy.ops.object.mode_set(mode='OBJECT')     
        print()
        #for bone in spline_armature.data.bones:
        #    print(bone.name)

    else:
        print('No proper hierarchy')                    