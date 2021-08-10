import fnmatch
import re
import os
import subprocess
import mkdocs
import mkdocs.plugins
import mkdocs.structure.files

class Exclude(mkdocs.plugins.BasePlugin):
    """A mkdocs plugin that removes all matching files from the input list."""

    config_scheme = (
        ('glob', mkdocs.config.config_options.Type((str, list), default=None)),
        ('regex', mkdocs.config.config_options.Type((str, list), default=None)),
        ('gitignore', mkdocs.config.config_options.Type((bool,), default=False)),
    )

    def on_files(self, files, config):
        globs = self.config['glob'] or []
        if not isinstance(globs, list):
            globs = [globs]
        regexes = self.config['regex'] or []
        if not isinstance(regexes, list):
            regexes = [regexes]
        gitignore = self.config['gitignore']
        out = []
        def include(name):
            for g in globs:
                if fnmatch.fnmatchcase(name, g):
                    return False
            for r in regexes:
                if re.match(r, name):
                    return False
            return True
        for i in files:
            name = i.src_path
            if not include(name):
                continue
            abs_path = i.abs_src_path
            if gitignore and git_ignores_path(abs_path):
                continue

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
                namefix = name.replace(os.sep, '/')
                if not include(namefix):
                    continue
            out.append(i)
        return mkdocs.structure.files.Files(out)

def git_ignores_path(abs_path):
    r"""
    This is adapted from `pytest-gitignore
    <https://github.com/tgs/pytest-gitignore/blob/7dc7087f16dbc467435e08f7faeac64d7ee0f0a1/pytest_gitignore.py#L18-L35>`_,
    which, as of the adaptation, was `signaled as being in the public domain
    <https://github.com/tgs/pytest-gitignore/blob/7dc7087f16dbc467435e08f7faeac64d7ee0f0a1/LICENSE>`_.
    """
    if os.path.basename(abs_path) == '.git':  # Ignore .git directory
        return True
    cmd = ['git', 'check-ignore', abs_path]
    result = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True)
    status = result.returncode
    # Possible return values: (via git help check-ignore)
    #    0: Yes, the file is ignored
    #    1: No, the file isn't ignored
    #  128: Fatal error, git can't tell us whether to ignore
    #
    # The latter happens a lot with python virtualenvs, since they have
    # symlinks and git gives up when you try to follow one.  But maybe you have
    # a test directory that you include with a symlink, who knows?  So we treat
    # the file as not-ignored.
    return status == 0
