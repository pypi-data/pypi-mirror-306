"""
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
"""
# pylint: disable=multiple-statements



import os
import re
from typing import ClassVar, Iterable, List, Optional, Set
from dataclasses import dataclass
from collections import defaultdict

from mkdocs.exceptions import BuildError
from mkdocs.config.defaults import MkDocsConfig

from ...__version__ import __version__
from ..pyodide_logger import logger
from .config import PLUGIN_CONFIG_SRC
from .maestro_base import BaseMaestro









class MaestroContracts(BaseMaestro):
    """
    Mixin enforcing various contracts on PMT usage within mkdocs.
    """


    is_dirty: bool

    __mkdocs_checked = False
    """ Flag to check the mkdocs.yml config once only """


                                                            # pylint: disable-next=all
    def on_startup(self, command:str, dirty:bool):
        # pylint: disable=attribute-defined-outside-init
        self.is_dirty = dirty


    # Override
    def on_config(self, config:MkDocsConfig):

        self._check_material_prefixes_plugins_config_once(config)
        self._check_docs_paths_validity()
        PLUGIN_CONFIG_SRC.validate_macros_plugin_config(self)
        PLUGIN_CONFIG_SRC.handle_deprecated_options_and_conversions(self)

        super().on_config(config)




    def _check_docs_paths_validity(self) -> None :
        """
        Travel through all paths in the docs_dir and raises an BuildError if "special characters"
        are found in directory, py, or md file names (accepted characters are: r'[\\w.-]+' )

        NOTE: Why done here and not in `_on_files`?
                => because on_files is subject to files exclusions, and most python files SHOULD
                have been excluded from the build. So `on_files` could make more sense considering
                the kind of task, but is not technically appropriate/relevant anyway...
        """
        if self.skip_py_md_paths_names_validation:
            logger.warning("The build.skip_py_md_paths_names_validation option is activated.")
            return

        logger.debug("Markdown path names validation.")

        invalid_chars = re.compile(r'[^A-Za-z0-9_.-]+')
        wrongs = defaultdict(list)

        # Validation is done on the individual/current segments of the paths, so that an invalid
        # directory name is not affecting the validation of its children:
        for path,dirs,files in os.walk(self.docs_dir):

            files_to_check = [ file for file in files if re.search(r'\.(py|md)$', file)]

            for segment in dirs + files_to_check:
                invalids = frozenset(invalid_chars.findall(segment))
                if invalids:
                    wrongs[invalids].append( os.path.join(path,segment) )

        if wrongs:
            msg = ''.join(
                f"\nInvalid characters {repr(''.join(sorted(invalids)))} found in these filepaths:"
                + "".join(f"\n\t{ path }" for path in sorted(lst))
                for invalids,lst in wrongs.items()
            )
            raise BuildError(
                f"{ msg }\nPython and markdown files, and their parent directories' names "
                'should only contain alphanumerical characters (no accents or special chars), '
                "dots, underscores, and/or hyphens."
            )



    def _check_material_prefixes_plugins_config_once(self, config:MkDocsConfig):
        """
        Following 2.2.0 breaking change: material plugins' do not _need_ to be prefixed
        anymore, but the json schema validation expects non prefixed plugin names, so:

            if config.theme.name is material:
                error + how to fix it (mismatched config)
            if "material/plugin":
                error + how to fix it (pmt/...)
            if config.theme.name is something else (theme extension):
                if not "pmt/plugin":  error + how to fix it (pmt/...)


        HOW TO SPOT VALUES:
            Access plugins (dict):  `config.plugins`

                Containing keys (behavior of material's plugins only!):
                * `{theme.name}/search`  <-  `mkdocs.yml:plugins: - search`
                * `{some}/search`        <-  `mkdocs.yml:plugins: - {some}/search`
                => The theme prefix IS ALWAYS THERE in the config!
        """
        if self.__mkdocs_checked:
            return
        self.__mkdocs_checked = True # pylint: disable=attribute-defined-outside-init


        errors       = []
        material     = 'material'
        pmt          = 'pyodide-mkdocs-theme'
        theme        = config.theme.name
        is_extension = theme and theme not in (material, pmt, None)
        registered   = RegisteredPlugin.convert(config.plugins)


        if not theme or theme==material:
            errors.append(
                f"The { pmt }'s plugin is registered, so `theme.name` should be set "
                f"to `{ pmt }` instead of `{ theme }`."
            )

        features = config.theme.get('features', ())
        if 'navigation.instant' in features:
            errors.append(
                "Remove `navigation.instant` from `mkdocs.yml:theme.features`. "
                "It is not compatible with the pyodide-mkdocs-theme."
            )

        for plug in registered:
            if plug.prefix != theme:
                errors.append(
                    f"The `{ plug.qualname }` plugin should be registered " + (
                        f"with `pyodide-mkdocs-theme/{ plug.name }`."
                            if is_extension else
                        f"using `{ plug.name }` only{ ' (PMT >= 2.2.0)' * (theme==pmt) }."
                    )
                )

        if errors:
            str_errors = ''.join(map( '\n  {}'.format, errors ))
            raise BuildError(
                f"Invalid theme or material's plugins configuration(s):{ str_errors }"
            )









@dataclass
class RegisteredPlugin:
    """
    Represents an mkdocs plugin name, with information about how it's built.
    """

    qualname: str
    """ Fully qualified name: 'pyodide-mkdocs-theme/search' """

    name: str
    """ Plugin's name: 'search' """

    prefix: Optional[str]
    """ Plugin's prefix: 'pyodide-mkdocs-theme' or None """



    MATERIAL_PLUGINS: ClassVar[Set[str]] = set('''
        blog group info offline privacy search social tags
    '''.split())
    """
    All existing mkdocs-material plugins.
    See: https://github.com/squidfunk/mkdocs-material/tree/master/src/plugins
    """


    @classmethod
    def convert(cls, plugins:Iterable[str]) -> List['RegisteredPlugin'] :
        pattern = re.compile(
            f"(?:(?P<prefix>\\w*)/)?(?P<name>{ '|'.join(cls.MATERIAL_PLUGINS) })"
        )
        registered = [
            RegisteredPlugin(m[0], m['name'], m['prefix'])
                for m in map(pattern.fullmatch, plugins)
                if m
        ]
        return registered
