"""
The test launcher of the Ultimate-Hosts-Blacklist project.

This is the module that will provides all our pyfunceble related settings or
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

from PyFunceble.cli.continuous_integration.github_actions import GitHubActions
from PyFunceble.cli.continuous_integration.jenkins import Jenkins

LINKS_STABLE: dict = {
    "license": {
        "link": "https://raw.githubusercontent.com/funilrys/PyFunceble/master/LICENSE",
        "destination": "LICENSE_PyFunceble",
    },
}


LINKS_DEV: dict = {
    "license": {
        "link": "https://raw.githubusercontent.com/funilrys/PyFunceble/dev/LICENSE",
        "destination": "LICENSE_PyFunceble",
    },
}

LINKS: dict = dict(LINKS_DEV)

CONFIGURATION = {
    "lookup": {"timeout": 5.0, "reputation": False},
    "share_logs": True,
    "cli_testing": {
        "whois_db": True,
        "autocontinue": True,
        "preload_file": True,
        "cooldown_time": 0.09,
        "ci": {
            "active": Jenkins().guess_all_settings().authorized
            or GitHubActions().guess_all_settings().authorized,
            "commit_message": "[Autosave] Testing for Ultimate Hosts Blacklist",
            "end_commit_message": "[Results] Testing for Ultimate Hosts Blacklist",
            "max_exec_minutes": 15,
        },
        "file_generation": {"hosts": True, "plain": True},
        "display_mode": {
            "all": False,
            "dots": True,
            "execution_time": True,
            "less": True,
            "percentage": True,
            "quiet": False,
            "simple": False,
            "status": "ALL",
        },
        "testing_mode": {
            "availability": True,
            "syntax": False,
            "reputation": False,
        },
        "max_workers": None
        if not Jenkins().guess_all_settings().authorized
        and not GitHubActions().guess_all_settings().authorized
        else 1,
    },
    "dns": {
        "server": ["9.9.9.10", "149.112.112.10", "2620:fe::10"],
        "protocol": "UDP",
        "follow_server_order": False,
        "trust_server": True,
    },
}
