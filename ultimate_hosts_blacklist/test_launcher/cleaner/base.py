"""
The test launcher of the Ultimate-Hosts-Blacklist project.

This is the module that provides the base of all cleaners.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

License:
::


    MIT License

    Copyright (c) 2019-2024 Mitchell Krog - @mitchellkrogza
    Copyright (c) 2019-2024 Nissar Chababy - @funilrys
    Copyright (c) 2019-2024 Ultimate Hosts Blacklist - @Ultimate-Hosts-Blacklist Contributors

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import functools
from typing import List


class CleanerBase:
    """
    This is the base of all cleaner.
    """

    STD_FILES_TO_IGNORE: List[str] = [".keep", ".gitingore"]

    def execute_if_authorized(func):  # pylint: disable=no-self-argument
        """
        Executes the decorated method only if the authorization is granted.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.authorized:
                # pylint: disable=not-callable
                return func(self, *args, **kwargs)
            return None

        return wrapper

    @property
    def authorized(self) -> bool:
        """
        Provides the authorization to start.
        """

        return False

    @execute_if_authorized
    def start(self) -> "CleanerBase":
        """
        Starts the cleaning.
        """

        raise NotImplementedError()
