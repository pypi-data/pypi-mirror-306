import json

from allotropy.parser_factory import Vendor
from allotropy.testing.utils import from_file

# file_name = "appbio_quantstudio_example02.txt"
# file_name = "appbio_quantstudio_example04.txt"
# file_name = "appbio_quantstudio_example05.txt"
# file_name = "appbio_quantstudio_example06.txt"
# file_name = "appbio_quantstudio_example07.txt"
# file_name = "appbio_quantstudio_multiple_cal_doc_wells.txt"
# file_name = "appbio_quantstudio_minimal_test04.txt"
# file_name = "error_xls.xlsx"
# file_name = "new_error.xlsx"
# file_name = "appbio_quantstudio_designandanalysis_QS1_Standard_Curve_example01.xlsx"

# file_name = "absorbance/Kinetic_Analysis_Mean_Slope_and_Standard_Curve_tab.txt"

# file_name = "agilent_tapestation_analysis_example_01.xml"

file_name = "src/error_experiment_type.xlsx"
file_name = "tests/parsers/appbio_quantstudio_designandanalysis/testdata/appbio_quantstudio_designandanalysis_QS7Pro_Primary_Analysis_example2.xlsx"

test_filepath = (
    file_name
    # f"../tests/parsers/agilent_tapestation_analysis/testdata/{file_name}"
    # f"../tests/parsers/appbio_quantstudio/testdata/{file_name}"
    # f"../tests/parsers/agilent_gen5/testdata/{file_name}"
)
allotrope_dict = from_file(test_filepath, Vendor.APPBIO_QUANTSTUDIO_DESIGNANDANALYSIS)

print(json.dumps(allotrope_dict, indent=4, ensure_ascii=False))  # noqa: T201
