import os
import pkgutil
import platform
import sys
import subprocess

import pytest
from prophet import Prophet

try:
    import prophet.tests
except ImportError:
    print('Error: Unable to import prophet.tests')
    sys.exit(1)

def go():
    py_major = sys.version_info[0]
    py_minor = sys.version_info[1]
    py_impl = platform.python_implementation().lower()
    machine = platform.machine().lower()
    is_windows = platform.system().lower() == 'windows'

    print("Python implementation:", py_impl)
    print("              Machine:", machine)

    m = Prophet()
    print(f'Using backend: {m.stan_backend.get_type()}')

    loader = pkgutil.get_loader("prophet.tests")
    tests_dir = os.path.dirname(loader.path)
    
    # Workaround for pytest fixture discovery on Windows Python 3.10
    # pytest 8.4.2 has issues finding conftest.py in this specific combination
    # Add tests directory to Python path to help pytest discover conftest.py
    if is_windows and py_major == 3 and py_minor == 10:
        if tests_dir not in sys.path:
            sys.path.insert(0, tests_dir)
    
    pytest_args = [tests_dir, "-vv"]
    print("Final pytest args:", pytest_args)

    # actually run the tests
    sys.exit(pytest.main(pytest_args))


if __name__ == "__main__":
    subprocess.run(["pip", "check"])
    go()
