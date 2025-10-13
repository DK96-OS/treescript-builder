"""Tree Generators used by Test Suites.
"""
from pathlib import Path
from tempfile import TemporaryDirectory


from treescript_builder.data.tree_data import TreeData
from treescript_builder.input.line_reader import read_input_tree


def generate_simple_tree():
    """ Simple Tree: a Directory and a File in that Directory.
    """
    yield TreeData(1, 0, True, 'src', '')
    yield TreeData(2, 1, False, 'data.txt', '')


def generate_gradle_module_tree():
    """ Tree Template: a Gradle Module for Java.
    """
    yield TreeData(1, 0, True, 'module1', '')
    yield TreeData(2, 1, False, 'build.gradle', '')
    yield TreeData(3, 1, True, 'src', '')
    yield TreeData(4, 2, True, 'main', '')
    yield TreeData(5, 3, True, 'java', '')
    yield TreeData(6, 2, True, 'test', '')
    yield TreeData(7, 3, True, 'java', '')


def generate_gradle_module_tree_with_data():
    """ Tree Template: a Gradle Module for Java, with the Gradle Build File.
    """
    yield TreeData(1, 0, True, 'module1', '')
    yield TreeData(2, 1, False, 'build.gradle', 'gbuild_module1')
    yield TreeData(3, 1, True, 'src', '')
    yield TreeData(4, 2, True, 'main', '')
    yield TreeData(5, 3, True, 'java', '')
    yield TreeData(6, 2, True, 'test', '')
    yield TreeData(7, 3, True, 'java', '')


def generate_python_package_tree():
    """ Tree Template: a Python Package
    """
    yield TreeData(1, 0, True, 'package_name', '')
    yield TreeData(2, 1, False, '__init__.py', '')
    yield TreeData(3, 1, False, 'internal_module.py', '')


def generate_complex_tree():
    """ Complex Tree: an example Gradle-Java project.
    """
    yield TreeData(1, 0, True, '.github', '')
    yield TreeData(2, 1, True, 'workflows', '')
    yield TreeData(3, 0, True, 'module1', '')
    yield TreeData(4, 1, False, 'build.gradle', '')
    yield TreeData(5, 1, True, 'src', '')
    yield TreeData(6, 2, True, 'main', '')
    yield TreeData(7, 3, True, 'java', '')
    yield TreeData(8, 4, True, 'com', '')
    yield TreeData(9, 5, True, 'example', '')
    yield TreeData(10, 6, False, 'Main.java', '')
    yield TreeData(11, 2, True, 'test', '')
    yield TreeData(12, 3, True, 'java', '')
    yield TreeData(13, 4, True, 'com', '')
    yield TreeData(14, 5, True, 'example', '')
    yield TreeData(15, 6, False, 'MainTest.java', '')
    yield TreeData(16, 0, False, 'README.md', '')
    yield TreeData(17, 0, False, 'build.gradle', '')
    yield TreeData(18, 0, False, 'settings.gradle', '')


def generate_invalid_tree_line_1():
    """ The First TreeData generated has a depth that is inconsistent with tree state.
    """
    return read_input_tree("  src/\n")


def generate_invalid_tree_line_2():
    """ The Second TreeData generated has a depth that is inconsistent with tree state.
    """
    return read_input_tree("src/\n    data.txt")


def sample_treescript_1() -> str:
    return "build/\n  empty.txt\n  sample.tree SampleTree.tree\n"


def sample_treescript_2() -> str:
    return "build/\n  empty.txt\n  sample.tree SampleTree.tree\n\n\n" + "builder/\n  file.txt\n"


def sample_treescript_2_crlf() -> str:
    return "build/\r\n  empty.txt\r\n  sample.tree SampleTree.tree\r\n\r\n\r\n" + "builder/\r\n  file.txt\r\n"


def sample_treedata_1() -> list[TreeData]:
    return [
        TreeData(1, 0, True, "build"),
        TreeData(2, 1, False, "empty.txt"),
        TreeData(3, 1, False, "sample.tree", "SampleTree.tree"),
    ]

def sample_treedata_2() -> list[TreeData]:
    return [
        TreeData(1, 0, True, "build"),
        TreeData(2, 1, False, "empty.txt"),
        TreeData(3, 1, False, "sample.tree", "SampleTree.tree"),
        TreeData(6, 0, True, "builder"),
        TreeData(7, 1, False, "file.txt"),
    ]


def get_test_dir_with_sample1() -> TemporaryDirectory:
    """ Creates a TempDir containing a data directory with two files.
     - The empty.txt file contains nothing.
     - The sample.tree file contains TreeScript for the TempDir.
    """
    t = TemporaryDirectory()
    data_dir = Path(t.name) / "data"
    data_dir.mkdir()
    # Empty File
    (data_dir / "empty.txt").touch()
    # TreeScript Sample File
    (sample_tree := (data_dir / "sample.tree")).touch()
    sample_tree.write_text(sample_treescript_1())
    return t