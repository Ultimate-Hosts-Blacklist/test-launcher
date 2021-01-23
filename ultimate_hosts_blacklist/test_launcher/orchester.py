"""
The test launcher of the Ultimate-Hosts-Blacklist project.

This is the module that will provides the orchestration of the data flow.

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
import multiprocessing
import os
from typing import Optional

from PyFunceble.cli.continuous_integration.base import ContinuousIntegrationBase
from PyFunceble.cli.processes.producer import ProducerProcessesManager
from PyFunceble.cli.processes.tester import TesterProcessesManager
from PyFunceble.cli.utils.testing import get_destination_from_origin
from PyFunceble.downloader.ipv4_reputation import IPV4ReputationDownloader
from PyFunceble.helpers.file import FileHelper

from ultimate_hosts_blacklist.test_launcher.administration import Administration
from ultimate_hosts_blacklist.test_launcher.defaults import outputs
from ultimate_hosts_blacklist.test_launcher.pyfunceble.system_launcher import (
    UHBPyFuncebleSystemLauncher,
)


class Orchestration:
    """
    This is the orchestration class. It orchestrate the test and production of
    output with the help of PyFunceble.

    :param administration:
        A instance of the admintration management class.
    """

    STD_PROTOCOL: dict = {
        "type": None,
        "subject_type": None,
        "destination": None,
        "source": None,
        "abs_source": None,
        "rel_source": None,
        "subject": None,
        "idna_subject": None,
        "output_dir": None,
        "checker_type": None,
        "session_id": None,
    }

    sync_manager: Optional[multiprocessing.Manager] = None

    administration: Optional[Administration] = None
    continuous_integration: Optional[ContinuousIntegrationBase] = None

    tester_process_manager: Optional[TesterProcessesManager] = None
    producer_process_manager: Optional[ProducerProcessesManager] = None

    def __init__(
        self,
        administration: Administration,
        continuous_integration: ContinuousIntegrationBase,
        max_workers: Optional[int] = None,
    ) -> None:
        self.administration = administration
        self.continuous_integration = continuous_integration

        self.sync_manager = multiprocessing.Manager()

        max_workers = (
            max_workers - 1
            if max_workers is not None
            else TesterProcessesManager.STD_MAX_WORKER + 1
        )

        self.tester_process_manager = TesterProcessesManager(
            self.sync_manager,
            max_worker=max_workers,
            continuous_integration=self.continuous_integration,
            daemon=True,
        )

        self.producer_process_manager = ProducerProcessesManager(
            self.sync_manager,
            max_worker=1,
            input_queue=self.tester_process_manager.output_queue,
            continuous_integration=self.continuous_integration,
            daemon=True,
        )

        self.system_launcher = UHBPyFuncebleSystemLauncher(
            administration=self.administration
        )

    def start_all_process_manager(self) -> "Orchestration":
        """
        Starts all our process manager.
        """

        logging.debug("Started launch of tester proc manager.")

        self.tester_process_manager.send_feeding_signal(worker_name="main")
        self.tester_process_manager.start()

        logging.debug("Finished launch of tester proc manager.")

        logging.debug("Started launch of producer proc manager.")
        self.producer_process_manager.start()
        logging.debug("Finished launch of producer proc manager.")

        return self

    def wait_for_all_process_manager(self) -> "Orchestration":
        """
        Wait for all process manager to finish.
        """

        self.tester_process_manager.wait()

        self.producer_process_manager.wait()

        return self

    def fill_queues_with_protocol(self) -> "Orchestration":
        """
        Waits for the queues with protocol.
        """

        protocol_base = dict(self.STD_PROTOCOL)

        protocol_base["type"] = "files"
        protocol_base["subject_type"] = "domain"
        protocol_base["destination"] = get_destination_from_origin(
            outputs.INPUT_DESTINATION
        )
        protocol_base["source"] = outputs.INPUT_DESTINATION
        protocol_base["abs_source"] = os.path.abspath(outputs.INPUT_DESTINATION)
        protocol_base["rel_source"] = os.path.relpath(outputs.INPUT_DESTINATION)
        protocol_base["checker_type"] = self.administration.pyfunceble[
            "checker_type"
        ].upper()
        protocol_base["session_id"] = self.administration.pyfunceble["session_id"]
        protocol_base["output_dir"] = outputs.OUTPUT_DIRECTORY

        with FileHelper(outputs.INPUT_DESTINATION).open(
            "r", encoding="utf-8"
        ) as file_stream:
            for line in file_stream:
                line = line.strip()
                test_protocol = dict(protocol_base)
                test_protocol["subject"] = line
                test_protocol["idna_subject"] = line

                self.tester_process_manager.add_to_input_queue(
                    test_protocol, worker_name="main"
                )

        self.tester_process_manager.send_stop_signal(worker_name="main")

    def start(self) -> "Orchestration":
        """
        Starts the whole process of orchestration.
        """

        IPV4ReputationDownloader().start()

        self.system_launcher.start()

        return self
