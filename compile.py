""" Compiles html into a single file.

Usage:
    python compile.py index.html index.compiled.html
"""

import base64
import functools
import mimetypes
import pathlib
import re
import sys

IMAGE_PATTERN = re.compile(r'<img src="(.+?)"')

def replace(source_path, match):
    path = match.group(1)
    path = pathlib.Path(source_path).parent / path
    typ, _ = mimetypes.guess_type(path)
    with open(path, 'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return f'<img src="data:{typ};base64,{encoded}"'

def main():
    if len(sys.argv) != 3:
        sys.exit('Usage: python compile.py index.html index.compiled.html')
    input_path, output_path = sys.argv[1:]
    with open(input_path, 'r') as f:
        content = f.read()
    compiled = IMAGE_PATTERN.sub(functools.partial(replace, input_path), content)
    with open(output_path, 'w') as f:
        f.write(compiled)

if __name__ == '__main__':
    main()
