Library of Babel Tools (libobsh)
================================

[PyPI version] (https://badge.fury.io/py/libobsh) [License: GPL v3] (https://img.shields.io/badge/License-GPLv3-blue.svg)

Proof of Concept
----------------

This tool is primarily for learning and skill improvement. It is functional for small data but has limited practical application due to coordinate size overhead. See "Limitations" below.

Installation
------------

    pip install libobsh

Usage
-----

* Encode a file (any size):
      lob-encode myfile
      Creates myfile.coord

* Decode a coordinate back to a file:
      lob-decode myfile.coord restored

* Run a bash script directly from its coordinate:
      lob-run myfile.coord

How it works
------------

* Files <= 3200 bytes are stored in a single Library page; the .coord contains the page address.
* Larger files are split into 3200‑byte pages; a manifest (JSON) is stored in the Library, and the .coord contains the manifest address.
* The decoder automatically detects whether the coordinate points to a manifest or raw data.

Limitations
-----------

Proof of concept / educational project
  This tool is a personal exploration of the Library of Babel concept and deterministic encoding. It is fully functional for small files (e.g., shell scripts, configuration files, short text) but does not provide storage compression. On the contrary, a Library coordinate is always longer (about 1.55x) than the original data. For a 3200‑byte page, the coordinate is ≈4950 characters.

Practical use
  * Works well for tiny files (a few hundred bytes) where the coordinate length is still manageable.
  * Inefficient for large files (megabytes): the manifest (list of page coordinates) becomes larger than the original file.
  * Not suitable as a general‑purpose archiving or compression tool.

Educational value
  The primary purpose of this project is to learn about:
    - Base‑256 to base‑36 conversion and big‑integer arithmetic.
    - Deterministic addressing and recursion for splitting data.
    - Building a complete Python package from scratch (CLI, packaging, PyPI, documentation).

Use this tool to experiment, learn, or satisfy curiosity – not for production storage of large files.

Requirements
------------

* Python 3.6+ (no external libraries).

License
-------

GNU General Public License v3.0

Credits
-------

This software (libobsh) is inspired by and builds upon the following works:

Conceptual Origin
  Jorge Luis Borges – "The Library of Babel" (1941), a short story describing an infinite library containing every possible book.

Technical Implementation
  Jonathan Basile – Created libraryofbabel.info (2015), the first working implementation of Borges's concept using a deterministic algorithm.

  jrhea – GitHub repository jrhea/library-of-babel, a faithful client-side recreation of the Library of Babel. The core encoding/decoding logic in this project was originally derived from that repository.

Additional References
  The binary encoding approach (base‑256, page size 3200) was developed independently for this project to handle arbitrary binary data and large files.

I am grateful to all these contributors for making this work possible.
