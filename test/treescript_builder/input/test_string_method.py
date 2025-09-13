from test.treescript_builder.input.conftest import generate_basenames, generate_filenames
from treescript_builder.input.string_validation import validate_data_label


def test_method():
    trials = 100
    for x in range(trials):
        for fn in generate_filenames():
            assert validate_data_label(fn)
