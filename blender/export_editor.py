"""Run inside Blender after selecting the scene camera and modeling NT_DUM."""
import bpy
import json
import os
from pathlib import Path

scene = bpy.context.scene
root = bpy.data.objects['NT_DUM']
if not scene.camera:
    raise RuntimeError('Set a calibrated active camera before exporting.')
project = Path(os.environ['VIZ_PROJECT_DIR'])
output = project / 'output' / 'model-data.json'
output.parent.mkdir(parents=True, exist_ok=True)
original = root.matrix_basis.copy()
try:
    root.location = (0, 0, 0)
    root.rotation_euler = (0, 0, 0)
    root.scale = (1, 1, 1)
    bpy.context.view_layer.update()
    graph = bpy.context.evaluated_depsgraph_get()
    vertices = []
    for obj in scene.objects:
        if obj.parent != root or obj.hide_render or obj.type not in {'MESH', 'CURVE'}:
            continue
        evaluated = obj.evaluated_get(graph)
        mesh = evaluated.to_mesh()
        try:
            mesh.calc_loop_triangles()
            normal_matrix = obj.matrix_world.to_3x3().inverted().transposed()
            for tri in mesh.loop_triangles:
                normal = (normal_matrix @ tri.normal).normalized()
                material = mesh.materials[tri.material_index] if len(mesh.materials) > tri.material_index else None
                color = list(material.diffuse_color[:3]) if material else [.5, .5, .5]
                for index in tri.vertices:
                    point = obj.matrix_world @ mesh.vertices[index].co
                    vertices.extend(round(v, 5) for v in [*point, *normal, *color])
        finally:
            evaluated.to_mesh_clear()
    camera = scene.camera
    projection = camera.calc_matrix_camera(graph, x=3600, y=2400, scale_x=1, scale_y=1)
    vp = projection @ camera.matrix_world.inverted()
    data = {
        'vertices': vertices,
        'viewProjection': [vp[r][c] for c in range(4) for r in range(4)],
        'inverseViewProjection': [vp.inverted()[r][c] for c in range(4) for r in range(4)],
        'baseSize': [root.get('width',10), root.get('depth',8)],
        'groundZ': root.get('ground_z',0),
    }
    output.write_text(json.dumps(data, separators=(',', ':')), encoding='utf-8')
    print(f'Exported {len(vertices) // 27} triangles to {output}')
finally:
    root.matrix_basis = original
    bpy.context.view_layer.update()
