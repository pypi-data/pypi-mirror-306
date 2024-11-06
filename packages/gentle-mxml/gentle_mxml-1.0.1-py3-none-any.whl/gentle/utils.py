# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

"""
Utility functions and classes.
"""

import lxml.etree as ET


def stringify(element: ET._Element) -> str:
    """
    Extract all text from the given XML element.

    :param element: XML element object

    :returns: text from the given element
    """

    return "".join(
        (text for text in element.itertext() if isinstance(text, str))
    )
