""" Testing Tree Builder Methods.
 - The primary Method in the TreeBuilder module is build.
 - The first build parameter is a tuple of Instructions.
 - The second build parameter is the FileMode Enum. (Default: Overwrite)
 
**Testing Overview:**
1. Building directories and files.
2. Nested directories and files.
3. Various file modes. (Does not affect Directories).

**Test Cases:**
1. Building directories and files.
 - Build One Directory.
   - Already Exists -> Succeeds, returns true.
   - Does Not Exist -> Succeeds, returns true.
   - Does Not Exist -> Fails, returns false.
 - Build One File. (In Overwrite Mode)
   - Already Exists -> Succeeds, returns true.
   - Does Not Exist -> Succeeds, returns true.
   - Does Not Exist -> Fails, returns false.
2. Nested directories and files. (In Overwrite Mode)
 - Build Two Directories, one nested inside the other.
   - Both Already exist -> Succeeds, returns true.
   - Inner Directory Does Not Exist -> Succeeds, returns true.
   - Inner Directory Does Not Exist -> Fails, returns false.
   - Neither Directory Exists -> Succeeds, returns true.
   - Neither Directory Exists -> Fails, returns false.
3. Various File Modes.
 - Append.
   - Existing File is Empty -> Succeeds, returns true.
   - Existing File contains data, no instruction data -> Succeeds, returns true.
   - Existing File contains data, with instruction data -> Succeeds, returns true.
   - Existing File is Empty -> Fails, returns false.
   - Existing File contains data, no instruction data -> Fails, returns false.
   - Existing File contains data, with instruction data -> Fails, returns false.
 - Prepend.
   - Existing File is Empty -> Succeeds, returns true.
   - Existing File contains data, no instruction data -> Succeeds, returns true.
   - Existing File contains data, with instruction data -> Succeeds, returns true.
   - Existing File is Empty -> Fails, returns false.
   - Existing File contains data, no instruction data -> Fails, returns false.
   - Existing File contains data, with instruction data -> Fails, returns false.
 - Overwrite.
   - Existing File is Empty -> Succeeds, returns true.
   - Existing File contains data, no instruction data -> Succeeds, returns true.
   - Existing File contains data, with instruction data -> Succeeds, returns true.
   - Existing File is Empty -> Fails, returns false.
   - Existing File contains data, no instruction data -> Fails, returns false.
   - Existing File contains data, with instruction data -> Fails, returns false.
"""
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from test.conftest import DATA_TREE_TARGET_DIR_INSTRUCT, DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA, \
	DATA_TREE_TARGET_FILE_INSTRUCT_WITH_DATA, DATA_TREE_TARGET_FILE_NAME, create_data_tree, DATA_TREE_TARGET_DIR_NAME, \
	DATA_TREE_TARGET_FILE_CONTENTS, DATA_TREE_DATA_FILE_CONTENTS
from test.treescript_builder.tree.conftest import get_test_dir_with_sample1, sample_treescript_1
from test.treescript_builder.tree.test_tree_trimmer import mock_raise_ioerror, mock_raise_oserror
from treescript_builder.data.file_mode_enum import FileModeEnum
from treescript_builder.data.instruction_data import InstructionData
from treescript_builder.tree.tree_builder import build


def test_build_one_directory_already_exists_returns_true():
	test_instructions = (
		InstructionData(True, Path('./src'), None),
	)
	mode = FileModeEnum.OVERWRITE
	with pytest.MonkeyPatch().context() as m:
		m.setattr(Path, 'exists', lambda _: True)
		assert build(test_instructions, mode) == (True,)


def test_build_one_directory_does_not_exist_succeeds_returns_true():
	test_instructions = (
		InstructionData(True, Path('./src'), None),
	)
	mode = FileModeEnum.OVERWRITE
	with pytest.MonkeyPatch().context() as m:
		m.setattr(Path, 'exists', lambda _: False)
		m.setattr(Path, 'mkdir', MagicMock())
		assert build(test_instructions, mode) == (True,)


