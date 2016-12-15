'''assign automatically colorered bone groups'''

import bpy

ob = bpy.context.object
color = ["THEME02", "THEME04", "THEME11", "THEME12","THEME09", "THEME01","THEME03"]
group_names = {}
group_names["Main", "THEME09"] = ["torso", "chest", "hips","shoulder","head", "neck", "eye", "jaw","master"]
group_names["FK", "THEME04"] = ["fk"]
group_names["IK", "THEME01"] = ["ik"]
group_names["Face", "THEME02"] = ["cheek", "nose", "lip","chin","brow","lid","ear"]
group_names["Finger", "THEME06"] = ["f_", "thumb", "palm"]
group_names["Tweaks", "THEME07"] = ["tweak"]

for key, values in group_names.items():
    ob.pose.bone_groups.new(key[0])
    ob.pose.bone_groups[key[0]].color_set = key[1]
    for v in values:
        for bone in ob.pose.bones:
            if bone.name.find(v) != -1 and bone.custom_shape != None:
                bone.bone_group = ob.pose.bone_groups[key[0]]  
 
