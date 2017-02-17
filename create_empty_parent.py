import bpy

for obj in bpy.context.selected_objects:
    loc = list(obj.matrix_world.translation)
    rot = list(obj.rotation_euler)
    obj.location = [0, 0, 0]
    obj.rotation_euler = [0, 0, 0]
    bpy.ops.object.empty_add(type='PLAIN_AXES', view_align=False, location=(0,0,0), layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True))
    master = bpy.context.object
    master.name = obj.name + "_parent"
    master.parent = obj.parent
    obj.parent = master
    master.matrix_world.translation = loc
    master.rotation_euler = rot