def test_build_one_directory_does_not_exist_fails_returns_false():
	test_instructions = (
		InstructionData(True, Path('./src'), None),
	)
	mode = FileModeEnum.OVERWRITE
	with pytest.MonkeyPatch().context() as m:
		m.setattr(Path, 'exists', lambda _: False)
		def raise_error():
			raise IOError()
		m.setattr(Path, 'mkdir', lambda *args, **kwargs: raise_error())
		assert build(test_instructions, mode) == (False,)


def test_build_one_file_does_not_exist_succeeds_returns_true():
	test_instructions = (
		InstructionData(False, Path('./data.txt'), None),
	)
	mode = FileModeEnum.OVERWRITE
	with pytest.MonkeyPatch().context() as m:
		m.setattr(Path, 'exists', lambda _: False)
		m.setattr(Path, 'touch', lambda *args, **kwargs: None)
		assert build(test_instructions, mode) == (True,)


def test_build_one_file_already_exists_touch_returns_true():
	test_instructions = (
		InstructionData(False, Path('./data.txt'), None),
	)
	mode = FileModeEnum.OVERWRITE
	with pytest.MonkeyPatch().context() as m:
		m.setattr(Path, 'exists', lambda _: True)
		assert build(test_instructions, mode) == (True,)


def test_build_file_from_data_dir_get_sample_copies_data():
	test_dir = get_test_dir_with_sample1()
	mode = FileModeEnum.OVERWRITE
	# Define Instruction Targets
	target_path = (test_dir_path := Path(test_dir.name)) / "target.tree"
	data_dir_path = test_dir_path / "data" / "sample.tree"
	# Create InstructionData
	test_input = (InstructionData(False, target_path, data_dir_path),)
	# Execute
	assert build(test_input, mode)
	# Validate
	assert target_path.exists()
	assert len(target_path.read_text()) == len(sample_treescript_1())
	

