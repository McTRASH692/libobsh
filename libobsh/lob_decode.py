#!/usr/bin/env python3
"""
smart_decode.py – Decode a Library coordinate, automatically handling manifests.
Usage: python3 smart_decode.py <coord_file> <output_file>
"""
import sys
import os
import json
sys.path.insert(0, os.path.dirname(__file__))
from libobsh.lob import bytes_at_address, retrieve_file

def is_json(data: bytes) -> bool:
    stripped = data.lstrip()
    return stripped.startswith(b'{') or stripped.startswith(b'[')

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 smart_decode.py <coord_file> <output_file>")
        sys.exit(1)

    coord_file = sys.argv[1]
    output_file = sys.argv[2]

    if not output_file:
        print("Error: output file name is empty")
        sys.exit(1)

    if not os.path.exists(coord_file):
        print(f"Error: coordinate file not found: {coord_file}")
        sys.exit(1)

    with open(coord_file, 'r') as f:
        coord = f.read().strip()

    data = bytes_at_address(coord)

    if is_json(data):
        print("Detected manifest – fetching all pages...")
        manifest_path = output_file + ".tmp_manifest.json"
        with open(manifest_path, 'wb') as mf:
            mf.write(data)
        retrieve_file(manifest_path, output_file)
        os.unlink(manifest_path)
    else:
        with open(output_file, 'wb') as f:
            f.write(data)
        print(f"Recovered {len(data)} bytes to {output_file}")

if __name__ == "__main__":
    main()
