#!/usr/bin/env python3
"""
smart_encode.py – Encode any file to a single Library coordinate.
For large files, stores manifest in Library and outputs manifest coordinate.
Usage: python3 smart_encode.py <filename>
"""
import sys
import os
import json
sys.path.insert(0, os.path.dirname(__file__))
from libobsh.lob import address_of_bytes, store_file, store_binary

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 smart_encode.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, 'rb') as f:
        data = f.read()

    if len(data) <= 3200:
        coord = address_of_bytes(data)
        print(f"Single page: {len(data)} bytes")
    else:
        print(f"Large file: {len(data)} bytes, splitting into pages...")
        # Store file pages and get manifest list (local file)
        manifest_path = filename + '.manifest.json'
        store_file(filename, manifest_path)   # creates local manifest
        # Now store the manifest itself in the Library
        with open(manifest_path, 'rb') as mf:
            manifest_data = mf.read()
        coord = address_of_bytes(manifest_data)
        # Optionally remove the local manifest (or keep for debugging)
        # os.unlink(manifest_path)
        print(f"Manifest stored, coordinate points to {len(manifest_data)} bytes of JSON")

    # Save coordinate to .coord file
    coord_file = filename + '.coord'
    with open(coord_file, 'w') as cf:
        cf.write(coord)
    print(f"Coordinate saved to {coord_file}")
    print(f"First 60 chars: {coord[:60]}...")

if __name__ == "__main__":
    main()
