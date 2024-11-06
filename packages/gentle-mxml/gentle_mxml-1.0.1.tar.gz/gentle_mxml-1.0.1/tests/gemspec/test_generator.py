# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023-2024 Anna <cyber@sysrq.in>
# No warranty

from pathlib import Path

import pytest

from gentle.generators.gemspec import GemspecGenerator
from gentle.metadata import MetadataXML
from tests.utils import BaseTestGenerator


class TestGemspecGeneratorYaml(BaseTestGenerator):
    generator_cls = GemspecGenerator
    generator_data_dir = Path(__file__).parent / "yaml"

    @pytest.mark.parametrize("dirname", ["rails"])
    def test_pkg(self, mxml: MetadataXML, dirname: str):
        self._test_pkg(mxml, dirname)


@pytest.mark.ruby
class TestGemspecGeneratorRuby(BaseTestGenerator):
    generator_cls = GemspecGenerator
    generator_data_dir = Path(__file__).parent / "ruby"

    @pytest.mark.parametrize("dirname", ["rubygems"])
    def test_pkg(self, mxml: MetadataXML, dirname: str):
        self._test_pkg(mxml, dirname)
