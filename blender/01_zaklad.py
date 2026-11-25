"""Generic demonstration geometry, unrelated to client plans. Run in Blender."""
import bpy
from mathutils import Vector

WIDTH, DEPTH, WALL_HEIGHT, RIDGE_HEIGHT = 10.0, 8.0, 3.0, 5.0
scene = bpy.data.scenes.new('VIZ_Demo')
bpy.context.window.scene = scene
scene.unit_settings.system = 'METRIC'
root = bpy.data.objects.new('NT_DUM', None)
scene.collection.objects.link(root)
root['width'], root['depth'], root['ground_z'] = WIDTH, DEPTH, 0.0

def material(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    return m

wall = material('Demo_wall', (.7, .7, .7))
roof = material('Demo_roof', (.08, .09, .1))
# Extruded pentagonal house profile. Outward normals are recalculated later.
profile = [(-DEPTH/2, 0), (DEPTH/2, 0), (DEPTH/2, WALL_HEIGHT), (0, RIDGE_HEIGHT), (-DEPTH/2, WALL_HEIGHT)]
verts = [(x,y,z) for x in (-WIDTH/2,WIDTH/2) for y,z in profile]
faces = [(4,3,2,1,0),(5,6,7,8,9)] + [(i,(i+1)%5,(i+1)%5+5,i+5) for i in range(5)]
mesh = bpy.data.meshes.new('Demo_house')
mesh.from_pydata(verts, [], faces)
mesh.materials.append(wall)
mesh.materials.append(roof)
obj = bpy.data.objects.new('Demo_house', mesh)
scene.collection.objects.link(obj)
obj.parent = root
for poly in mesh.polygons:
    if poly.index in (4,5):
        poly.material_index = 1
camera_data = bpy.data.cameras.new('Demo_camera')
camera = bpy.data.objects.new('Demo_camera', camera_data)
scene.collection.objects.link(camera)
camera.location = (18,-24,15)
camera.rotation_euler = (Vector((0,0,2))-camera.location).to_track_quat('-Z','Y').to_euler()
scene.camera = camera
camera_data.lens = 40
sun_data = bpy.data.lights.new('Demo_sun', 'SUN')
sun_data.energy = 2
sun = bpy.data.objects.new('Demo_sun', sun_data)
scene.collection.objects.link(sun)
sun.rotation_euler = (.4,-.5,-.3)
scene.render.resolution_x, scene.render.resolution_y = 3600,2400
print('Created generic 10 x 8 m demonstration house; calibrate camera to your own photo.')
