#!/usr/bin/env python
import sys

import scheme

fname = sys.argv[1]

with open(fname, "r") as f:
    program = f.read()
    scheme.run(program)
