# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

"""
Generic generator interface.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from gentle.metadata import MetadataXML


class AbstractGenerator(ABC):
    """
    Generic class for metadata generators.
    """

    @abstractmethod
    def __init__(self, srcdir: Path):
        """
        :param srcdir: path to unpacked sources
        """

    @abstractmethod
    def update_metadata_xml(self, mxml: MetadataXML) -> None:
        """
        Update metadata object in place.

        :param mxml: :file:`metadata.xml` object
        """

    @property
    @abstractmethod
    def active(self) -> bool:
        """
        Whether generator works.
        """

    @property
    def slow(self) -> bool:
        """
        Whether generator takes long time to finish.
        """

        return False
