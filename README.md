# tracetools
Utility programs to manipulate Chrome-style trace files, such as those output by [ninjatracing](https://github.com/nico/ninjatracing).

All the scripts in here are composable by piping them together, in any order.

For example:
```bash
ninjatracing -a build/.ninja_log | tracefilter '\b(Staging|thirdparty)\b' | trace2object > trace.json
```

Another example:
```bash
cat infile.json \
    | tracefilter '\b(Staging|thirdparty)\b' \
    | tracename 'Building' \
    | tracedup --to_pid=1 '\.[ao]\b' \
    | tracename --pid=1 'Compiling' \
    > trace.json
```

## tracefilter

Takes a trace file and filters out entries based on matching a given regex pattern for a given field.

Usage: `tracefilter [--field=<field>] <pattern> [<filepath>]`

Uses `stdin` by default, unless a `filepath` is given. The default field is "`name`", but can
be changed with the `--field=<field>` option.

By default, the given pattern is applied to the 'name' field of each Array
entry, or of the Array in the "`traceEvents`" and "`samples`" key fields if it's
an Object-based JSON format. The input file/stdin can be Array or Object-based JSON.

Further details are available with `tracefilter -h`.


## tracedup

Takes a trace file and duplicates entries based on matching a given regex pattern for a given field,
assigning them new PID numbers. This is useful to display separate graph sections of specific parts,
since most visual tools separate time-lines by PID.

Usage: `tracedup [--from-pid=<pid>] [--to-pid=<pid>] [--field=<field>] <pattern> [<filepath>]`

Uses `stdin` by default, unless a `filepath` is given.

The default field is "`name`", but can be changed with the `--field=<field>` option.

The `--from-pid` specifies what current PID to copy from, while the `--to-pid`
specifies the PID number to assign to the copied entry. By default the `--from-pid`
is `0`, and the `--to-pid` is one more than the highest one in the file.

By default, the given pattern is applied to the 'name' field of each Array
entry, or of the Array in the "`traceEvents`" and "`samples`" key fields if it's
an Object-based JSON format. The input file/stdin can be Array or Object-based JSON.

Further details are available with `tracedup -h`.


## tracename

Reads in a trace file or stdin, and adds a metadata entry to assign a display name
for the given PID or TID.

Usage: `tracename [ --pid=<pid> [--tid=<tid>]] <name> [<filepath>]`

Uses `stdin` by default, unless a `filepath` is given.

If no `--pid` is given, defaults naming PID 0.

If `--pid` is given, assigns the name to that PID.
If `--tid` is given, assigns the name to that TID, for the given PID.

Further details are available with `tracename -h`.


## trace2object

Takes a JSON Array-based trace file and converts it to an Object-based one, with the
entries moved into a "`traceEvents`" object key field. This allows one to add more
metadata to the trace file.

Usage: `trace2object [<filepath>]`

Uses `stdin` by default, unless a `filepath` is given. If the input JSON is already
Object-based, it is passed through unchanged.


## Background

Trace files come in many formats. The tools in here are meant for the JSON trace file
format [specified by Google](https://docs.google.com/document/d/1CvAClvFfyA5R-PhYUmn5OOQtYMH4h6I0nSsKchNAySU/preview).

Such files can be viewed in:
* [Perfetto](https://ui.perfetto.dev/)
* [Chrome tracing](chrome://tracing/) - open Chrome and put `about:tracing` in the address box.
* [Speedscope](https://www.speedscope.app)

...and others.
