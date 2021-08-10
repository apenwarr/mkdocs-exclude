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
         gitignore: true
         glob:
           - exclude/this/path/*
           - "*.tmp"
           - "*.pdf"
           - "*.gz"
         regex:
           - '.*\.(tmp|bin|tar)$'
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

Setting `gitignore` to `true` will ignore files if `git` ignores them.<sup>1</sup> (This
defaults to `false` if omitted.)

---

<sup>1</sup> Some environments like [`tox`](https://tox.readthedocs.io/) do not pass on
the `HOME` environment variable by default. `git` uses `HOME` to expand configurations
like `excludesfile = ~/.gitignore`. If you rely on `git` configurations other than what
lives in your repository, this can lead to disparities between what you observe when
running `git` in your shell versus what gets ignored by this plugin. If you experience
this and are unable to move the requisite configuration into your repository’s
`.gitignore` file(s), consider exposing the `HOME` environment variable to your build
environment, or modifying `.git/config` or `.git/info/exclude` in your local repository
copy.
