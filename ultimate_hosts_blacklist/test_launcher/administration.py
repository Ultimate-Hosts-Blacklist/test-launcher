"""
The test launcher of the Ultimate-Hosts-Blacklist project.

This is the module that provides the administration management interface.
The interface provided by this module, will provides all information needed
to operate smoothly.


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
from typing import Any, Optional

from PyFunceble.helpers.command import CommandHelper
from PyFunceble.helpers.dict import DictHelper
from PyFunceble.helpers.file import FileHelper

from ultimate_hosts_blacklist.test_launcher.defaults import infrastructure, outputs


class Administration:
    """
    Provides the administration interface.
    """

    info_file_location: Optional[str] = None
    info_file_helper: Optional[FileHelper] = None
    __our_info: dict = dict()

    def __init__(self) -> None:
        self.info_file_location = outputs.ADMINISTRATION_DESTINATION
        self.info_file_helper = FileHelper(self.info_file_location)

        self.__our_info.update(self.load())

    def __contains__(self, index: str) -> bool:
        return index in self.__our_info

    def __getitem__(self, index: str) -> Any:
        if index in self.__our_info:
            return self.__our_info[index]

        raise KeyError(index)

    def __getattr__(self, index: str) -> Any:
        if index in self.__our_info:
            return self.__our_info[index]

        raise AttributeError(index)

    def __setattr__(self, index: str, value: Any) -> None:
        if self.__our_info:
            self.__our_info[index] = value
        else:
            super().__setattr__(index, value)

    def __delattr__(self, index: str) -> None:
        if index in self.info:
            del self.info[index]

    def __del__(self) -> None:
        self.save()

    @staticmethod
    def convert_data_for_system(data: dict) -> dict:
        """
        Given the content of the info file, we convert it into something our
        system may understand.

        .. warning::
            This method also delete the keys that are scheduled or declared
            for deletion

        :param data:
            The data to work with.
        """

        result = dict()

        for key, value in dict(data).items():
            if key in infrastructure.ADMINISTRATION_INDEXES["delete"]:
                continue

            if key == "name":
                result[key] = (
                    CommandHelper("basename $(git rev-parse --show-toplevel)")
                    .execute()
                    .strip()
                )
            elif key in infrastructure.ADMINISTRATION_INDEXES["bool"]:
                result[key] = bool(int(value))
            elif key in infrastructure.ADMINISTRATION_INDEXES["int"]:
                result[key] = int(value)
            elif key in infrastructure.ADMINISTRATION_INDEXES["dict"]:
                result[key] = dict(value)
            elif key in infrastructure.ADMINISTRATION_INDEXES["datetime"]:
                try:
                    result[key] = datetime.fromisoformat(value)
                except ValueError:
                    result[key] = datetime.utcnow()
            elif key in infrastructure.ADMINISTRATION_INDEXES["epoch"]:
                result[key] = datetime.fromtimestamp(value)
            else:
                result[key] = value

        if "pyfunceble" not in result:
            result["pyfunceble"] = {
                "config": {},
            }

        for sanitize_type, keys in infrastructure.ADMINISTRATION_INDEXES.items():
            if sanitize_type == "delete":
                continue

            for key in keys:
                if key not in result:
                    if sanitize_type == "bool":
                        local_result = bool(None)
                    elif sanitize_type == "int":
                        local_result = 0
                    elif sanitize_type == "dict":
                        local_result = dict()
                    elif sanitize_type == "datetime":
                        local_result = datetime.utcnow() - timedelta(days=365.25)
                    elif sanitize_type == "epoch":
                        local_result = datetime.utcnow() - timedelta(days=365.25)
                    else:
                        local_result = None

                    result[key] = local_result

        return result

    @staticmethod
    def convert_data_for_file(data: dict) -> dict:
        """
        Given the content of the info file, we convert it into something that
        can be saved into a JSON file.

        .. warning::
            This method also delete the keys that are scheduled or declared
            for deletion

        :param data:
            The data to work with.
        """

        result = dict()

        for key, value in dict(data).items():
            if key in infrastructure.ADMINISTRATION_INDEXES["delete"]:
                continue

            if key in infrastructure.ADMINISTRATION_INDEXES["bool"]:
                result[key] = bool(value)
            elif key in infrastructure.ADMINISTRATION_INDEXES["int"]:
                result[key] = int(value)
            elif key in infrastructure.ADMINISTRATION_INDEXES["datetime"]:
                result[key] = value.isoformat()
            elif key in infrastructure.ADMINISTRATION_INDEXES["epoch"]:
                result[key] = value.timestamp()
            else:
                result[key] = value

        return result

    def load(self) -> dict:
        """
        Loads and return the content of the administration file.
        """

        content = self.info_file_helper.read()
        logging.debug("Administration file content:\n%s", content)

        return self.convert_data_for_system(
            DictHelper().from_json(content, return_dict_on_error=False)
        )

    def save(self) -> dict:
        """
        Saves the loaded content of the administration file.
        """

        DictHelper(self.convert_data_for_file(self.__our_info)).to_json_file(
            self.info_file_location
        )
