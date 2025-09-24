""" Testing Tree Trimming Methods.
"""
from pathlib import Path
import pytest
import shutil

from treescript_builder.data.file_mode_enum import FileModeEnum
from treescript_builder.data.instruction_data import InstructionData
from treescript_builder.tree.tree_trimmer import trim


def mock_raise_ioerror(*args, **kwargs):
	raise IOError

def mock_raise_oserror(*args, **kwargs):
	raise OSError


def mock_move_method(src, dest):
	return True


mode = FileModeEnum.OVERWRITE


def test_trim_src_dir_returns_true():
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'rmdir', lambda _: True)
		i = (InstructionData(True, Path('src/'), None), )
		results = trim(i, mode)
		assert len(results) == 1
		assert results[0]


def test_trim_file_returns_true():
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'unlink', lambda _, **kwargs: True)
		i = (InstructionData(False, Path('data.txt'), None), )
		results = trim(i, mode)
		assert len(results) == 1
		assert results[0]


def test_trim_file_error_returns_false():
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'unlink', mock_raise_ioerror)
		i = (InstructionData(True, Path('data.txt'), None), )
		results = trim(i, mode)
		assert len(results) == 1
		assert not results[0]


def test_trim_file_with_data_label_returns_true():
	with pytest.MonkeyPatch().context() as c:
		c.setattr(shutil, 'move', mock_move_method)
		i = (InstructionData(False, Path('data.txt'), Path('data.csv')), )
		results = trim(i, mode)
		assert len(results) == 1
		assert results[0]