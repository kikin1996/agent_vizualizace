#!/usr/bin/env python3
"""Build one self-contained, offline placement editor from user-owned assets."""
import argparse
import base64
import json
from pathlib import Path


def build(photo, model, output, template):
    data = json.loads(model.read_text(encoding='utf-8'))
    for key in ('vertices', 'viewProjection', 'inverseViewProjection'):
        if key not in data:
            raise ValueError(f'Missing model field: {key}')
    if len(data['vertices']) % 27:
        raise ValueError('Expected triangles with position, normal and RGB color.')
    for key in ('viewProjection', 'inverseViewProjection'):
        if len(data[key]) != 16:
            raise ValueError(f'{key} must have 16 column-major elements.')
    suffix = photo.suffix.lower()
    mime = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png'}.get(suffix)
    if not mime:
        raise ValueError('Use a JPEG or PNG photograph.')
    if output.exists():
        raise FileExistsError(f'Refusing to overwrite {output}')
    source = template.read_text(encoding='utf-8')
    embedded = json.dumps(data, separators=(',', ':'), allow_nan=False).replace('<', '\\u003c')
    source = source.replace('__PHOTO__', f'data:{mime};base64,' + base64.b64encode(photo.read_bytes()).decode('ascii'))
    source = source.replace('__MODEL__', embedded)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(source, encoding='utf-8')
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--photo', type=Path, required=True)
    parser.add_argument('--model', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    template = Path(__file__).resolve().parents[1] / 'web/editor-template.html'
    print(build(args.photo, args.model, args.output, template))
