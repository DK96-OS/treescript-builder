""" Testing TreeScript-Builder Main Method.
 Author: DK96-OS 2024 - 2025
"""
import builtins
import os
import sys
from itertools import chain
from typing import Callable

import pytest

from test.conftest import TEST_INPUT_FILE, TEST_DATA_DIR, get_basic_tree_script, get_nested_tree_script, \
    get_empty_dirs_tree_script
from treescript_builder.__main__ import main


class PrintCollector:
    def __init__(self):
        self.collection: str = ''

    def get_output(self) -> str:
        return self.collection

    def append_print_output(self, output: str):
        self.collection = self.collection + output

    def assert_expected(self, expected: str):
        assert self.collection == expected

    def get_collector(self):
        def _collection(result, **kwargs):
            self.append_print_output(result)
            if (end_append := kwargs['end']) is not None:
                self.append_print_output(end_append)
        return _collection

    
def setup_mock_print_collector() -> tuple[PrintCollector, Callable[[str], None]]:
    return (collector := PrintCollector()), collector.get_collector()


def test_main_build_basic_tree(monkeypatch, tmp_path):
    sys.argv = ['treescript-builder', TEST_INPUT_FILE]
    os.chdir(tmp_path)
    #
    (input_file := tmp_path / TEST_INPUT_FILE).touch()
    input_file.write_text(get_basic_tree_script())
    #
    collector, mock_print = setup_mock_print_collector()
    monkeypatch.setattr(builtins, 'print', mock_print)
    main()
    collector.assert_expected('')
    item_list = sorted(map(lambda x: str(x), list(tmp_path.rglob('*'))))
    assert item_list[0].endswith(TEST_INPUT_FILE)
    assert item_list[1].endswith('src')
    assert item_list[2].endswith('src/data.txt')
    assert 3 == len(item_list)


def test_main_build_nested_tree(monkeypatch, tmp_path):
    sys.argv = ['treescript-builder', TEST_INPUT_FILE]
    os.chdir(tmp_path)
    #
    (input_file := tmp_path / TEST_INPUT_FILE).touch()
    input_file.write_text(get_nested_tree_script())
    #
    collector, mock_print = setup_mock_print_collector()
    monkeypatch.setattr(builtins, 'print', mock_print)
    main()
    collector.assert_expected('')
    item_list = sorted(map(lambda x: str(x), list(tmp_path.rglob('*'))))
    assert item_list[0].endswith(TEST_INPUT_FILE)
    assert item_list[1].endswith('src')
    assert item_list[2].endswith('src/main') or item_list[2].endswith('src\\main')
    assert item_list[3].endswith('src/main/SourceClass.java') or item_list[2].endswith('src\\main\\SourceClass.java')
    assert 4 == len(item_list)


def test_main_build_empty_dirs_tree(monkeypatch, tmp_path):
    sys.argv = ['treescript-builder', TEST_INPUT_FILE]
    os.chdir(tmp_path)
    #
    (input_file := tmp_path / TEST_INPUT_FILE).touch()
    input_file.write_text(get_empty_dirs_tree_script())
    #
    collector, mock_print = setup_mock_print_collector()
    monkeypatch.setattr(builtins, 'print', mock_print)
    main()
    collector.assert_expected('')
    item_list = sorted(map(lambda x: str(x), list(tmp_path.rglob('*'))))
    assert item_list[0].endswith('empty_dirs')
    assert item_list[1].endswith('empty_dirs/dir1') or item_list[1].endswith('empty_dirs\\dir1')
    assert item_list[2].endswith('empty_dirs/dir2') or item_list[2].endswith('empty_dirs\\dir2')
    assert item_list[3].endswith('empty_dirs/dir3') or item_list[3].endswith('empty_dirs\\dir3')
    assert item_list[4].endswith(TEST_INPUT_FILE)
    assert 5 == len(item_list)


def test_main_default_basic_tree(monkeypatch, mock_basic_tree):
    sys.argv = ['treescript-builder', TEST_INPUT_FILE]
    os.chdir(mock_basic_tree)
    collector, mock_print = setup_mock_print_collector()
    monkeypatch.setattr(builtins, 'print', mock_print)
    main()
    collector.assert_expected('')
    # BasicTree + TestInputFile = 2 + 1 = 3
    assert 3 == len(list(mock_basic_tree.rglob('*'))) 


def test_main_default_nested_tree(monkeypatch, mock_nested_tree):
    sys.argv = ['treescript-builder', TEST_INPUT_FILE]
    os.chdir(mock_nested_tree)
    collector, mock_print = setup_mock_print_collector()
    monkeypatch.setattr(builtins, 'print', mock_print)
    main()
    collector.assert_expected('')
    assert 4 == len(list(mock_nested_tree.rglob('*')))


def test_main_default_empty_dirs_tree(monkeypatch, mock_empty_dirs_tree):
    sys.argv = ['treescript-builder', TEST_INPUT_FILE]
    os.chdir(mock_empty_dirs_tree)
    collector, mock_print = setup_mock_print_collector()
    monkeypatch.setattr(builtins, 'print', mock_print)
    main()
    collector.assert_expected('')
    assert 5 == len(list(mock_empty_dirs_tree.rglob('*')))


