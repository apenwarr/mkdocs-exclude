import fnmatch
import re
import os
import sys
import mkdocs
import mkdocs.plugins
import mkdocs.structure.files
import typing


class Exclude(mkdocs.plugins.BasePlugin):
    """A mkdocs plugin that removes all matching files from the input list."""

    config_scheme = (
        ('glob', mkdocs.config.config_options.Type((str, list), default=None)),
        ('regex', mkdocs.config.config_options.Type((str, list), default=None)),
    )

    def on_config(self, config):
        globs, regexes = self.__get_exclude_config()
        new_nav, _ = self.__filter_nav(config['nav'], globs, regexes)
        config['nav'] = new_nav
        return config

    def on_files(self, files, config):
        globs, regexes = self.__get_exclude_config()
        out = []
        for i in files:
            name = i.src_path
            if not self.__include(name, globs, regexes):
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
                if not self.__include(namefix, globs, regexes):
                    continue
            out.append(i)
        return mkdocs.structure.files.Files(out)

    def __filter_nav(self, nav, globs, regexes):
        """Recursively filters navigation items based on excluded files

        Headers that would remain empty are removed.
        """
        new_nav = []
        removed = 0
        for nav_item in nav:
            # Flat list of individual navigation items objects
            if isinstance(nav_item, list):
                new_nav.extend(self.__filter_nav(nav_item, globs, regexes)[0])
            elif isinstance(nav_item, dict):
                for name, content in nav_item.items():
                    # Nested navigation section (name: [nested, sections])
                    if isinstance(content, list):
                        filtered_nav, removed = self.__filter_nav(content, globs, regexes)
                        # Only append this category to new nav if there
                        # are any contents
                        if removed < len(content):
                            new_nav.append({name: filtered_nav})
                    # Base case, content is the link to the .md file
                    elif isinstance(content, str):
                        if self.__include(content, globs, regexes):
                            new_nav.append({name: content})
                        else:
                            removed += 1

        return new_nav, removed

    def __get_exclude_config(self) -> typing.Tuple[typing.List[str], typing.List[str]]:
        globs = self.config['glob'] or []
        if not isinstance(globs, list):
            globs = [globs]
        regexes = self.config['regex'] or []
        if not isinstance(regexes, list):
            regexes = [regexes]

        return globs, regexes

    def __include(self, name, globs, regexes):
        for g in globs:
            if fnmatch.fnmatchcase(name, g):
                return False
        for r in regexes:
            if re.match(r, name):
                return False
        return True

