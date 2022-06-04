#!/usr/bin/env python3

# Copyright 2022 Hadriel Kaplan
# See LICENSE file for MIT license.

"""tracefilter ( <filepath> | - ) [--field=<field>] <pattern>

Filters a trace file.

Takes a trace file from either stdin or a given `path/to/file`, and filters out
entries based on the given regex pattern.

The trace file format can be either Array or Object-based JSON.

By default, the given pattern is applied to the 'name' field of each Array
entry, or of the Array in the 'traceEvents' and 'samples' Object fields if it's
an Object-based JSON format.

To choose a different field, use the `--field=<field>` option.

If the chosen field's type is not a string, it will be converted to a string
before applying the regex pattern.

To apply different patterns to different fields, simply pipe multiple
tracefilter commands together.

The regex pattern uses Python's engine, so you can have a case-insensitive
match by preceeding the pattern with '(?i)', for example. Also, this script
uses `re.search()`, so the pattern can match anywhere in the input string;
use anchors to constrain it.

Example usage:
    cat intrace.json | tracefilter - "\\bStaging|thirdparty\\b" > outtrace.json
Or for stdin:
    tracefilter intrace.json "\\bStaging|thirdparty\\b" > outtrace.json   

Example filtering out entries of shorter duration than 100,000 microseconds:
    tracefilter intrace.json --field=dur "^[0-9]{1,5}$" > outtrace.json
"""


from __future__ import print_function
import json
import optparse
import re
import sys


def filter_entries(entries, field, pattern):
    filter_re = re.compile(pattern)
    output = []
    for entry in entries:
        if field in entry and filter_re.search(str(entry[field])):
            continue
        output.append(entry)
    return output


def filter_json(trace, field, pattern):
    if isinstance(trace, list):
        return filter_entries(trace, field, pattern)
    if isinstance(trace, dict):
        for key in ["traceEvents", "samples"]:
            if key in trace:
                trace[key] = filter_entries(trace[key], field, pattern)
    return trace


def main(argv):
    # optparse can't handle a single dash
    argv = ["--stdin" if x == "-" else x for x in argv]

    parser = optparse.OptionParser(__doc__)
    parser.add_option(
        "--field",
        dest="field",
        default="name",
        help="Specify a JSON field to filter on (default: %default)",
    )
    parser.add_option(
        "--stdin",
        dest="use_stdin",
        action="store_true",
        help="Use stdin for input (can just be a '-' instead)",
    )
    (options, args) = parser.parse_args(argv)

    if options.use_stdin:
        trace = json.load(sys.stdin)
    elif len(args) != 2:
        parser.print_help()
        print("\nERROR: no input file given, or no pattern, or too many arguments\n")
        return 1
    else:
        with open(args[0], "r") as file:
            trace = json.load(file)

    json.dump(filter_json(trace, options.field, args[1]), sys.stdout)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
