# File exclude plugin for mkdocs

`mkdocs-exclude` is a
[mkdocs plugin](http://www.mkdocs.org/user-guide/plugins/) that allows you
to exclude files from your input using unix-style wildcards (globs) or
regular expressions (regexes).

This implements what people were asking for in some mkdocs bugs, such as
<https://github.com/mkdocs/mkdocs/issues/1500> and
<https://github.com/mkdocs/mkdocs/issues/1152>.


## Quick start

1. Install the module using pip: `pip3 install mkdocs-exclude`

2. In your project, add a plugin configuration to `mkdocs.yml`:

   ```yaml
   plugins:
     - exclude:
         glob:
           - exclude/this/path/*
           - "*.tmp"
           - "*.pdf"
           - "*.gz"
         regex:
           - '.*\.(tmp|bin|tar)$'
         include-glob:
           - include/this/path/*
           - "*.png"
           - "*.md"
           - "assets/**" # the material theme requires this folder
         include-regex:
           - '.*\.(js|css)$'
   ```

You can provide zero or more patterns of each type.  (If you don't provide
any patterns, then nothing will happen!)

Note!  Because of peculiarity of yaml syntax, the `glob:` and `regex:` lines
**must not** start with a dash, but the lines under them **must** start with
a dash.

Also because of yaml, patterns that start with a punctuation mark must be
quoted.

When writing regexes, it's best to use single quotes rather than double
quotes, so that your regex backslash escapes are preserved correctly without
having to be doubled up.

## Exclude and Include

It is possible to exclude and include. For example you could exclude `*` but include `*.md`.
Include has higher priority over exclude.
