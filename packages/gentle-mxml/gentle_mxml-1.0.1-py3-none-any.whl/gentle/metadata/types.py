# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

"""
Types for working with Gentoo package metadata.
"""

from dataclasses import dataclass, field
from enum import Enum, auto

import lxml.etree as ET


class MaintainerStatus(Enum):
    """
    Maintainer status.
    """

    #: Not specified.
    NONE = auto()

    #: Active.
    ACTIVE = auto()

    #: Inactive.
    INACTIVE = auto()


@dataclass
class Person:
    """
    Representation of a person.
    """

    #: Maintainer name.
    name: str = field(default="", compare=False)

    #: Maintainer email.
    email: str = ""

    #: Maintainer activity status.
    status: MaintainerStatus = MaintainerStatus.NONE

    def __str__(self) -> str:
        if self.name and self.email:
            return f"{self.name} <{self.email}>"

        if self.email:
            return self.email

        return self.name

    def to_xml(self, attrib: dict | None = None) -> ET._Element:
        """
        Make an XML ``<maintainer>`` tag.

        :param attrib: attributes for the tag

        :return: :file:`metadata.xml` respresentation of a person
        """

        attrib = attrib or {}
        match self.status:
            case MaintainerStatus.ACTIVE:
                attrib["status"] = "active"
            case MaintainerStatus.INACTIVE:
                attrib["status"] = "inactive"

        result = ET.Element("maintainer", attrib=attrib)
        if self.name:
            name_elem = ET.SubElement(result, "name")
            name_elem.text = self.name
        if self.email:
            email_elem = ET.SubElement(result, "email")
            email_elem.text = self.email

        return result


@dataclass
class RemoteID:
    """
    Representation of a Remote ID.
    """

    #: Site name.
    attr: str

    #: Package identificator on the site.
    value: str

    def __str__(self) -> str:
        return f"{self.attr}:{self.value}"

    def to_xml(self) -> ET._Element:
        """
        Make an XML ``<remote-id>`` tag.

        :return: :file:`metadata.xml` respresentation of a remote id
        """

        remote_elem = ET.Element("remote-id", type=self.attr)
        remote_elem.text = self.value
        return remote_elem


@dataclass
class Upstream:
    """
    Representation of upstream metadata.
    """

    #: Upstream maintainers.
    maintainers: list[Person] = field(default_factory=list)

    #: Upstream changelog.
    changelog: str | None = None

    #: Upstream documentation.
    doc: str | None = None

    #: Upstream bug tracker.
    bugs_to: str | None = None

    #: Upstream identificators on third-party sites.
    remote_ids: list[RemoteID] = field(default_factory=list)
