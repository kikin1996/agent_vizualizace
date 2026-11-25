"""Recalculate outward normals on this generated house's meshes and cutters."""
import bpy
import bmesh
root = bpy.data.objects['NT_DUM']
for obj in bpy.context.scene.objects:
    if obj.parent != root or obj.type != 'MESH':
        continue
    mesh = bmesh.new()
    try:
        mesh.from_mesh(obj.data)
        bmesh.ops.recalc_face_normals(mesh, faces=list(mesh.faces))
        mesh.to_mesh(obj.data)
    finally:
        mesh.free()
print('House and cutter normals recalculated; verify openings in a render.')
