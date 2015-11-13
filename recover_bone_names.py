import bpy
layer_number = 0


def find_layer(layers):
    for n, layer in enumerate(layers):
        if layer == True:
            return n
        
def test_vector(value, value_recover):
    flag = True
    for i in range(len(value)):
        if float("%.5f" % value[i]) != float("%.5f" % value_recover[i]):
           flag = False
        #print("%.3f" % value[i], "%.3f" % value_recover[i], len(value))
    return flag

def test_constraint(constraint, constraint_recover):
    flag = True
    if len(constraint) == len(constraint_recover) and len(constraint) != 0:
        for i in range(len(constraint)):
            if constraint[i].name != constraint_recover[i].name:
                flag = False  
    else:
        flag = False
    return flag

#test_vector(bpy.data.armatures['rig_recover'].bones['f_index.01.R.001'].tail_local, bpy.data.armatures['rig_recover'].bones['f_index.01.R'].tail_local)

for bone in bpy.data.armatures['rig'].bones:
    for bone_recover in bpy.data.armatures['rig_recover'].bones:
        if find_layer(bone.layers) == find_layer(bone_recover.layers) and test_vector(bone.head_local, bone_recover.head_local) and test_vector(bone.tail_local, bone_recover.tail_local) and test_constraint(bpy.data.objects['rig'].pose.bones[bone.name].constraints, bpy.data.objects['rig_recover'].pose.bones[bone_recover.name].constraints):
            
  
            bone_recover.name = bone.name
            
            
            
      
            
            