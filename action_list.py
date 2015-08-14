import bpy

def action_updated(context):
    ob = bpy.context.object
    action_index = bpy.data.actions.find(ob.animation_data.action.name)
    if action_index != ob.action_list_index:
        print("action changed")
        ob.action_list_index = action_index
                
#select the new action when there is a new selection in the ui list and go to the first frame
def update_action_list(self, context):
    ob = bpy.context.object
    ob.animation_data.action = bpy.data.actions[ob.action_list_index]
    bpy.context.scene.frame_current = 1

class ACTION_UI_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(item, "name", text="", emboss=False, icon_value=icon)
        elif self.layout_type in {'GRID'}:
            pass

class UIListActionPanel(bpy.types.Panel):
    """Creates a Panel in the 3D View properties window"""
    bl_label = "Action List"
    bl_idname = "OBJECT_PT_ui_list"
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        ob = context.object    
        layout.template_list("ACTION_UL_list", "", bpy.data, "actions", ob, "action_list_index")

bpy.app.handlers.scene_update_post.append(action_updated)             
#bpy.app.handlers.scene_update_pre.append(action_updated) 

def register():
    bpy.types.Object.action_list_index = bpy.props.IntProperty(update=update_action_list)
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Object.action_list_index

if __name__ == "__main__":
    register()