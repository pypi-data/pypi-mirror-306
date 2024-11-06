# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023-2024 Anna <cyber@sysrq.in>
# No warranty

from pathlib import Path

import build
import pytest

from gentle.generators.python.wheel import WheelGenerator
from gentle.metadata import MetadataXML
from tests.utils import BaseTestGenerator


class TestWheelGenerator(BaseTestGenerator):
    generator_cls = WheelGenerator
    generator_data_dir = Path(__file__).parent

    @pytest.mark.parametrize("dirname", ["pyproject.toml", "setup.cfg", "setup.py"])
    def test_pkg_empty(self, monkeypatch: pytest.MonkeyPatch, mxml: MetadataXML, dirname: str):
        # subprocess calls can make this test fail
        def blackhole(*args, **kwargs):
            pass
        monkeypatch.setattr(build.env, "run_subprocess", blackhole)

        self._test_pkg_empty(mxml, "pkg_empty/" + dirname)

    @pytest.mark.net
    @pytest.mark.parametrize("dirname", ["rich", "commonmark"])
    def test_pkg(self, mxml: MetadataXML, dirname: str):
        self._test_pkg(mxml, dirname)
