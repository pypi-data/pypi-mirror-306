# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023-2024 Anna <cyber@sysrq.in>
# No warranty

from pathlib import Path

import pytest

from gentle.generators.python.pkg_info import PkgInfoGenerator
from gentle.metadata import MetadataXML
from tests.utils import BaseTestGenerator


class TestPkgInfoGenerator(BaseTestGenerator):
    generator_cls = PkgInfoGenerator
    generator_data_dir = Path(__file__).parent

    @pytest.mark.parametrize("dirname", ["mkdocs-material", "pkgcraft"])
    def test_pkg(self, mxml: MetadataXML, dirname: str):
        self._test_pkg(mxml, dirname)
