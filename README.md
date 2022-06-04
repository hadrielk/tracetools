# tracetools
Utility programs to manipulate trace files, such as those output by [ninjatracing](https://github.com/nico/ninjatracing).

All the scripts in here are composable by piping them together, in any order.

For example:
```bash
ninjatracing -a build/.ninja_log | tracefilter - '\bStaging|thirdparty\b' | trace2object > trace.json
```


### tracefilter

Takes a trace file and filters out entries based on matching a given regex pattern for a given field.

Usage: `tracefilter ( <filepath> | - ) [--field=<field>] <pattern>`

Use `-` instead of a `path/to/file` to use `stdin`. The default field is "`name`", but can
be changed with the `--field=<field>` option.

By default, the given pattern is applied to the 'name' field of each Array
entry, or of the Array in the "`traceEvents`" and "`samples`" key fields if it's
an Object-based JSON format. The input file/stdin can be Array or Object-based JSON.

Further details are available with `tracefilter -h`.


### trace2object

Takes a JSON Array-based trace file and converts it to an Object-based one, with the
entries moved into a "`traceEvents`" object key field. This allows one to add more
metadata to the trace file.

Usage: `trace2object [<filepath>]`

Uses `stdin` by default, unless a `path/to/file` is given. If the input JSON is already
Object-based, it is passed through unchanged.


## Background

Trace files come in many formats. The tools in here are meant for the JSON [trace file
format specified by Google](https://docs.google.com/document/d/1CvAClvFfyA5R-PhYUmn5OOQtYMH4h6I0nSsKchNAySU/preview).

Such files can be viewed in:
* [Perfetto](https://ui.perfetto.dev/)
* [Chrome tracing](chrome://tracing/) - open Chrome and put `about:tracing` in the address box.
* [Speedscope](https://www.speedscope.app)

...and others.
