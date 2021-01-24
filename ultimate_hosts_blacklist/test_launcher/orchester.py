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

from typing import Optional

from PyFunceble.cli.processes.producer import ProducerProcessesManager
from PyFunceble.cli.processes.tester import TesterProcessesManager
from PyFunceble.downloader.ipv4_reputation import IPV4ReputationDownloader

from ultimate_hosts_blacklist.test_launcher.administration import Administration
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

    administration: Optional[Administration] = None

    tester_process_manager: Optional[TesterProcessesManager] = None
    producer_process_manager: Optional[ProducerProcessesManager] = None

    def __init__(
        self,
        administration: Administration,
    ) -> None:
        self.administration = administration

        self.system_launcher = UHBPyFuncebleSystemLauncher(
            administration=self.administration
        )

    def start(self) -> "Orchestration":
        """
        Starts the whole process of orchestration.
        """

        IPV4ReputationDownloader().start()

        self.system_launcher.start()

        return self
