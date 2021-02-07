import fnmatch
import re
import os
import sys
import mkdocs
import mkdocs.plugins
import mkdocs.structure.files

class ExcludeDecider:
    def __init__(self, globs, regexes, include_globs, include_regexes):
        self.globs = globs
        self.regexes = regexes
        self.include_globs = include_globs
        self.include_regexes = include_regexes

    def is_include(self, file):
        if not self._is_include(file):
            if file.endswith(".md"):
                print("NO", self.include_globs)
            return False
        # Windows reports filenames as eg.  a\\b\\c instead of a/b/c.
        # To make the same globs/regexes match filenames on Windows and
        # other OSes, let's try matching against converted filenames.
        # On the other hand, Unix actually allows filenames to contain
        # literal \\ characters (although it is rare), so we won't
        # always convert them.  We only convert if os.sep reports
        # something unusual.  Conversely, some future mkdocs might
        # report Windows filenames using / separators regardless of
        # os.sep, so we *always* test with / above.
        if os.sep != '/':
            filefix = file.replace(os.sep, '/')
            if not self._is_include(filefix):
                return False
        return True

    def _is_include(self, file):
        for g in self.include_globs:
            if fnmatch.fnmatchcase(file, g):
                return True
        for r in self.include_regexes:
            if re.match(r, file):
                return True
        for g in self.globs:
            if fnmatch.fnmatchcase(file, g):
                return False
        for r in self.regexes:
            if re.match(r, file):
                return False
        return True

def get_list_from_config(name, config):
    """ Gets a list item from config. If it doesn't exist, gets empty list.
    If it is not a list, wrap it in a list """
    result = config[name] or []
    if not isinstance(result, list):
        result = [result]
    return result

class Exclude(mkdocs.plugins.BasePlugin):
    """A mkdocs plugin that removes all matching files from the input list."""

    config_scheme = (
        ('glob', mkdocs.config.config_options.Type((str, list), default=None)),
        ('regex', mkdocs.config.config_options.Type((str, list), default=None)),
        ('include-glob', mkdocs.config.config_options.Type((str, list), default=None)),
        ('include-regex', mkdocs.config.config_options.Type((str, list), default=None)),
    )

    def on_files(self, files, config):
        for k in self.config:
            for scheme in self.config_scheme:
                if scheme[0] == k:
                    break
            else:
                raise Exception("Configuration '%s' not found for exclude-plugin" % k)

        globs = get_list_from_config('glob', self.config)
        regexes = get_list_from_config('regex', self.config)
        include_globs = get_list_from_config('include-glob', self.config)
        include_regexes = get_list_from_config('include-regex', self.config)
        exclude_decider = ExcludeDecider(globs, regexes, include_globs, include_regexes)
        out = []
        for i in files:
            name = i.src_path
            if exclude_decider.is_include(name):
                print("include:",name)
                out.append(i)
        return mkdocs.structure.files.Files(out)
