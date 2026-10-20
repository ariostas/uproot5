# BSD 3-Clause License; see https://github.com/scikit-hep/uproot5/blob/main/LICENSE

import pytest
import skhep_testdata

import uproot

ak = pytest.importorskip("awkward")
pd = pytest.importorskip("pandas")
pytest.importorskip("pyarrow")
akimbo_pandas = pytest.importorskip("akimbo.pandas")
if not hasattr(akimbo_pandas, "to_pandas_array"):
    pytest.skip("akimbo without to_pandas_array", allow_module_level=True)


@pytest.fixture
def df():
    with uproot.open(skhep_testdata.data_path("uproot-HZZ.root"))["events"] as tree:
        yield tree.arrays(["Muon_Px", "NMuon"], library="pd")


def test_cells_are_awkward(df):
    px = df["Muon_Px"]
    assert px.dtype == "awkward"
    assert isinstance(px[0], ak.Array)
    assert str(px[0].type) == "2 * float32"
    assert (px[0] * 2).tolist() == pytest.approx([-105.79891, 75.47556])
    assert (px * 2)[0].tolist() == (px[0] * 2).tolist()
    assert df["NMuon"].dtype == "int32"


def test_types_are_kept():
    with uproot.open(skhep_testdata.data_path("uproot-HZZ-objects.root"))[
        "events"
    ] as tree:
        branch = tree["muonp4"]
        series = branch.array(library="pd", entry_stop=10)
        assert series.ak.array.type == branch.array(entry_stop=10).type
        assert "TLorentzVector" in str(series.iloc[0].type)

    with uproot.open(skhep_testdata.data_path("uproot-stl_containers.root"))[
        "tree"
    ] as tree:
        branch = tree["map_int32_int16"]
        series = branch.array(library="pd")
        assert series.ak.array.type == branch.array().type


def test_row_selections(df):
    selected = df[df["NMuon"] > 2]["Muon_Px"]
    assert str(selected.ak.array.type) == "42 * var * float32"
    assert df["Muon_Px"].reindex([0, -1]).ak.array.tolist()[1] is None


@pytest.mark.parametrize("how", ["dataframe", "dict", "extend", "rntuple"])
def test_write_back(tmp_path, df, how):
    filename = tmp_path / "out.root"
    with uproot.recreate(filename) as f:
        if how == "dataframe":
            f["t"] = df[["Muon_Px"]]
        elif how == "dict":
            f["t"] = {"Muon_Px": df["Muon_Px"]}
        elif how == "extend":
            f.mktree("t", {"Muon_Px": "var * float32"})
            f["t"].extend({"Muon_Px": df["Muon_Px"]})
        else:
            f.mkrntuple("t", {"Muon_Px": "var * float32"})
            f["t"].extend({"Muon_Px": df["Muon_Px"]})

    with uproot.open(filename) as f:
        out = f["t"]["Muon_Px"].array()
        assert str(out.type) == "2421 * var * float32"
        assert out.tolist() == df["Muon_Px"].tolist()


def test_parquet_round_trip(tmp_path, df):
    pytest.importorskip("pyarrow.parquet")
    df.to_parquet(tmp_path / "out.parquet")
    out = pd.read_parquet(tmp_path / "out.parquet")
    assert out["Muon_Px"].dtype == "awkward"
    assert isinstance(out["Muon_Px"][0], ak.Array)
    assert out["Muon_Px"].tolist() == df["Muon_Px"].tolist()
