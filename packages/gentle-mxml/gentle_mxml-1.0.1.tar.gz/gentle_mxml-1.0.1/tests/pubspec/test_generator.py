# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023-2024 Anna <cyber@sysrq.in>
# No warranty

from pathlib import Path

from gentle.generators.pubspec import PubspecGenerator
from tests.utils import BaseTestGenerator


class TestPubspecGenerator(BaseTestGenerator):
    generator_cls = PubspecGenerator
    generator_data_dir = Path(__file__).parent
