import bpy
import random

objects = bpy.data.objects
occupied_index = {'none':0}
for obj in objects:
    if obj.pass_index != 0:
        occupied_index[obj] = obj.pass_index
    
#print(occupied_index)

accepted_objects = []
for obj in objects:
    if (obj.type == 'MESH' or obj.type == 'EMPTY') and obj not in occupied_index.keys():
        accepted_objects.append(obj)
        
index_list = list(range(len(accepted_objects) + len(set(occupied_index.values()))))
accepted_index = list(set(index_list) - set(occupied_index.values()))
        
#print(len(accepted_index))
#print(len(accepted_objects))

for obj in accepted_objects:
    val = random.choice(accepted_index)
    obj.pass_index = val
    accepted_index.remove(val)
    

