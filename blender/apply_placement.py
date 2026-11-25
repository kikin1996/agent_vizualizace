"""Apply exported editor placement; VIZ_PLACEMENT_FILE points to the JSON."""
import bpy
import json
import math
import os
from pathlib import Path

state = json.loads(Path(os.environ['VIZ_PLACEMENT_FILE']).read_text(encoding='utf-8'))
values = {k: state.get(k, 0) for k in ('x', 'y', 'rotation', 'rotationX', 'rotationY')}
values['scale'] = state.get('scale', 1)
if not all(isinstance(v, (int, float)) and math.isfinite(v) for v in values.values()):
    raise ValueError('Placement values must be finite numbers.')
if not .6 <= values['scale'] <= 1.8 or any(abs(values[k]) > 180 for k in ('rotation', 'rotationX', 'rotationY')):
    raise ValueError('Placement exceeds the editor limits.')
root = bpy.data.objects['NT_DUM']
root.rotation_mode = 'XYZ'
root.rotation_euler = tuple(math.radians(values[k]) for k in ('rotationX', 'rotationY', 'rotation'))
k = values['scale']
root.scale = (k, k, k)
root.location = (values['x'], values['y'], -root.get('ground_z',0) * (k - 1))
bpy.context.view_layer.update()
print('Placement applied; save the scene to a new file when ready.')
