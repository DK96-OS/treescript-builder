"""Testing Tree Builder Methods.
"""
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from test.treescript_builder.tree.conftest import get_test_dir_with_sample1, sample_treescript_1
from treescript_builder.data.instruction_data import InstructionData
from treescript_builder.tree.tree_builder import build


def test_build_one_directory_already_exists_returns_true():
	with pytest.MonkeyPatch().context() as m:
		instructions = (
			InstructionData(True, Path('./src'), None),
		)
		m.setattr(Path, 'exists', lambda _: True)
		assert build(instructions) == (True,)


def test_build_one_directory_does_not_exist_succeeds_returns_true():
	with pytest.MonkeyPatch().context() as m:
		instructions = (
			InstructionData(True, Path('./src'), None),
		)
		m.setattr(Path, 'exists', lambda _: False)
		m.setattr(Path, 'mkdir', MagicMock())
		assert build(instructions) == (True,)


def test_build_one_directory_does_not_exist_fails_returns_false():
	instructions = (
		InstructionData(True, Path('./src'), None),
	)
	with pytest.MonkeyPatch().context() as m:
		m.setattr(Path, 'exists', lambda _: False)
		def raise_error():
			raise IOError()
		m.setattr(Path, 'mkdir', lambda *args, **kwargs: raise_error())
		assert build(instructions) == (False,)


def test_build_one_file_does_not_exist_succeeds_returns_true():
	with pytest.MonkeyPatch().context() as m:
		instructions = (
			InstructionData(False, Path('./data.txt'), None),
		)
		m.setattr(Path, 'exists', lambda _: False)
		m.setattr(Path, 'touch', lambda *args, **kwargs: None)
		assert build(instructions) == (True,)


def test_build_one_file_already_exists_touch_returns_true():
	with pytest.MonkeyPatch().context() as m:
		instructions = (
			InstructionData(False, Path('./data.txt'), None),
		)
		m.setattr(Path, 'exists', lambda _: True)
		assert build(instructions) == (True,)


def test_build_file_from_data_dir_get_sample_copies_data():
	test_dir = get_test_dir_with_sample1()
	# Define Instruction Targets
	target_path = (test_dir_path := Path(test_dir.name)) / "target.tree"
	data_dir_path = test_dir_path / "data" / "sample.tree"
	# Create InstructionData
	test_input = (InstructionData(False, target_path, data_dir_path),)
	# Execute
	assert build(test_input)
	# Validate
	assert target_path.exists()
	assert len(target_path.read_text()) == len(sample_treescript_1())