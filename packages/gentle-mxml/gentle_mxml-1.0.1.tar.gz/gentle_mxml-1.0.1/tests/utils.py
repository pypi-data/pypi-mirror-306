# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023-2024 Anna <cyber@sysrq.in>
# No warranty

from copy import deepcopy
from pathlib import Path
from typing import Type

import pytest
from xmldiff.formatting import DiffFormatter
from xmldiff.main import diff_trees

from gentle.generators import AbstractGenerator
from gentle.metadata import MetadataXML


def compare_mxml(old: MetadataXML, new: MetadataXML) -> str:
    return diff_trees(old.xml, new.xml, formatter=DiffFormatter())


@pytest.mark.usefixtures("mxml")
class BaseTestGenerator:
    generator_cls: Type[AbstractGenerator]
    generator_data_dir: Path

    def test_pkg_none(self, mxml: MetadataXML):
        self._test_pkg_none(mxml, "pkg_none")

    def test_pkg_empty(self, mxml: MetadataXML):
        self._test_pkg_empty(mxml, "pkg_empty")

    def _test_pkg_none(self, mxml: MetadataXML, dirname: str):
        gen = self.generator_cls(self.generator_data_dir / dirname)
        assert not gen.active

    def _test_pkg_empty(self, mxml: MetadataXML, dirname: str):
        gen = self.generator_cls(self.generator_data_dir / dirname)
        assert gen.active

        mxml_old = deepcopy(mxml)
        gen.update_metadata_xml(mxml)
        assert compare_mxml(mxml_old, mxml) == ""

    def _test_pkg(self, mxml: MetadataXML, dirname: str):
        gen = self.generator_cls(self.generator_data_dir / dirname)
        assert gen.active

        gen.update_metadata_xml(mxml)
        with open(self.generator_data_dir / dirname / "metadata.xml") as file:
            assert mxml.dumps() == file.read().rstrip()

        mxml_prev = deepcopy(mxml)
        gen.update_metadata_xml(mxml)
        assert compare_mxml(mxml_prev, mxml) == ""
