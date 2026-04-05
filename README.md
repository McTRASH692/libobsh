Library of Babel Tools (lob)
============================
[![PyPI version](https://badge.fury.io/py/libobsh.svg)](https://pypi.org/project/libobsh/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Encode any file to a deterministic Library of Babel coordinate, and decode/run it.

Installation
------------

    git clone https://github.com/yourusername/libobsh.git
    cd libobsh
    ./setup.sh
    export PATH="$HOME/.local/bin:$PATH"

Usage
-----

* Encode a file (any size):
      lob-encode myfile
      Creates myfile.coord.

* Decode a coordinate back to a file:
      lob-decode myfile.coord restored

* Run a bash script directly from its coordinate:
      lob-run myfile.coord

How it works
------------

* Files <= 3200 bytes: stored in a single Library page; .coord contains the page address.
* Larger files: split into 3200-byte pages; a manifest (JSON) is stored in the Library, and the .coord contains the manifest address.
* The decoder automatically detects whether the coordinate points to a manifest or raw data.

Requirements
------------

* Python 3.6+ (no external libraries).

License
-------

GNU GPLv3

Credits
-------

This software is based on the concept of the "Library of Babel" by Jorge Luis Borges and the technical implementation by Jonathan Basile (libraryofbabel.info). It also uses algorithmic ideas from the open‑source repository jrhea/library-of-babel. See CREDITS.md for details.
