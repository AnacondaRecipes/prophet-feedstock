import os
import pkgutil
import platform
import sys

import pytest
from prophet import Prophet


def go():
    py_major = sys.version_info[0]
    py_impl = platform.python_implementation().lower()
    machine = platform.machine().lower()

    print("Python implementation:", py_impl)
    print("              Machine:", machine)

    m = Prophet()
    print(f'Using backend: {m.stan_backend.get_type()}')

    loader = pkgutil.get_loader("prophet.tests")
    pytest_args = [os.path.dirname(loader.path), "-vv"]
    print("Final pytest args:", pytest_args)

    # actually run the tests
    sys.exit(pytest.main(pytest_args))


if __name__ == "__main__":
    go()