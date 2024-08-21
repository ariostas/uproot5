# BSD 3-Clause License; see https://github.com/scikit-hep/uproot5/blob/main/LICENSE

import pathlib
import pytest
import shutil
import skhep_testdata

from functools import wraps

try:
    from pytest_pyodide import run_in_pyodide
    from pytest_pyodide.decorator import copy_files_to_pyodide
except ImportError:
    pytest.skip("Pyodide is not available", allow_module_level=True)

# copy skhep_testdata files to current directory (needed for @copy_files_to_pyodide)
def ensure_testdata(filename):
    if not pathlib.Path(filename).is_file():
        filepath = skhep_testdata.data_path(filename)
        shutil.copyfile(filepath, filename)


def wrap_test_for_pyodide(test_file=None):
    def decorator(test_func):
        @wraps(test_func)
        def wrapper(selenium):
            if test_file is not None:
                ensure_testdata(test_file)
            @copy_files_to_pyodide(file_list=[("dist","dist")] + ([] if test_file is None else [(test_file, test_file)]), install_wheels=True)
            def inner_func(selenium):
                run_in_pyodide()(test_func)(selenium)
            return inner_func(selenium)
        return wrapper
    return decorator