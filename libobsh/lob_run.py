#!/usr/bin/env python3
"""
lob-run – Execute a script from its .coord file.
"""
import sys, os, subprocess, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from libobsh.lob import bytes_at_address

if len(sys.argv) != 2:
    print("Usage: lob-run <script.coord>", file=sys.stderr)
    sys.exit(1)
coord_file = sys.argv[1]
if not os.path.exists(coord_file):
    print(f"Error: {coord_file} not found", file=sys.stderr)
    sys.exit(1)
with open(coord_file) as f:
    coord = f.read().strip()
data = bytes_at_address(coord)
fd, tmp = tempfile.mkstemp(dir='.', prefix='.lob_', suffix='.sh')
os.write(fd, data)
os.close(fd)
os.chmod(tmp, 0o755)
try:
    subprocess.run([tmp], check=True)
finally:
    os.unlink(tmp)
