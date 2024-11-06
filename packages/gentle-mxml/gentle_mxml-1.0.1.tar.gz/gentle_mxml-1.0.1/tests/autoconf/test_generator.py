# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023-2024 Anna <cyber@sysrq.in>
# No warranty

from pathlib import Path

import pytest

from gentle.generators.autoconf import AutoconfGenerator
from gentle.metadata import MetadataXML
from tests.utils import BaseTestGenerator


class TestAutoconfGenerator(BaseTestGenerator):
    generator_cls = AutoconfGenerator
    generator_data_dir = Path(__file__).parent

    @pytest.mark.parametrize("dirname", ["autoconf", "libsecp256k1"])
    def test_pkg(self, mxml: MetadataXML, dirname: str):
        self._test_pkg(mxml, dirname)
