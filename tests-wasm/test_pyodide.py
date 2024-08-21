# BSD 3-Clause License; see https://github.com/scikit-hep/uproot5/blob/main/LICENSE

try:
    from pytest_pyodide import run_in_pyodide
    from pytest_pyodide.decorator import copy_files_to_pyodide
    from utils import wrap_test_for_pyodide
except ImportError:
    pytest.skip("Pyodide is not available", allow_module_level=True)

from utils import ensure_testdata

# def test_schema_extension(selenium_standalone):
#     testfile = "test_ntuple_extension_columns.root"
#     ensure_testdata(testfile)

#     @copy_files_to_pyodide(file_list=[(testfile,testfile), ("dist","dist")], install_wheels=True)
#     @run_in_pyodide
#     def test_func(selenium_mock):
#         import uproot
#         with uproot.open("test_ntuple_extension_columns.root") as f:
#             obj = f["EventData"]

#             assert len(obj.column_records) > len(obj.header.column_records)
#             assert len(obj.column_records) == 936
#             assert obj.column_records[903].first_ele_index == 36

#             arrays = obj.arrays()

#             pbs = arrays[
#                 "HLT_AntiKt4EMPFlowJets_subresjesgscIS_ftf_TLAAux::fastDIPS20211215_pb"
#             ]
#             assert len(pbs) == 40
#             assert all(len(l) == 0 for l in pbs[:36])
#             assert next(i for i, l in enumerate(pbs) if len(l) != 0) == 36

#             jets = arrays["HLT_AntiKt4EMPFlowJets_subresjesgscIS_ftf_TLAAux:"]
#             assert len(jets.pt) == len(pbs)
    
#     test_func(selenium_standalone)


@wrap_test_for_pyodide(test_file="test_ntuple_extension_columns.root")
def test_schema_extension(selenium):
    import uproot
    with uproot.open("test_ntuple_extension_columns.root") as f:
        obj = f["EventData"]

        assert len(obj.column_records) > len(obj.header.column_records)
        assert len(obj.column_records) == 936
        assert obj.column_records[903].first_ele_index == 36

        arrays = obj.arrays()

        pbs = arrays[
            "HLT_AntiKt4EMPFlowJets_subresjesgscIS_ftf_TLAAux::fastDIPS20211215_pb"
        ]
        assert len(pbs) == 40
        assert all(len(l) == 0 for l in pbs[:36])
        assert next(i for i, l in enumerate(pbs) if len(l) != 0) == 36

        jets = arrays["HLT_AntiKt4EMPFlowJets_subresjesgscIS_ftf_TLAAux:"]
        assert len(jets.pt) == len(pbs)