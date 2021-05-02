"""
The test launcher of the Ultimate-Hosts-Blacklist project.

This is the module that provides the updater of the README file.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

License:
::


    MIT License

    Copyright (c) 2019, 2020, 2021 Ultimate-Hosts-Blacklist
    Copyright (c) 2019, 2020, 2021 Nissar Chababy
    Copyright (c) 2019, 2020, 2021 Mitchell Krog

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

import importlib.resources
import logging
import os

from PyFunceble.helpers.file import FileHelper

from ultimate_hosts_blacklist.test_launcher.defaults import outputs
from ultimate_hosts_blacklist.test_launcher.updater.base import UpdaterBase


class ReadmeUpdater(UpdaterBase):
    """
    This is the interface that updates our readme file.
    """

    @property
    def authorized(self) -> bool:
        """
        Provides the authorization to launch.
        """

        return not FileHelper(
            os.path.join(
                outputs.CURRENT_DIRECTORY, outputs.EXAMPLE_ADMINISTRATION_FILENAME
            )
        ).exists()

    @UpdaterBase.execute_if_authorized
    def start(self) -> "UpdaterBase":
        """
        Starts the update process.
        """

        if self.administration.raw_link:
            with importlib.resources.path(
                "ultimate_hosts_blacklist.test_launcher.data.docs",
                "about_repository.md",
            ) as file_path:
                content = FileHelper(str(file_path)).read()
        else:
            with importlib.resources.path(
                "ultimate_hosts_blacklist.test_launcher.data.docs",
                "about_repository_self.md",
            ) as file_path:
                content = FileHelper(str(file_path)).read()

        content += "\n\n"

        with importlib.resources.path(
            "ultimate_hosts_blacklist.test_launcher.data.docs", "about_ultimate.md"
        ) as file_path:
            content += FileHelper(str(file_path)).read()

        content += "\n\n"

        with importlib.resources.path(
            "ultimate_hosts_blacklist.test_launcher.data.docs", "about_pyfunceble.md"
        ) as file_path:
            content += FileHelper(str(file_path)).read()

        content += "\n"

        readme_file = FileHelper(
            os.path.join(outputs.CURRENT_DIRECTORY, outputs.README_FILENAME)
        )
        readme_file.write(content, overwrite=True)

        logging.info("Updated: %r", readme_file.path)
