#Collapsing all shapekeys with Left and Right Vgroups for exporting clean shapekeys to fbx

import bpy

obj = bpy.context.object
shapekeynames =[]
keyblocks = obj.data.shape_keys.key_blocks

for shapekey in keyblocks:
	shapekey.value = 0
	shapekeynames.append(shapekey.name)    

print(shapekeynames)


for name in shapekeynames:
	shapekey = keyblocks[name]
	if shapekey.vertex_group is not '':
		shapekey.value = 1
		bpy.ops.object.shape_key_add(from_mix=True)
		print (obj.active_shape_key)
		new_shapekey = obj.active_shape_key
		for i in range(0,len(keyblocks)):
			if keyblocks[i].name == name:
				obj.active_shape_key_index = i
		bpy.ops.object.shape_key_remove(all=False)
		new_shapekey.name = name
		


	
bpy.context.scene.update() 