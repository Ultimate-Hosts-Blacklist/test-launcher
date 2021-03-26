"""
The test launcher of the Ultimate-Hosts-Blacklist project.

This is the module that provides the infrastructure cleaner.

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
from typing import List

from PyFunceble.helpers.directory import DirectoryHelper
from PyFunceble.helpers.file import FileHelper

from ultimate_hosts_blacklist.test_launcher.cleaner.base import CleanerBase
from ultimate_hosts_blacklist.test_launcher.defaults import outputs


class InfrastructureCleaner(CleanerBase):
    """
    This is the infrastructure cleaner. If will ensure that our repository
    stays clean.
    """

    FILES_TO_REMOVE: List[str] = [
        ".PyFunceble_cross_input_sources.yaml",
        ".pyfunceble_intern_downtime.json",
        ".PyFunceble_production.yaml",
        ".PyFunceble.yaml",
        ".travis.yml",
        "administration.py",
        "dir_structure.json",
        "iana-domains-db.json",
        "inactive_db.json",
        "LICENSE_PyFunceble",
        "public-suffix.json",
        "update.py",
        "user_agents.json",
        ".PyFunceble_LICENSE",
        "requirements.txt",
        "Jenkinsfile",
        [".pyfunceble", "ipv4_reputation.data"],
    ]

    FILES_TO_MOVE_TO_PYFUNCEBLE_CONFIG: List[str] = ["whois_db.json"]

    @property
    def authorized(self):
        return not FileHelper(
            os.path.join(
                outputs.CURRENT_DIRECTORY, outputs.EXAMPLE_ADMINISTRATION_FILENAME
            )
        ).exists()

    @CleanerBase.execute_if_authorized
    def start(self) -> "InfrastructureCleaner":
        analytic_directory = DirectoryHelper(
            os.path.join(outputs.OUTPUT_ROOT_DIRECTORY, "json")
        )

        if analytic_directory.exists():
            for element in os.listdir(outputs.OUTPUT_ROOT_DIRECTORY):
                if any(x in element for x in self.STD_FILES_TO_IGNORE):
                    continue

                dir_helper = DirectoryHelper(
                    os.path.join(outputs.OUTPUT_ROOT_DIRECTORY, element)
                )

                if dir_helper.exists():
                    dir_helper.delete()

                    logging.info("Deleted: %r", dir_helper.path)

        del analytic_directory

        for file in self.FILES_TO_REMOVE:
            if not isinstance(file, list):
                file_helper = FileHelper(os.path.join(outputs.CURRENT_DIRECTORY, file))
            else:
                file_helper = FileHelper(os.path.join(outputs.CURRENT_DIRECTORY, *file))

            if file_helper.exists():
                file_helper.delete()
                logging.info("Deleted: %r", file_helper.path)

        for file in self.FILES_TO_MOVE_TO_PYFUNCEBLE_CONFIG:
            file_helper = FileHelper(os.path.join(outputs.CURRENT_DIRECTORY, file))

            if file_helper.exists():
                file_helper.move(
                    os.path.join(outputs.PYFUNCEBLE_CONFIG_DIRECTORY, file)
                )

                logging.info("Moved: %r", file_helper.path)

        return self
