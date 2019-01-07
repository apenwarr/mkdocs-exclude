import fnmatch
import re
import sys
import mkdocs
import mkdocs.plugins
import mkdocs.structure.files

class Exclude(mkdocs.plugins.BasePlugin):
    """A mkdocs plugin that removes all matching files from the input list."""

    config_scheme = (
        ('glob', mkdocs.config.config_options.Type((str, list), default=None)),
        ('regex', mkdocs.config.config_options.Type((str, list), default=None)),
    )

    def on_files(self, files, config):
        globs = self.config['glob'] or []
        if not isinstance(globs, list):
            globs = [globs]
        regexes = self.config['regex'] or []
        if not isinstance(regexes, list):
            regexes = [regexes]
        out = []
        def include(name):
            for g in globs:
                if fnmatch.fnmatchcase(i.src_path, g):
                    return False
            for r in regexes:
                if re.match(r, i.src_path):
                    return False
            return True
        for i in files:
            if include(i):
                out.append(i)
        return mkdocs.structure.files.Files(out)
