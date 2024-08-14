# BSD 3-Clause License; see https://github.com/scikit-hep/uproot5/blob/main/LICENSE

import sys
import pytest

@pytest.mark.skipif("emscripten" in sys.platform,
                    reason="only test on emscripten")
def test_http_wasm():
    url = "https://github.com/scikit-hep/scikit-hep-testdata/raw/main/src/skhep_testdata/data/DAOD_TRUTH3_RC2.root"
    with uproot.open(f"simplecache::{url}") as f:
        ntpl = f["RNT:CollectionTree"]
        a = ntpl.arrays()
