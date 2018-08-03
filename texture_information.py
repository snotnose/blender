import bpy
import os

os.system('cls' if os.name == 'nt' else 'clear')

for texture in bpy.data.images:
    flag = False
    for mat in bpy.data.materials:
        if mat.node_tree is not None:
            for node in mat.node_tree.nodes:
                if node.type == 'TEX_IMAGE':
                    if node.image == texture:
                        flag = True
                        path = bpy.data.images[node.image.name].filepath
                        obs = [o.name for o in bpy.data.objects if type(o.data) is bpy.types.Mesh and mat.name in o.data.materials]
                        print('\nThe Material', mat.name,'in the object',obs, 'is using the texture', node.image.name, '\nfrom', path)
                        
                    
    if flag == False:
        print('\nno users found for',texture.name)