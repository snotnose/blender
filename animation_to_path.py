bl_info = {
    "name": "Animation to Path",
    "author": "Bassam Kurdal, Tal Hershkovich",
    "version": (0, 1),
    "blender": (2, 90, 0),
    "location": "View3D > Animation > Animation to Path",
    "description": "Turn animations into spline paths",
    "warning": "",
    "wiki_url": "",
    "category": "Object"}

import bpy
from mathutils import Vector


def create_curve(ob):
    name = ob.name
    foo = bpy.data.curves.new(name="motion_{}".format(name),type='CURVE')
    bar = bpy.data.objects.new(name="motion_{}".format(name), object_data=foo)
    
    #add to all the same collections like the original object
    for col in ob.users_collection:
        col.objects.link(bar)
    foo.splines.new(type='POLY')
    foo.dimensions = '3D'
    return bar


class AnimToPath(bpy.types.Operator):
    ''' Transform Animation into curve paths'''
    bl_idname = "object.animation_to_path"
    bl_label = "Convert animation into spline path"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        act = context.active_object
        return context.mode == 'OBJECT' and\
         act and act.animation_data and act.animation_data.action

    def execute(self, context):
        allcurves = context.active_object.animation_data.action.fcurves
        fcurves = sorted(
            [curve for curve in allcurves if curve.data_path == 'location'],
            key=lambda curve: curve.array_index)
        if fcurves:
            cu = create_curve(context.active_object)   
            for frame in range(context.scene.frame_start, context.scene.frame_end):
                if frame != context.scene.frame_start:
                    cu.data.splines[0].points.add(count=1)
                cu.data.splines[0].points[-1].co = Vector((
                    fcurves[0].evaluate(frame),
                    fcurves[1].evaluate(frame),
                    fcurves[2].evaluate(frame),0))

        return {'FINISHED'}
    
class AnimToPath_Panel(bpy.types.Panel):
    bl_label = "Animation to Path"
    bl_idname = "OBJECT_PT_AnimToPath"
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "Animation"

    @classmethod
    def poll(cls, context):
         return bpy.context.object

    def draw(self, context):
        layout = self.layout
                        
        layout.operator('object.animation_to_path', text="Convert Animation to Path", icon = 'CURVE_DATA')

def register():
    bpy.utils.register_class(AnimToPath)
    bpy.utils.register_class(AnimToPath_Panel)

def unregister():
    bpy.utils.unregister_class(AnimToPath)
    bpy.utils.unregister_class(AnimToPath_Panel)

if __name__ == "__main__":
    register()    