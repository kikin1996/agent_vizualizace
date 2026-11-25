"""Generic example facade panels; not measured client construction geometry."""
import bpy
root = bpy.data.objects['NT_DUM']
width, depth = root['width'], root['depth']
material = bpy.data.materials.new('Demo_glazing')
material.diffuse_color = (.12,.2,.25,1)
for name,x,z,w,h in [('left',-width*.25,1.6,1.4,1.2),('right',width*.25,1.6,1.4,1.2),('door',0,1.05,.9,2.1)]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x,-depth/2-.03,z))
    obj=bpy.context.object
    obj.name='Demo_'+name
    obj.dimensions=(w,.06,h)
    obj.parent=root
    obj.data.materials.append(material)
print('Added generic facade markers. Replace with detailed openings for production.')
