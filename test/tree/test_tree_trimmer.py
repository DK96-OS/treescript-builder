"""Testing Tree Trimming Methods.
"""
from pathlib import Path
import pytest

from tree.instruction_data import InstructionData
from tree.tree_trimmer import trim


def test_trim_src_dir_returns_true():
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'rmdir', lambda _: True)
		#
		i = (InstructionData(True, Path('src/'), None), )
		results = trim(i)
		assert results[0] == True
		assert len(results) == 1


def test_trim_file_returns_true():
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'unlink', lambda _, **kwargs: True)
		i = (InstructionData(False, Path('data.txt'), None), )
		results = trim(i)
		assert results[0] == True
		assert len(results) == 1
