import os
import importlib.util
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

    spec = importlib.util.find_spec("prophet.tests")
    if spec is None:
        print("Error: could not find module spec for prophet.tests")
        sys.exit(1)
    if spec.submodule_search_locations:
        tests_dir = os.fspath(next(iter(spec.submodule_search_locations)))
    elif spec.origin:
        tests_dir = os.path.dirname(os.fspath(spec.origin))
    else:
        print("Error: could not determine tests directory for prophet.tests")
        sys.exit(1)

    pytest_args = [tests_dir, "-vv"]
    
    # Workaround for pytest fixture discovery on Windows Python 3.10
    # pytest 8.4.2 has issues finding conftest.py when rootdir is set to build directory
    # Explicitly set rootdir to tests directory so conftest.py can be discovered
    if is_windows and py_major == 3 and py_minor == 10:
        pytest_args.insert(1, f"--rootdir={tests_dir}")
    
    print("Final pytest args:", pytest_args)

    # actually run the tests
    sys.exit(pytest.main(pytest_args))


if __name__ == "__main__":
    subprocess.run([sys.executable, "-m", "pip", "check"], check=False)
    go()
