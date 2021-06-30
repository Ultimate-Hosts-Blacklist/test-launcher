"""
The test launcher of the Ultimate-Hosts-Blacklist project.

This is the module that will provides all our infrastructure related settings or
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
from typing import Dict, List

WORKFLOW_LINKS: dict = {
    "main": {
        "link": "https://raw.githubusercontent.com/Ultimate-Hosts-Blacklist/template/master/.github/workflows/main.yml",  # noqa: E501
        "destination": os.path.join(".github", "workflows", "main.yml"),
    },
    "scheduler": {
        "link": "https://raw.githubusercontent.com/Ultimate-Hosts-Blacklist/template/master/.github/workflows/scheduler.yml",  # noqa: E501
        "destination": os.path.join(".github", "workflows", "scheduler.yml"),
    },
}

CENTRAL_LINKS: dict = {
    "license": {
        "link": "https://raw.githubusercontent.com/Ultimate-Hosts-Blacklist/template/master/LICENSE",  # noqa: E501
        "destination": "LICENSE",
    },
    "gitattributes": {
        "link": "https://raw.githubusercontent.com/Ultimate-Hosts-Blacklist/template/master/.gitattributes",  # noqa: E501
        "destination": ".gitattributes",
    },
}

LINKS_STABLE: dict = {}


LINKS_DEV: dict = {}

# This is the one we are going to use.
LINKS: dict = {**CENTRAL_LINKS, **LINKS_DEV}

MARKERS: dict = {"launch": r"Launch\stest"}

ADMINISTRATION_INDEXES: Dict[str, List[str]] = {
    "bool": ["currently_under_test"],
    "int": ["days_until_next_test", "last_test"],
    "dict": ["custom_pyfunceble_config"],
    "datetime": [
        "start_datetime",
        "end_datetime",
        "previous_start_datetime",
        "previous_end_datetime",
    ],
    "epoch": ["start_epoch", "end_epoch", "previous_start_epoch", "previous_end_epoch"],
    "delete": [
        "arguments",
        "clean_original",
        "stable",
        "last_test",
        "last_autosave_epoch",
        "last_autosave_datetime",
        "previous_stats",
        "current_stats",
        "custom_pyfunceble_config",
    ],
}


REQUIREMENTS_FILE_CONTENT: List[str] = [
    "PyFunceble-dev",
    "ultimate-hosts-blacklist-test-launcher",
]

AUTOMATED_ISSUE_REPOSITORY: str = "Ultimate-Hosts-Blacklist/dev-center"
AUTOMATED_ISSUE_ASSIGNEE: str = "funilrys"

AUTOMATED_ISSUE_TEMPLATE: str = """An error occurred while testing [%(name)s](https://github.com/Ultimate-Hosts-Blacklist/%(name)s).
Please take the time to fix it.

Detail:

```
%(error_detail)s
```

Kind regards


_P.S.: This issue was automatically submitted._

"""  # noqa: E501
