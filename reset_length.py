import bpy

obj = bpy.context.object    
if obj.type == 'ARMATURE':
       for bone in obj.pose.bones:
           for con in bone.constraints:
               if con.type == 'STRETCH_TO':           
                   con.rest_length = 0
             