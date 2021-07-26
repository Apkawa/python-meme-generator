import os

import pytest


@pytest.fixture(scope='session')
def image_diff_root(request):
    return os.path.join(request.config.rootdir, 'tests')


@pytest.fixture(scope='session')
def image_diff_threshold():
    return 0.05
