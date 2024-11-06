# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023-2024 Anna <cyber@sysrq.in>
# No warranty

from pathlib import Path

import pytest

from gentle.generators.npm import NpmGenerator
from gentle.metadata import MetadataXML
from tests.utils import BaseTestGenerator


class TestNpmGenerator(BaseTestGenerator):
    generator_cls = NpmGenerator
    generator_data_dir = Path(__file__).parent

    @pytest.mark.parametrize("dirname", ["mkdocs-material"])
    def test_pkg(self, mxml: MetadataXML, dirname: str):
        self._test_pkg(mxml, dirname)
