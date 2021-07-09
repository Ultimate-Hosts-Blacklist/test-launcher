"""
The test launcher of the Ultimate-Hosts-Blacklist project.

This is the module that overwrites some of of the methods of the official
PyFunceble producer.

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

from typing import Any, Optional, Tuple

from PyFunceble.cli.processes.workers.producer import ProducerWorker
from PyFunceble.helpers.file import FileHelper

from ultimate_hosts_blacklist.test_launcher.defaults import outputs


class UHBPyFuncebleProducerWorker(ProducerWorker):
    def target(self, consumed: Any) -> Optional[Tuple[Any, ...]]:
        result = super().target(consumed)

        if result is not None:
            _, test_result = result

            if (
                hasattr(test_result, "status_after_extra_rules")
                and test_result.status_after_extra_rules is not None
            ):

                FileHelper(outputs.TEMP_VOLATIVE_DESTINATION).write(
                    test_result.idna_subject + "\n"
                )

        return result