def test_build_append_target_dir_succeeds_returns_true(temp_cwd):
	""" Target Dir Instruct --> Succeeds, returns true """
	create_data_tree(root_dir := Path(temp_cwd.name))
	test_instructions = (DATA_TREE_TARGET_DIR_INSTRUCT,)
	assert (True,) == build(test_instructions, FileModeEnum.APPEND)
	# Target file is not modified.
	result = (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()
	assert result == ''


def test_build_append_target_dir_fails_returns_false(temp_cwd):
	""" Target Dir Instruct --> Fails, returns false """
	create_data_tree(root_dir := Path(temp_cwd.name))
	test_instructions = (DATA_TREE_TARGET_DIR_INSTRUCT,)
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'stat', mock_raise_oserror)
		assert (False,) == build(test_instructions, FileModeEnum.APPEND)
	# Target file is not modified.
	result = (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()
	assert result == ''


def test_build_append_empty_target_file_no_data_succeeds_returns_true(temp_cwd):
	""" Existing File is Empty, no instruction data -> Succeeds, returns true. """
	create_data_tree(root_dir := Path(temp_cwd.name))
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA,)
	assert (True,) == build(test_instructions, FileModeEnum.APPEND)
	# Target file is not modified.
	result = (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()
	assert result == ''


def test_build_append_empty_target_file_with_data_succeeds_returns_true(temp_cwd):
	""" Existing File is Empty, with instruction data -> Succeeds, returns true. """
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=False)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_WITH_DATA,)
	assert (True,) == build(test_instructions, FileModeEnum.APPEND)
	# Target file is not modified.
	result = (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()
	assert result == DATA_TREE_DATA_FILE_CONTENTS


def test_build_append_existing_file_no_data_succeeds_returns_true(temp_cwd):
	""" Existing File contains data, no instruction data -> Succeeds, returns true. """
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=True)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA,)
	assert (True,) == build(test_instructions, FileModeEnum.APPEND)
	# Target file is not modified.
	result = (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()
	assert result == DATA_TREE_TARGET_FILE_CONTENTS


def test_build_append_existing_file_with_data_succeeds_returns_true(temp_cwd):
	""" Existing File contains data, with instruction data -> Succeeds, returns true. """
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=True)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_WITH_DATA,)
	assert (True,) == build(test_instructions, FileModeEnum.APPEND)
	# Target file is not modified.
	result = (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()
	assert result == DATA_TREE_TARGET_FILE_CONTENTS + DATA_TREE_DATA_FILE_CONTENTS


def test_build_append_empty_target_file_no_data_fails_returns_false(temp_cwd):
	""" Existing File is Empty, no instruction data -> Fails, returns false. """
	create_data_tree(root_dir := Path(temp_cwd.name), False)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA,)
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'touch', mock_raise_oserror)
		assert (False,) == build(test_instructions, FileModeEnum.APPEND)
	result = (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()
	assert result == ''


def test_build_append_empty_target_file_with_data_fails_returns_false(temp_cwd):
	""" Existing File is Empty, with instruction data -> Fails, returns false. """
	create_data_tree(root_dir := Path(temp_cwd.name), False)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_WITH_DATA,)
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'read_text', mock_raise_oserror)
		assert (False,) == build(test_instructions, FileModeEnum.APPEND)
	result = (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()
	assert result == ''


def test_build_append_existing_target_file_no_data_fails_returns_false(temp_cwd):
	""" Existing File contains data, no instruction data -> Fails, returns false. """
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=True)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA,)
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'touch', mock_raise_oserror)
		assert (False,) == build(test_instructions, FileModeEnum.APPEND)
	# Target file is not modified.
	result = (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()
	assert result == DATA_TREE_TARGET_FILE_CONTENTS


def test_build_append_existing_file_fails_returns_false(temp_cwd):
	""" Existing File contains data, with instruction data -> Fails, returns false. """
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=True)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_WITH_DATA,)
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'read_text', mock_raise_ioerror)
		assert (False,) == build(test_instructions, FileModeEnum.APPEND)
	result = (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()
	assert result == DATA_TREE_TARGET_FILE_CONTENTS


def test_build_prepend_empty_target_file_no_data_succeeds_returns_true(temp_cwd):
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=False)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA,)
	assert (True,) == build(test_instructions, FileModeEnum.PREPEND)
	result = (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()
	assert result == ''


def test_build_prepend_empty_target_file_with_data_succeeds_returns_true(temp_cwd):
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=False)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_WITH_DATA,)
	assert (True,) == build(test_instructions, FileModeEnum.PREPEND)
	result = (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()
	assert result == DATA_TREE_DATA_FILE_CONTENTS


def test_build_prepend_exiting_target_file_no_data_succeeds_returns_true(temp_cwd):
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=True)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA,)
	assert (True,) == build(test_instructions, FileModeEnum.PREPEND)
	result = (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()
	assert result == DATA_TREE_TARGET_FILE_CONTENTS


def test_build_prepend_existing_target_file_with_data_succeeds_returns_true(temp_cwd):
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=True)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_WITH_DATA,)
	assert (True,) == build(test_instructions, FileModeEnum.PREPEND)
	result = (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()
	assert result == DATA_TREE_DATA_FILE_CONTENTS + DATA_TREE_TARGET_FILE_CONTENTS


def test_build_prepend_empty_target_file_no_data_fails_returns_false(temp_cwd):
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=False)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA,)
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'touch', mock_raise_oserror)
		assert (False,) == build(test_instructions, FileModeEnum.PREPEND)
	# Target file is not modified.
	result = (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()
	assert result == ''


def test_build_prepend_empty_target_file_with_data_fails_returns_false(temp_cwd):
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=False)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_WITH_DATA,)
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'read_text', mock_raise_oserror)
		assert (False,) == build(test_instructions, FileModeEnum.PREPEND)
	# Target file is not modified.
	result = (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()
	assert result == ''


def test_build_prepend_existing_target_file_no_data_fails_returns_false(temp_cwd):
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=True)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA,)
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'touch', mock_raise_oserror)
		assert (False,) == build(test_instructions, FileModeEnum.PREPEND)
	# Target file is not modified.
	result = (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()
	assert result == DATA_TREE_TARGET_FILE_CONTENTS


def test_build_prepend_existing_target_file_with_data_fails_returns_false(temp_cwd):
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=True)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_WITH_DATA,)
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'read_text', mock_raise_oserror)
		assert (False,) == build(test_instructions, FileModeEnum.PREPEND)
	# Target file is not modified.
	result = (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()
	assert result == DATA_TREE_TARGET_FILE_CONTENTS
