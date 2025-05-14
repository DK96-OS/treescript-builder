"""Testing Tree Builder Methods.
"""
from unittest.mock import MagicMock
import pytest
from pathlib import Path

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