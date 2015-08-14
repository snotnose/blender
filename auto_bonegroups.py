import bpy

ob = bpy.context.object
color = ["THEME02", "THEME04", "THEME11", "THEME12","THEME09", "THEME01","THEME03"]
group_names = {}
group_names["Torso", "THEME02"] = ["torso", "chest", "spine", "hips","shoulder"]
group_names["FK", "THEME12"] = ["fk"]
group_names["IK", "THEME09"] = ["ik"]
group_names["Head", "THEME11"] = ["head", "neck"]
group_names["Finger_tweaks", "THEME02"] = ["01", "02", "03"]
group_names["Finger", "THEME04"] = ["f_", "thumb", "palm"]
group_names["Tweaks", "THEME01"] = ["hose"]

for key, values in group_names.items():
    ob.pose.bone_groups.new(key[0])
    ob.pose.bone_groups[key[0]].color_set = key[1]
    for v in values:
        for bone in ob.pose.bones:
            if bone.name.find(v) != -1 and bone.custom_shape != None:
                bone.bone_group = ob.pose.bone_groups[key[0]]  
 
