#!/usr/bin/env python3

# Copyright 2022 Hadriel Kaplan
# See LICENSE file for MIT license.

"""Converts an array-based trace file to a object-based one.

Takes a trace file from either stdin or a given filename, and transforms
it from an Array-based JSON to a Object-based one, based on the Google
Trace Format spec.

This allows it to be consumed by more tools.

Example usage:
    ninja -C $BUILDDIR
    ninjatracing $BUILDDIR/.ninja_log | traceclean > trace.json

Or:
    ninja -C $BUILDDIR
    ninjatracing $BUILDDIR/.ninja_log > trace.json
    traceclean intrace.json > outtrace.json   
"""


from __future__ import print_function
import json
import sys


def main(argv):
    if len(argv) > 1:
        print("At most one input file can be given")
        print(__doc__)
        return 1
    if not argv:
        infile = "-"
    else:
        infile = argv[0]

    if any(x in infile for x in ["-h", "--help", "-v", "--version"]):
        print(__doc__)
        return 2

    if infile == "-":
        in_array = json.load(sys.stdin)
    else:
        with open(infile, "r") as file:
            in_array = json.load(file)

    if isinstance(in_array, dict):
        json.dump(in_array, sys.stdout)
        return 0

    if not isinstance(in_array, list):
        raise json.JSONDecodeError("Not an array or map", in_array, 0)

    json.dump({"traceEvents": in_array}, sys.stdout)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