def test_main_reverse_basic_tree(monkeypatch, mock_basic_tree):
    sys.argv = ['treescript-builder', TEST_INPUT_FILE, '--reverse',]
    os.chdir(mock_basic_tree)
    collector, mock_print = setup_mock_print_collector()
    monkeypatch.setattr(builtins, 'print', mock_print)
    main()
    collector.assert_expected('')
    assert 1 == len(list(mock_basic_tree.rglob('*')))


def test_main_trim_basic_tree(monkeypatch, mock_basic_tree):
    sys.argv = ['treescript-builder', TEST_INPUT_FILE, '--trim',]
    os.chdir(mock_basic_tree)
    collector, mock_print = setup_mock_print_collector()
    monkeypatch.setattr(builtins, 'print', mock_print)
    main()
    collector.assert_expected('')
    assert 1 == len(list(mock_basic_tree.rglob('*')))


def test_main_trim_nested_tree(monkeypatch, mock_nested_tree):
    sys.argv = ['treescript-builder', TEST_INPUT_FILE, '--trim',]
    os.chdir(mock_nested_tree)
    collector, mock_print = setup_mock_print_collector()
    monkeypatch.setattr(builtins, 'print', mock_print)
    main()
    collector.assert_expected('')
    assert 1 == len(list(mock_nested_tree.rglob('*')))


def test_main_trim_empty_dirs_tree(monkeypatch, mock_empty_dirs_tree):
    sys.argv = ['treescript-builder', TEST_INPUT_FILE, '--trim',]
    os.chdir(mock_empty_dirs_tree)
    collector, mock_print = setup_mock_print_collector()
    monkeypatch.setattr(builtins, 'print', mock_print)
    main()
    collector.assert_expected('')
    assert 1 == len(list(mock_empty_dirs_tree.rglob('*')))


def test_main_data_basic_tree_dir_does_not_exist_raises_exit(monkeypatch, mock_basic_tree):
    sys.argv = ['treescript-builder', TEST_INPUT_FILE, '--data', TEST_DATA_DIR,]
    os.chdir(mock_basic_tree)
    collector, mock_print = setup_mock_print_collector()
    monkeypatch.setattr(builtins, 'print', mock_print)
    with pytest.raises(SystemExit, match='The Directory does not exist.'):
        main()


def test_main_data_basic_tree(monkeypatch, mock_basic_tree):
    sys.argv = ['treescript-builder', TEST_INPUT_FILE, '--data', TEST_DATA_DIR,]
    os.chdir(mock_basic_tree)
    # Create the TEST_DATA_DIR
    (mock_basic_tree / TEST_DATA_DIR).mkdir()
    collector, mock_print = setup_mock_print_collector()
    monkeypatch.setattr(builtins, 'print', mock_print)
    main()
    collector.assert_expected('')


def test_main_data_nested_tree(monkeypatch, mock_nested_tree):
    sys.argv = ['treescript-builder', TEST_INPUT_FILE, '--data', TEST_DATA_DIR,]
    os.chdir(mock_nested_tree)
    (mock_nested_tree / TEST_DATA_DIR).mkdir()
    collector, mock_print = setup_mock_print_collector()
    monkeypatch.setattr(builtins, 'print', mock_print)
    main()
    collector.assert_expected('')


def test_main_data_empty_dirs_tree(monkeypatch, mock_empty_dirs_tree):
    sys.argv = ['treescript-builder', TEST_INPUT_FILE, '--data', TEST_DATA_DIR,]
    os.chdir(mock_empty_dirs_tree)
    (mock_empty_dirs_tree / TEST_DATA_DIR).mkdir()
    collector, mock_print = setup_mock_print_collector()
    monkeypatch.setattr(builtins, 'print', mock_print)
    main()
    collector.assert_expected('')


@pytest.mark.parametrize(
    'unrecognized_option_arg', [
        f'-{chr(letter)}' for letter in chain(
            range(65, 91),
            range(97, 114),
            # -r is valid
            range(115, 123),
        )
    ]
)
def test_main_unrecognized_option_basic_tree(unrecognized_option_arg, mock_basic_tree):
    sys.argv = ['treescript-builder', TEST_INPUT_FILE, unrecognized_option_arg ]
    os.chdir(mock_basic_tree)
    with pytest.raises(SystemExit, match="Unable to Parse Arguments."):
        main()


def test_main_reverse_option_basic_tree(monkeypatch, mock_basic_tree):
    sys.argv = ['treescript-builder', TEST_INPUT_FILE, '-r' ]
    os.chdir(mock_basic_tree)
    collector, mock_print = setup_mock_print_collector()
    monkeypatch.setattr(builtins, 'print', mock_print)
    main()
    collector.assert_expected('')
    assert 1 == len(list(mock_basic_tree.rglob('*')))
