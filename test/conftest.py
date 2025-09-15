""" Test Fixtures and Data Providers.
 - Selection of TreeScript: Basic, Nested, EmptyDirs.
 - TempPath FileTree Fixtures.
 Author: DK96-OS 2024 - 2025
"""
from pathlib import Path

import pytest


def get_basic_tree_script() -> str:
    return 'src/\n  data.txt'


def get_nested_tree_script() -> str:
    return 'src/\n  main/\n    SourceClass.java'


def get_empty_dirs_tree_script() -> str:
    return 'empty_dirs/\n  dir1/\n  dir2/\n  dir3/'


def get_hidden_tree_script() -> str:
    return """.github/
  dependabot.yml
  workflows/
    ci.yml
.hidden.txt
"""


@pytest.fixture
def mock_basic_tree(tmp_path):
    src_dir = tmp_path / 'src'
    src_dir.mkdir()
    (src_dir / 'data.txt').touch()
    return Path(str(tmp_path))


@pytest.fixture
def mock_nested_tree(tmp_path):
    src_dir = tmp_path / 'src'
    src_dir.mkdir()
    main_dir = src_dir / 'main'
    main_dir.mkdir()
    (main_dir / 'SourceClass.java').touch()
    return Path(str(tmp_path))


@pytest.fixture
def mock_empty_dirs_tree(tmp_path):
    my_dirs = tmp_path / 'empty_dirs/'
    my_dirs.mkdir()
    for n in range(1, 4): # Create Numbered Empty Dirs
        (my_dirs / f'dir{n}').mkdir()
    return Path(str(tmp_path))


@pytest.fixture
def mock_hidden_tree(tmp_path):
    github_dir = tmp_path / '.github'
    github_dir.mkdir()
    (github_dir / 'dependabot.yml').touch()
    workflows_dir = github_dir / 'workflows'
    workflows_dir.mkdir()
    (workflows_dir / 'ci.yml').touch()
    (tmp_path / '.hidden.txt').touch()
    return Path(str(tmp_path))
