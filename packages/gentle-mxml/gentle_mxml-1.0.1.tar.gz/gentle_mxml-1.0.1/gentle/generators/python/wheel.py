# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

"""
Metadata XML generator for Python PEP 517.

The following attributes are supported:

* Upstream maintainer(s)
* Upstream bug tracker
* Upstream changelog
* Upstream documentation
* Remote ID
"""

import logging
import shutil
from importlib.metadata import PathDistribution, PackageMetadata
from pathlib import Path
from tempfile import TemporaryDirectory

from gentle.generators import AbstractGenerator
from gentle.generators.python import (
    BUG_TRACKER_LABELS,
    CHANGELOG_LABELS,
    DOCS_LABELS,
    HOME_REPO_LABELS
)
from gentle.metadata import MetadataXML
from gentle.metadata.utils import extract_name_email, extract_remote_id

try:
    import pyproject_hooks
    from build import BuildException, BuildBackendException, ProjectBuilder
    from build.env import DefaultIsolatedEnv
    _HAS_BUILD = True
except ModuleNotFoundError:
    _HAS_BUILD = False

logger = logging.getLogger("wheel")


class WheelGenerator(AbstractGenerator):
    def __init__(self, srcdir: Path):
        self.srcdir = srcdir

        self.pyproject_toml = srcdir / "pyproject.toml"
        self.setup_cfg = srcdir / "setup.cfg"
        self.setup_py = srcdir / "setup.py"

        self.pkg_info = srcdir / "PKG-INFO"

    def project_wheel_metadata(self) -> PackageMetadata:
        with DefaultIsolatedEnv(installer="uv") as env:
            builder = ProjectBuilder.from_isolated_env(
                env, self.srcdir,
                runner=pyproject_hooks.quiet_subprocess_runner,
            )
            env.install(builder.build_system_requires)
            env.install(builder.get_requires_for_build("wheel"))
            with TemporaryDirectory(prefix="gentle-wheel-") as tmpdir:
                path = Path(builder.metadata_path(tmpdir))
                return PathDistribution(path).metadata

    # pylint: disable=too-many-branches
    def update_metadata_xml(self, mxml: MetadataXML) -> None:
        try:
            metadata: PackageMetadata = self.project_wheel_metadata()
        except (BuildException, BuildBackendException):
            return

        maint_key = "maintainer"
        if maint_key not in metadata:
            maint_key = "author"

        maint_email_key = "maintainer-email"
        if maint_email_key not in metadata:
            maint_email_key = "author-email"

        maintainers = []
        for key in (maint_key, maint_email_key):
            if key not in metadata:
                continue
            maintainers += [entry.strip() for entry in metadata[key].split(",")]

        for maint in map(extract_name_email, maintainers):
            if maint is None:
                continue
            logger.info("Found upstream maintainer: %s", maint)
            mxml.add_upstream_maintainer(maint)

        if (homepage := metadata.get("home-page")) is not None:  # type: ignore
            logger.info("Found homepage: %s", homepage)
            if (remote_id := extract_remote_id(homepage)) is not None:
                mxml.add_upstream_remote_id(remote_id)

        for entry in metadata.get_all("project-url", []):
            name, value = [item.strip()
                           for item in entry.split(",", maxsplit=1)]
            logger.info("Found %s: %s", name, value)
            if name.lower() in BUG_TRACKER_LABELS:
                mxml.set_upstream_bugs_to(value)
            elif name.lower() in CHANGELOG_LABELS:
                mxml.set_upstream_changelog(value)
            elif name.lower() in DOCS_LABELS:
                mxml.set_upstream_doc(value)
            elif name.lower() in HOME_REPO_LABELS:
                if (remote_id := extract_remote_id(value)) is not None:
                    mxml.add_upstream_remote_id(remote_id)

    @property
    def active(self) -> bool:
        return (
            _HAS_BUILD
            and not self.pkg_info.is_file()
            and shutil.which("uv") is not None
            and (
                self.pyproject_toml.is_file()
                or self.setup_cfg.is_file()
                or self.setup_py.is_file()
            )
        )

    @property
    def slow(self) -> bool:
        return True
