"""
The test launcher of the Ultimate-Hosts-Blacklist project.

This is the module that provides the command line interface.

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

import colorama
import PyFunceble.facility
import PyFunceble.storage
from PyFunceble import __version__ as pyfunceble_version
from PyFunceble.helpers.directory import DirectoryHelper
from PyFunceble.helpers.merge import Merge

from ultimate_hosts_blacklist.test_launcher import __version__
from ultimate_hosts_blacklist.test_launcher.administration import Administration
from ultimate_hosts_blacklist.test_launcher.authorization import Authorization
from ultimate_hosts_blacklist.test_launcher.cleaner.infrastructure import (
    InfrastructureCleaner,
)
from ultimate_hosts_blacklist.test_launcher.defaults import outputs
from ultimate_hosts_blacklist.test_launcher.defaults import (
    pyfunceble as pyfunceble_defaults,
)
from ultimate_hosts_blacklist.test_launcher.orchester import Orchestration
from ultimate_hosts_blacklist.test_launcher.updater.infrastructure_files import (
    InfrastructureFilesUpdater,
)
from ultimate_hosts_blacklist.test_launcher.updater.output_files import (
    OutputFilesUpdater,
)
from ultimate_hosts_blacklist.test_launcher.updater.readme import ReadmeUpdater
from ultimate_hosts_blacklist.test_launcher.updater.requirements import (
    RequirementsUpdater,
)


def tool() -> None:
    """
    This it the entrypoint of the CLI.
    """

    colorama.init(autoreset=True)

    parser = argparse.ArgumentParser(
        description="The test launcher of the Ultimate-Hosts-Blacklist project.",
        epilog=f"Crafted with {colorama.Fore.RED}♥{colorama.Fore.RESET} by "
        f"{colorama.Style.BRIGHT}{colorama.Fore.GREEN}Nissar Chababy (Funilrys)",
    )

    parser.add_argument(
        "-d",
        "--debug",
        help="Activates the debug mode.",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "-v",
        "--version",
        help="Show the version end exist.",
        action="version",
        version="%(prog)s " + __version__,
    )

    args = parser.parse_args()

    if args.debug:
        logging_level = logging.DEBUG
        PyFunceble.facility.Logger.activated = True
        PyFunceble.facility.Logger.min_level = "info"
        PyFunceble.facility.Logger.init_loggers()
    else:
        logging_level = logging.INFO
        PyFunceble.facility.Logger.activated = False

    logging.basicConfig(
        format="[%(asctime)s::%(levelname)s] %(message)s", level=logging_level
    )

    logging.info("Launcher version: %s", __version__)
    logging.info("PyFunceble version: %s", pyfunceble_version)

    administration = Administration()

    DirectoryHelper(outputs.PYFUNCEBLE_CONFIG_DIRECTORY).create()

    PyFunceble.storage.CONFIG_DIRECTORY = outputs.PYFUNCEBLE_CONFIG_DIRECTORY
    PyFunceble.facility.ConfigLoader.path_to_config = os.path.join(
        PyFunceble.storage.CONFIG_DIRECTORY,
        PyFunceble.storage.CONFIGURATION_FILENAME,
    )

    if administration.pyfunceble["config"] and isinstance(
        administration.pyfunceble["config"], dict
    ):
        our_config = Merge(administration.pyfunceble["config"]).into(
            pyfunceble_defaults.CONFIGURATION, strict=True
        )
    else:
        our_config = pyfunceble_defaults.CONFIGURATION

    PyFunceble.facility.ConfigLoader.set_custom_config(our_config).set_merge_upstream(
        True
    ).start()

    authorization = Authorization(administration)

    if authorization.launch:
        InfrastructureCleaner().start()
        RequirementsUpdater(administration).start()
        InfrastructureFilesUpdater(administration).start()
        OutputFilesUpdater(administration).start()
        ReadmeUpdater(administration).start()

        Orchestration(
            administration=administration,
        ).start()

    administration.save()
