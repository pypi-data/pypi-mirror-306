# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023-2024 Anna <cyber@sysrq.in>
# No warranty

from pathlib import Path

import pytest

from gentle.generators.cpan import CpanGenerator
from gentle.metadata import MetadataXML
from tests.utils import BaseTestGenerator


class TestCpanGeneratorJson(BaseTestGenerator):
    generator_cls = CpanGenerator
    generator_data_dir = Path(__file__).parent / "json"

    @pytest.mark.parametrize("dirname", ["URI"])
    def test_pkg(self, mxml: MetadataXML, dirname: str):
        self._test_pkg(mxml, dirname)


@pytest.mark.perl
class TestCpanGeneratorPerl(BaseTestGenerator):
    generator_cls = CpanGenerator
    generator_data_dir = Path(__file__).parent / "perl"

    @pytest.mark.parametrize("dirname", ["URI"])
    def test_pkg(self, mxml: MetadataXML, dirname: str):
        self._test_pkg(mxml, dirname)
