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


from abc import ABCMeta
from typing import Optional
from .ide_manager import IdeManager




class CommonTermIde(IdeManager, metaclass=ABCMeta):
    """ Behaviors and data common to bth IDEs and isolated terminals. """


    term_height: Optional[int] = None
    """
    Number of lines to define the height of the terminal (unless it's vertical)
    """


    def exported_items(self):
        """
        Generate all the items of data that must be exported to JS.
        """
        yield from super().exported_items()
        yield from [
            ("stdout_cut_off", self.env.stdout_cut_off),
            ("cut_feedback",   self.env.cut_feedback),
        ]
