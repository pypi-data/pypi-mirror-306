# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023-2024 Anna <cyber@sysrq.in>
# No warranty

from pathlib import Path

import pytest

from gentle.generators.python.setuptools import SetuptoolsGenerator
from gentle.metadata import MetadataXML
from tests.utils import BaseTestGenerator


class TestSetuptoolsGenerator(BaseTestGenerator):
    generator_cls = SetuptoolsGenerator
    generator_data_dir = Path(__file__).parent

    @pytest.mark.parametrize("dirname", ["django"])
    def test_pkg(self, mxml: MetadataXML, dirname: str):
        self._test_pkg(mxml, dirname)
