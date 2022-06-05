# tracetools
Utility programs to manipulate Chrome trace files, and in particular those output by
[ninjatracing](https://github.com/nico/ninjatracing) for the purpose of build-tool analysis.

* [tracefilter](#tracefilter): filter out portions of the trace using regex.
* [tracedup](#tracedup): duplicate portions of the trace into separate PIDs.
* [tracename](#tracename): name PIDs and TIDs in the trace.
* [trace2html](#trace2html): create a stand-alone HTML file of the trace with Chrome-tracing UI.
* [trace2object](#trace2object): convert trace JSON Array format to Object format.

All the scripts in here are composable by piping them together, in any order. (except `trace2html`, which generates HTML so it has to be last if used)

For example:
```bash
ninjatracing -a build/.ninja_log | tracefilter '\b(Staging|thirdparty)\b' > trace.json
```

Another example, this one creating a process-id of 1 for compiling and 2 for linking, and
resulting in a stand-alone HTML file with Google's Chrome-tracing UI and the trace embedded:
```bash
cat infile.json \
    | tracefilter '\b(?:Staging|thirdparty)\b' \
    | tracename 'Building' \
    | tracedup --to_pid=1 '\.(?:[aoc]|cc|cpp|cxx)\b' \
    | tracename --pid=1 'Compiling' \
    | tracedup --to_pid=2 --invert '\.(?:[aoc]|cc|cpp|cxx)\b' \
    | tracename --pid=2 'Linking' \
    | trace2html --title='Build times for gcc' \
    > trace.html
```


## tracefilter

Takes a trace file and filters out entries based on matching a given regex pattern for a given field.

Usage: `tracefilter [--field=<field>] [--invert] <pattern> [<filepath>]`

Uses `stdin` by default, unless a `filepath` is given. The default field is "`name`", but can
be changed with the `--field=<field>` option.

By default, the given pattern is applied to the "`name`" field of each Array
entry, or of the Array in the "`traceEvents`" and "`samples`" key fields if it's
an Object-based JSON format. The input file/stdin can be Array or Object-based JSON.

The `--invert` option filters those that do NOT match the pattern, however entries without
the given field at all will not be filtered.

Further details are available with `tracefilter -h`.


## tracedup

Takes a trace file and duplicates entries based on matching a given regex pattern for a given field,
assigning them new PID numbers. This is useful to display separate graph sections of specific parts,
since most visual tools separate time-lines by PID.

Usage: `tracedup [--from-pid=<pid>] [--to-pid=<pid>] [--field=<field>] [--invert] <pattern> [<filepath>]`

Uses `stdin` by default, unless a `filepath` is given.

The default field is "`name`", but can be changed with the `--field=<field>` option.

The `--from-pid` specifies what current PID to copy from, while the `--to-pid`
specifies the PID number to assign to the copied entry. By default the `--from-pid`
is `0`, and the `--to-pid` is one more than the highest one in the file.

By default, the given pattern is applied to the 'name' field of each Array
entry, or of the Array in the "`traceEvents`" and "`samples`" key fields if it's
an Object-based JSON format. The input file/stdin can be Array or Object-based JSON.

The `--invert` option duplicates those that do NOT match the pattern.

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


## trace2html

Reads in a trace file or stdin, and generates a stand-alone HTML file with
Google Chrome's tracing UI embedded in it, as well as the trace file.

This can be opened and used in any browser.

Usage: `trace2html [--title=<title>] [<filepath>] [--outfile=<outfile>]`

The `--title` option sets the title of the HTML page, which helps keep different
traces separate. If `--title` is not given, one will be created for you which
includes the current data and time.

The `--outfile` option sets a file to write out to, which might be useful for
scripting or to save some performance by avoiding copying the huge output
through stdout.


## trace2object

Takes a JSON Array-based trace file and converts it to an Object-based one, with the
entries moved into a "`traceEvents`" object key field. This allows one to add more
metadata to the trace file.

Usage: `trace2object [<filepath>]`

Uses `stdin` by default, unless a `filepath` is given. If the input JSON is already
Object-based, it is passed through unchanged.

Note: some viewing tools cannot handle the Object-based format.

## Background

Trace files come in many formats. The tools in here are meant for the JSON trace file
format [specified by Google](https://docs.google.com/document/d/1CvAClvFfyA5R-PhYUmn5OOQtYMH4h6I0nSsKchNAySU/preview).

Example programs such files can be viewed in:
* [Perfetto](https://ui.perfetto.dev/): an excellent viewer with many features, made by Google and the successor to Chrome's `about:tracing`. Works in any browser.
* [Chrome tracing](https://www.chromium.org/developers/how-tos/trace-event-profiling-tool/): open Chrome and put `about:tracing` in the address box.
* [Speedscope](https://www.speedscope.app): not as useful as some others for duration events, but the "Left order" view is unique, and for process performance stack trace views the "Sandwhich" view is quite useful.
