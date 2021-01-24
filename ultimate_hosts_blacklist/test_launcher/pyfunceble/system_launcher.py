"""
The test launcher of the Ultimate-Hosts-Blacklist project.

This is the module that provides a modified version of PyFunceble's system
launcher.

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

import argparse
import logging
import os
from datetime import datetime
from typing import Optional

from PyFunceble.cli.system.launcher import SystemLauncher
from PyFunceble.helpers.file import FileHelper
from ultimate_hosts_blacklist.whitelist.core import Core as whitelist_core_tool

from ultimate_hosts_blacklist.test_launcher.administration import Administration
from ultimate_hosts_blacklist.test_launcher.defaults import outputs
from ultimate_hosts_blacklist.test_launcher.pyfunceble.producer_worker import (
    UHBPyFuncebleProducerWorker,
)


class UHBPyFuncebleSystemLauncher(SystemLauncher):

    uhb_administration: Optional[Administration] = None

    def __init__(
        self,
        args: Optional[argparse.Namespace] = None,
        *,
        administration: Optional[Administration],
    ) -> None:

        self.uhb_administration = administration

        if not args:
            self.args = argparse.Namespace(
                files=[outputs.INPUT_DESTINATION],
                domains=None,
                urls=None,
                url_files=None,
            )
        else:
            self.args.files = [outputs.INPUT_DESTINATION]

        super().__init__(args=args)

        self.producer_process_manager.WORKER_OBJ = UHBPyFuncebleProducerWorker

        logging.debug("CI Engine: %r", self.continuous_integration)
        logging.debug(
            "CI Engine authorized ? %r", self.continuous_integration.authorized
        )

    def update_clean_list(self) -> "UHBPyFuncebleSystemLauncher":
        """
        Updates the content of the :code:`clean.list` file.
        """

        input_file = FileHelper(outputs.ACTIVE_SUBJECTS_DESTINATION)
        clean_file = FileHelper(outputs.CLEAN_DESTINATION)

        if input_file.exists():
            logging.info("Started generation of %r.", clean_file.path)

            with input_file.open(
                "r", encoding="utf-8"
            ) as input_file_stream, clean_file.open(
                "w", encoding="utf-8"
            ) as clean_file_stream:
                for line in input_file_stream:
                    line = line.strip()

                    if not line or line.startswith("#") or "." not in line:
                        continue

                    if line.endswith("."):
                        line = line[:-1]

                    clean_file_stream.write(line + "\n")

                clean_file_stream.write("\n")

            logging.info("Finished generation of %r.", clean_file.path)

        return self

    def update_whitelisted_list(self) -> "UHBPyFuncebleSystemLauncher":
        """
        Updates the content of the :code:`whitelist.list` file.
        """

        input_file = FileHelper(outputs.CLEAN_DESTINATION)
        whitelist_file = FileHelper(outputs.WHITELISTED_DESTINATION)

        if input_file.exists():
            logging.info("Started generation of %r.", whitelist_file.path)

            whitelist_core_tool(
                output_file=whitelist_file.path,
                use_official=True,
                processes=os.cpu_count(),
            ).filter(file=input_file.path, already_formatted=True, standard_sort=False)

            logging.info("Finished generation of %r.", whitelist_file.path)

        return self

    def update_volatile_list(self) -> "UHBPyFuncebleSystemLauncher":
        """
        Updates the content of the :code:`volatile.list` file.
        """

        input_file = FileHelper(outputs.TEMP_VOLATIVE_DESTINATION)
        volatile_file = FileHelper(outputs.VOLATILE_DESTINATION)
        clean_file = FileHelper(outputs.CLEAN_DESTINATION)

        logging.info("Started generation of %r.", volatile_file.path)

        with volatile_file.open("w", encoding="utf-8") as volatile_file_stream:
            if clean_file.exists():
                with clean_file.open("r", encoding="utf-8") as clean_file_stream:
                    for line in clean_file_stream:
                        line = line.strip()

                        if not line or line.startswith("#") or "." not in line:
                            continue

                        if line.endswith("."):
                            line = line[:-1]

                        volatile_file_stream.write(line + "\n")

            if input_file.exists():
                with input_file.open("r", encoding="utf-8") as input_file_stream:
                    for line in input_file_stream:
                        line = line.strip()

                        if not line or line.startswith("#") or "." not in line:
                            continue

                        if line.endswith("."):
                            line = line[:-1]

                        volatile_file_stream.write(line + "\n")

            volatile_file.write("\n")

        whitelist_core_tool(
            output_file=volatile_file.path,
            use_official=True,
            processes=os.cpu_count(),
        ).filter(file=volatile_file.path, already_formatted=True, standard_sort=False)

        logging.info("Finished generation of %r.", volatile_file.path)

        return self

    def update_ip_list(self) -> "UHBPyFuncebleSystemLauncher":
        """
        Updates the content of the :code:`ip.list` file.
        """

        input_file = FileHelper(outputs.IP_SUBJECTS_DESTINATION)
        ip_file = FileHelper(outputs.IP_DESTINATION)

        if input_file.exists():
            logging.info("Started generation of %r.", ip_file.path)

            with input_file.open(
                "r", encoding="utf-8"
            ) as input_file_stream, ip_file.open(
                "w", encoding="utf-8"
            ) as ip_file_stream:
                for line in input_file_stream:
                    if not line.strip() or line.startswith("#"):
                        continue

                    ip_file_stream.write("\n".join(line.split()[1:]) + "\n")

                ip_file_stream.write("\n")

            whitelist_core_tool(
                output_file=ip_file.path,
                use_official=True,
                processes=os.cpu_count(),
            ).filter(file=ip_file.path, already_formatted=True, standard_sort=False)

            logging.info("Finished generation of %r.", ip_file.path)

    def run_ci_saving_instructions(self) -> "SystemLauncher":
        if not self.uhb_administration.currently_under_test:
            self.uhb_administration.currently_under_test = True

        self.uhb_administration.save()
        return super().run_ci_saving_instructions()

    def run_standard_end_instructions(self) -> "SystemLauncher":
        self.uhb_administration.currently_under_test = False

        end_datetime = datetime.utcnow()

        self.uhb_administration.end_epoch = (
            self.uhb_administration.end_datetime
        ) = end_datetime

        self.uhb_administration.save()

        self.update_clean_list()
        self.update_whitelisted_list()
        self.update_volatile_list()
        self.update_ip_list()

        return super().run_standard_end_instructions()

    def start(self) -> "SystemLauncher":
        if not self.uhb_administration.currently_under_test:
            self.uhb_administration.currently_under_test = True

            start_datetime = datetime.utcnow()

            self.uhb_administration.previous_start_epoch = (
                self.uhb_administration.previous_start_datetime
            ) = self.uhb_administration.start_datetime

            self.uhb_administration.previous_end_epoch = (
                self.uhb_administration.previous_end_datetime
            ) = self.uhb_administration.end_datetime

            self.uhb_administration.start_epoch = start_datetime
            self.uhb_administration.start_datetime = start_datetime

        return super().start()
