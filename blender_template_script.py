"""
This script is a Python template for Blender, designed to create an operator, a panel, and a modal timer. 
It enables arguments to be passed from the panel to the operator using a dictionary. 
A global class named Registry is utilized to pass information between each module.
"""
import bpy
import pickle
import os
from bpy.types import Menu
import random
import time
import copy
import ast
import math

#exec(open(r"BL - Template Script.py").read())


def delete(deletion_object):
    deletion_object.hide_set(False) # Πρεπει να γινει visible για να διαγραφτει
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[deletion_object.name].select_set(True, view_layer=bpy.context.scene.view_layers[0])
    bpy.ops.object.delete(use_global=True, confirm=False)
    
def delete_all():
    for bld_obj in bpy.data.objects:
        bld_obj.hide_set(False) # Πρεπει να γινει visible για να διαγραφτει
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[bld_obj.name].select_set(True, view_layer=bpy.context.scene.view_layers[0])
        bpy.ops.object.delete(use_global=True, confirm=False)    

def delete_property(bld_obj,property):
    select_active(bld_obj)
    if (property in bld_obj):
        bpy.ops.wm.properties_remove(data_path="object", property_name=str(property))
    
def delete_properties(bld_obj,properties):
    for property in properties:
        delete_property(bld_obj,property)
 
def select_active(bld_obj):
    bpy.ops.object.select_all(action='DESELECT')
    bld_obj.select_set(True)
    bpy.context.view_layer.objects.active = bld_obj
    
def select_list(list_bld_objs):
    bpy.ops.object.select_all(action='DESELECT')
    for bld_obj in list_bld_objs:
        bld_obj.select_set(True)
    

def copytrans_contraint(wirecad_bld,stl_bld):
    new_constraint = stl_bld.constraints.new('COPY_TRANSFORMS')
    new_constraint.target = wirecad_bld
    new_constraint.target_space = "WORLD"
    new_constraint.use_scale = False
       
    return new_constraint

def child_contraint(parent_object,child_object):
    new_constraint = child_object.constraints.new('CHILD_OF')
    name = "cons_" + parent_object.name + "_" + child_object.name
    new_constraint.name = name
    new_constraint.target = parent_object
    new_constraint.use_scale_x = False
    new_constraint.use_scale_y = False
    new_constraint.use_scale_z = False
    
    select_active(child_object)
    bpy.ops.constraint.childof_clear_inverse(constraint = new_constraint.name)
    
    return new_constraint
   

def bldobj_get_object_collections(bld_obj,collection = None):
    
    if (collection is None):
        root_coll = bpy.context.scene.collection
    else:
        root_coll = collection
    all_collections = root_coll.children
    obj_collections = []
    for coll in all_collections:
        # Check if the object is in this collection
        if (bld_obj.name in coll.objects):
            # If the object is in the collection, add it to our list
            obj_collections.append(coll)
        
        obj_collections.extend(bldobj_get_object_collections(bld_obj,coll))    

    return obj_collections
    
def bldobj_link_object_collections(bld_obj,collections):
    for coll in collections:
        if not(bld_obj.name in coll.objects):
            coll.objects.link(bld_obj)

def bldobj_append_list(bld_obj,list_name,new_list):
    old_list = [x for x in bld_obj[list_name]]
    new_list = old_list + new_list
    bld_obj[list_name] = new_list
  
def unlink_object_from_all_collections(bld_obj):
    if (bld_obj in [x for x in bpy.context.scene.collection.objects]):                  
        bpy.context.scene.collection.objects.unlink(bld_obj)
    for collection in bpy.data.collections:
        if (bld_obj.name in collection.objects):
            collection.objects.unlink(bld_obj)
            
            


class Operator_Custom(bpy.types.Operator):
    bl_idname = "custom.operator"
    bl_label = "Operator"

    args: bpy.props.StringProperty()
    
    def execute(self, context):
        global registry

        try:
            args = ast.literal_eval(self.args)
        except ValueError:
            raise ValueError(f"Invalid format for Panel Arguments")

        self.report({'INFO'}, f'Args:{args}')
        
        action = args['action']
        
        if (action == 'some_action'):
            val = args['value']
            
        return {'FINISHED'}
        
        
    
class ModalTimer_Custom(bpy.types.Operator):
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"

    _timer = None

    def modal(self, context, event):
        global registry
        if event.type == 'TIMER':
            pass

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.01, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        
    
class Panel_Custom(bpy.types.Panel):
    bl_label = "Panel_Custom"
    bl_idname = "Panel_Custom"
    bl_category = "Panel_Custom"
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"

    def draw(self, context):
        global registry
           
        layout = self.layout
        box = layout.box()               
        row = box.row()
        row.operator("custom.operator", text = "INSERT_TEXT",icon='CHECKBOX_DEHLT').args = str({'action':'actionda','value':'dasf'})
        # # row.prop(bpy.context.scene,"custom_propery",text = "")
    


classes = (Operator_Custom,ModalTimer_Custom,Panel_Custom)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)            

class Registry():
    
    def __init__(self):
        pass



if __name__ == "__main__":
    print("Hello Template")


    # delete_all()

    registry = Registry()
   
    bpy.types.Scene.custom_propery = bpy.props.StringProperty(name = "custom_propery",default = "")
    bpy.context.scene.custom_propery = "SOLID"


    register()
    bpy.ops.wm.modal_timer_operator()
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
