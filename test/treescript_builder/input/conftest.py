""" Test Data Providers for Input Package Tests.
"""

NUMERICAL_CHARS = [chr(i) for i in range(48,57 + 1)]      # 10
UPPER_CASE_LETTERS = [chr(i) for i in range(65,90 + 1)]   # 26
LOWER_CASE_LETTERS = [chr(i) for i in range(97,122 + 1)]  # 26


def generate_basenames():
    """ A Generator of simple File basenames, built from simple character sets.
 - Letters
 - Numbers
 - Dashes
 - Underscores
    """
    yield from NUMERICAL_CHARS
    yield from UPPER_CASE_LETTERS
    yield from LOWER_CASE_LETTERS
    for uc_letter in UPPER_CASE_LETTERS:
        for lc_letter in LOWER_CASE_LETTERS:
            for num_char in NUMERICAL_CHARS:
                yield f"{uc_letter}{lc_letter}{num_char}"
                yield f"{uc_letter}{lc_letter}-{num_char}"
                yield f"{uc_letter}{lc_letter}_{num_char}"


def generate_filenames():
    """ A Generator of Filenames, based on the Basename Generator.
 - Adds File Extensions to each Basename yielded by generate_basenames method..
    """
    file_exts = ['.py', '.txt']
    for basename in generate_basenames():
        for f in file_exts:
            yield basename + f


def generate_invalid_data_label_chars():
    """ A Generator of Characters in the Invalid Range for Data Labels.
    """
    invalid_ranges = [
        (0,32),  # 33 == !
        (34,47), # Numbers
        (58,64), # Upper Case Latin
        (91,96), # Lower Case Latin
        (123,140), # The Rest...
    ]
    for ir in invalid_ranges:
        for x in range(ir[0], ir[1] + 1):
            yield chr(x)


class MockPathStat:
    def __init__(self, file_size: int = 400):
        self.st_mode = 2
        self.st_size = file_size
