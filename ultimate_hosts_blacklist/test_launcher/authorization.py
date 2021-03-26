"""
The test launcher of the Ultimate-Hosts-Blacklist project.

This is the module that will provides the manage and provides the authorizations
needed for a launch.

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
from datetime import datetime, timedelta
from typing import Optional

from PyFunceble.helpers.command import CommandHelper
from PyFunceble.helpers.regex import RegexHelper

from ultimate_hosts_blacklist.test_launcher.administration import Administration
from ultimate_hosts_blacklist.test_launcher.defaults import infrastructure


class Authorization:
    """
    Provides or deny all sort of authorizations.
    """

    administration: Optional[Administration] = None

    def __init__(self, administration: Administration) -> None:
        self.administration = administration

    @property
    def launch(self) -> bool:
        """
        Provides the authorization to launch.
        """

        if self.launch_marker_in_last_commit():
            logging.info("Test authorized by: Commit message.")

            return True

        if self.administration.currently_under_test:
            logging.info("Test authorized by: Still under test.")

            return True

        if not self.administration.currently_under_test:
            return True

        if int(self.administration.days_until_next_test) >= 1:
            until = self.administration.end_datetime + timedelta(
                days=self.administration.days_until_next_test
            )

            if datetime.utcnow() >= until:
                logging.info("Test authorized by: Restest time in the past.")
                return True

            logging.info("Test not authorized until: %s.", until.isoformat())

        return False

    @property
    def cleanup(self) -> bool:
        """
        Provides the authorization to cleanup.
        """

        if self.launch_marker_in_last_commit():
            logging.info("Cleanup authorized by: Commit message.")

            return True

        if self.administration.currently_under_test:
            logging.info("Cleanup not authorized by: Still under test.")

            return False

        if int(self.administration.days_until_next_test) >= 1:
            if self.administration.end_datetime >= datetime.utcnow() + timedelta(
                days=self.administration.days_until_next_test
            ):
                logging.info("Cleanup authorized by: Restest time in the past.")
                return True
            logging.info("Cleanup not authorized by: Restest time in the future.")
            return False

        return False

    @staticmethod
    def launch_marker_in_last_commit() -> bool:
        """
        Check if the launch marker is into the last commit message.
        """

        return RegexHelper(infrastructure.MARKERS["launch"]).match(
            CommandHelper("git log -1").execute(), return_match=False
        )
