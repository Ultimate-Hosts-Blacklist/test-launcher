"""
The test launcher of the Ultimate-Hosts-Blacklist project.

This is the module that will provides all our output related settings or
defaults.

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

import os

CURRENT_DIRECTORY: str = os.getcwd()

INPUT_FILENAME: str = "domains.list"
CLEAN_FILENAME: str = "clean.list"
WHITELISTED_FILENAME: str = "whitelisted.list"
VOLATILE_FILENAME: str = "volatile.list"
IP_FILENAME: str = "ip.list"
ADMINISTRATION_FILENAME: str = "info.json"
EXAMPLE_ADMINISTRATION_FILENAME: str = "info.example.json"
REQUIREMENTS_FILENAME: str = "requirements.txt"
MANIFEST_FILENAME: str = "MANIFEST.in"
README_FILENAME: str = "README.md"

PYFUNCEBLE_CONFIG_DIRNAME: str = ".pyfunceble"


INPUT_DESTINATION: str = os.path.join(CURRENT_DIRECTORY, INPUT_FILENAME)
CLEAN_DESTINATION: str = os.path.join(CURRENT_DIRECTORY, CLEAN_FILENAME)
WHITELISTED_DESTINATION: str = os.path.join(CURRENT_DIRECTORY, WHITELISTED_FILENAME)
VOLATILE_DESTINATION: str = os.path.join(CURRENT_DIRECTORY, VOLATILE_FILENAME)
IP_DESTINATION: str = os.path.join(CURRENT_DIRECTORY, IP_FILENAME)
ADMINISTRATION_DESTINATION: str = os.path.join(
    CURRENT_DIRECTORY, ADMINISTRATION_FILENAME
)

OUTPUT_ROOT_DIRECTORY: str = os.path.join(CURRENT_DIRECTORY, "output")
OUTPUT_DIRECTORY: str = os.path.join(OUTPUT_ROOT_DIRECTORY, INPUT_FILENAME)
PYFUNCEBLE_CONFIG_DIRECTORY: str = os.path.join(
    CURRENT_DIRECTORY, PYFUNCEBLE_CONFIG_DIRNAME
)


TEMP_VOLATIVE_DESTINATION: str = os.path.join(OUTPUT_DIRECTORY, VOLATILE_FILENAME)
ACTIVE_SUBJECTS_DESTINATION: str = os.path.join(
    OUTPUT_DIRECTORY, "domains", "ACTIVE", "list"
)
IP_SUBJECTS_DESTINATION: str = os.path.join(OUTPUT_DIRECTORY, "hosts", "ACTIVE", "ips")
