"""
The test launcher of the Ultimate-Hosts-Blacklist project.

This is the module that provides the updater of all our output files.

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
import os
import tempfile
from typing import List, Set, Tuple, Union

from PyFunceble.cli.utils.testing import get_subjects_from_line
from PyFunceble.helpers.download import DownloadHelper
from PyFunceble.helpers.file import FileHelper
from ultimate_hosts_blacklist.whitelist.core import Core as whitelist_core_tool

from ultimate_hosts_blacklist.test_launcher.administration import Administration
from ultimate_hosts_blacklist.test_launcher.defaults import outputs
from ultimate_hosts_blacklist.test_launcher.updater.base import UpdaterBase


class OutputFilesUpdater(UpdaterBase):
    """
    This is the interface that updates all our output files.
    """

    def __init__(self, administration: Administration) -> None:
        self.final_destination = outputs.INPUT_DESTINATION

        self.files_to_clean = [
            outputs.CLEAN_DESTINATION,
            outputs.IP_DESTINATION,
            outputs.VOLATILE_DESTINATION,
            outputs.WHITELISTED_DESTINATION,
        ]

        self.download_temp_file = tempfile.NamedTemporaryFile(mode="r", delete=False)

        self.whitelist_list = tempfile.NamedTemporaryFile(mode="r", delete=False)

        super().__init__(administration)

    def __del__(self) -> None:
        FileHelper(self.download_temp_file.name).delete()
        FileHelper(self.whitelist_list.name).delete()

    @property
    def authorized(self) -> bool:
        """
        Provides the authorization to launch.
        """

        return not FileHelper(
            os.path.join(
                outputs.CURRENT_DIRECTORY, outputs.EXAMPLE_ADMINISTRATION_FILENAME
            )
        ).exists()

    def __get_diff_data(
        self,
        current_content: Set[str],
        subjects: Union[List[str], Set[str], Tuple[str], str],
    ) -> Tuple[Set[str], Set[str]]:
        """
        Provides the diff.
        """

        new = set()
        kept = set()

        if isinstance(subjects, (set, tuple, list)):
            for subject in subjects:
                kept_kept, new_new = self.__get_diff_data(current_content, subject)

                new.update(new_new)
                kept.update(kept_kept)
        elif subjects in current_content:
            kept.add(subjects)
        else:
            new.add(subjects)

        return kept, new

    def produce_diff(self) -> None:
        """
        Produce the difference from teh downloaded file.
        """

        file_helper = FileHelper(self.final_destination)

        new = set()
        kept = set()
        removed = set()

        if file_helper.exists():
            with file_helper.open("r", encoding="utf-8") as file_stream:
                current_content = set(x.strip() for x in file_stream)
        else:
            current_content = set()

        downloaded_empty = True

        for line in self.download_temp_file:
            if downloaded_empty:
                downloaded_empty = False

            line = line.strip()

            if not line:
                continue

            kept_kept, new_new = self.__get_diff_data(
                current_content, get_subjects_from_line(line, "availability")
            )

            new.update(new_new)
            kept.update(kept_kept)

        if downloaded_empty:
            kept = current_content
        else:
            compare_base = kept.copy()
            compare_base.update(new)

            removed = current_content - compare_base

        self.download_temp_file.seek(0)

        return kept, removed, new

    def remove_removed(self) -> None:
        """
        Removed the removed entries from all files to clean.
        """

        file_helper = FileHelper()

        for file in self.files_to_clean:
            if not file_helper.set_path(file).exists():
                continue

            logging.info(
                "Started to cleanup: %r",
                file,
            )
            whitelist_core_tool(
                output_file=file,
                secondary_whitelist=self.whitelist_list.name,
                use_official=False,
                processes=os.cpu_count(),
            ).filter(file=file, already_formatted=True, standard_sort=True)
            logging.info(
                "Finished to cleanup: %r",
                file,
            )

    @UpdaterBase.execute_if_authorized
    def start(self) -> "UpdaterBase":
        """
        Starts the update process.
        """

        if self.administration.raw_link:
            logging.info("Started to download: %r", self.administration.raw_link)
            DownloadHelper(self.administration.raw_link).download_text(
                destination=self.download_temp_file.name
            )

            logging.info("Finished to download: %r", self.administration.raw_link)

        self.download_temp_file.seek(0)

        logging.info("Started comparison of: %r", self.final_destination)
        kept, removed, new = self.produce_diff()
        logging.info("Finished comparison of: %r", self.final_destination)

        to_write = kept.copy()
        to_write.update(new)

        try:
            # Safety.
            to_write.remove(None)
        except KeyError:
            pass

        try:
            # Safety.
            to_write.remove("")
        except KeyError:
            pass

        logging.info("Started to update: %r", self.final_destination)

        FileHelper(self.final_destination).write(
            "\n".join(sorted(to_write)) + "\n", overwrite=True
        )

        logging.info("Finished to update: %r", self.final_destination)

        if removed:
            logging.info(
                "Started to write our temporary whitelist list into: %r",
                self.whitelist_list.name,
            )
            FileHelper(self.whitelist_list.name).write(
                "\n".join(removed) + "\n", overwrite=True
            )
            self.whitelist_list.seek(0)
            logging.info(
                "Finished to write our temporary whitelist list into: %r",
                self.whitelist_list.name,
            )

            self.remove_removed()
