import os
from pathlib import Path
from typing import Union

import pytest


@pytest.fixture(scope="session")
def image_diff_root(request):
    return os.path.join(request.config.rootdir, "tests")


@pytest.fixture(scope="session")
def image_diff_threshold():
    return 0.05


FIXTURE_ROOT = Path(__file__).parent / Path("tests/fixtures")


@pytest.fixture(scope="session")
def fixture_path():
    def _path(name: Union[Path, str]):
        return FIXTURE_ROOT / Path(name)

    return _path
