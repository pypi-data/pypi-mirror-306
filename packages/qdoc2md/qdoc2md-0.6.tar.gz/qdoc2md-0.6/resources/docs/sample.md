
# Sample

A sample q script annotated with documentation comments.


## .sample.isdir

Check if a path is an existing directory.

**Parameters**

`path`: *hsym*

:   A file system path.

**Return**

*boolean*

:   `1b` if `path` is an existing directory; `0b` otherwise.

**Signals**

`TypeError`

:   If `path` is not an hsym.

**Example**

```q
q).sample.isdir `:src
1b
q).sample.isdir `src
'TypeError: not an hsym
```

**See Also**

[.sample.isfile](#sampleisfile)

:   For file check.

## .sample.isfile

Check if a path is an existing file.

**Parameters**

`path`: *hsym*

:   A file system path.

**Return**

*boolean*

:   `1b` if `path` is an existing file; `0b` otherwise.

**Signals**

`TypeError`

:   If `path` is not an hsym.

**Example**

```q
q).sample.isfile `:tests/resources/sample.q
1b
q).sample.isfile "tests/resources/sample.q"
'TypeError: not an hsym
```

**See Also**

[.sample.isdir](#sampleisdir)

:   For directory check.

## .sample.ishsym

Check if a given value is an hsym.

**Parameters**

`x`: *any*

:   Anything.

**Return**

*boolean*

:   `1b` if `x` is an hsym; `0b` otherwise.

**Example**

```q
q).sample.ishsym `:/tmp/abc
1b
q).sample.ishsym `$"/tmp/abc"
0b
```

!!! note

    It doesn't validate if the hsym is valid.
    Second line of note.

## .sample.isoweekday

Return the day of the week as an integer, where Monday is 1 and Sunday is 7.

**Parameters**

`d`⚛: *date*

:   A date.

**Return**

*long*

:   The day of the week.
