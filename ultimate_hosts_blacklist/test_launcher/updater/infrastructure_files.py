"""
The test launcher of the Ultimate-Hosts-Blacklist project.

This is the module that provides the updater of all our infrastructure related
files.

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

import logging
import os
import re
import secrets

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

            parent_directory = os.path.dirname(destination)
            os.makedirs(parent_directory, exist_ok=True)

            DownloadHelper(file["link"]).download_text(destination=destination)

            logging.info("Updated: %r", destination)

        for file in pyfunceble.LINKS.values():
            destination = os.path.join(outputs.CURRENT_DIRECTORY, file["destination"])

            parent_directory = os.path.dirname(destination)
            os.makedirs(parent_directory, exist_ok=True)

            DownloadHelper(file["link"]).download_text(destination=destination)

            logging.info("Updated: %r", destination)

        destination = os.path.join(
            outputs.CURRENT_DIRECTORY,
            infrastructure.WORKFLOW_LINKS["main"]["destination"],
        )
        DownloadHelper(infrastructure.WORKFLOW_LINKS["main"]["link"]).download_text(
            destination=destination
        )

        logging.info("Updated: %r", destination)

        scheduled_file = os.path.join(
            outputs.CURRENT_DIRECTORY,
            infrastructure.WORKFLOW_LINKS["scheduler"]["destination"],
        )

        if int(secrets.token_hex(8), 16) % 3 == 0:
            data = DownloadHelper(
                infrastructure.WORKFLOW_LINKS["scheduler"]["link"]
            ).download_text(destination=None)

            random_minute = secrets.randbelow(59)
            random_hour = secrets.randbelow(12)

            # pylint: disable=consider-using-f-string
            new_data = re.sub(
                r'cron: "\d+\s\d+\s(\*\s\*\s\*)"',
                r'cron: "{0} {1} \1"'.format(random_minute, random_hour),
                data,
            )

            with open(scheduled_file, "w", encoding="utf-8") as file_stream:
                file_stream.write(new_data)

                logging.info("Updated: %r", scheduled_file)
