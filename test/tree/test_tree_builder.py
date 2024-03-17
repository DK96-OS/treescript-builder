"""Testing Tree Builder Methods.
"""
import pytest
from pathlib import Path

from tree.instruction_data import InstructionData
from tree.tree_builder import build


def test_build_one_directory_already_exists_returns_true():
	instructions = (
		InstructionData(True, Path('./src'), None),
	)
	with pytest.MonkeyPatch().context() as m:
		m.setattr(Path, 'exists', lambda _: True)
	assert build(instructions) == (True)


def test_build_one_directory_does_not_exist_succeeds_returns_true():
	instructions = (
		InstructionData(True, Path('./src'), None),
	)
	with pytest.MonkeyPatch().context() as m:
		m.setattr(Path, 'exists', lambda _: False) 
		m.setattr(Path, 'mkdir', lambda _: False)
		#
	assert build(instructions) == (True)


def test_build_one_directory_does_not_exist_fails_returns_false():
	instructions = (
		InstructionData(True, Path('./src'), None),
	)
	with pytest.MonkeyPatch().context() as m:
		m.setattr(Path, 'exists', lambda _: False) 
		def raise_error():
			raise IOError()
		m.setattr(Path, 'mkdir', raise_error)
		#
	assert build(instructions) == (False)


def test_build_one_file():
	instructions = (
		InstructionData(True, Path('./src'), None),
		InstructionData(False, Path('./src/data.txt'), None),
	)
	with pytest.MonkeyPatch().context() as m:
		m.setattr(Path, 'exists', lambda _: True)
	# todo: assert
