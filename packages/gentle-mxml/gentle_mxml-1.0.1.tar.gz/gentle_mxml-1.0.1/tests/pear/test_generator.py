# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023-2024 Anna <cyber@sysrq.in>
# No warranty

from pathlib import Path

import pytest

from gentle.generators.pear import PearGenerator
from gentle.metadata import MetadataXML
from tests.utils import BaseTestGenerator


class TestPearGenerator(BaseTestGenerator):
    generator_cls = PearGenerator
    generator_data_dir = Path(__file__).parent

    @pytest.mark.parametrize("dirname", ["pear", "pecl-redis"])
    def test_pkg(self, mxml: MetadataXML, dirname: str):
        self._test_pkg(mxml, dirname)
