"""
The test launcher of the Ultimate-Hosts-Blacklist project.

This is the module that provides the updater of all our infrastructure related
files.

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

import logging
import os

from PyFunceble.helpers.download import DownloadHelper
from PyFunceble.helpers.file import FileHelper

from ultimate_hosts_blacklist.test_launcher.defaults import (
    infrastructure,
    outputs,
    pyfunceble,
)
from ultimate_hosts_blacklist.test_launcher.updater.base import UpdaterBase


class InfrastructureFilesUpdater(UpdaterBase):
    """
    This is the interface that updates all our infrastructure files.
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

        for file in infrastructure.LINKS.values():
            destination = os.path.join(outputs.CURRENT_DIRECTORY, file["destination"])
            DownloadHelper(file["link"]).download_text(destination=destination)

            logging.info("Updated: %r", destination)

        for file in pyfunceble.LINKS.values():
            destination = os.path.join(outputs.CURRENT_DIRECTORY, file["destination"])
            DownloadHelper(file["link"]).download_text(destination=destination)

            logging.info("Updated: %r", destination)
