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
import os
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from test.conftest import DATA_TREE_TARGET_DIR_INSTRUCT, DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA, \
	DATA_TREE_TARGET_FILE_INSTRUCT_WITH_DATA, DATA_TREE_TARGET_FILE_NAME, create_data_tree, DATA_TREE_TARGET_DIR_NAME, \
	DATA_TREE_TARGET_FILE_CONTENTS, DATA_TREE_DATA_FILE_CONTENTS, DATA_TREE_DATA_DIR_NAME, DATA_TREE_DATA_FILE_NAME, \
	input_data_with_dir
from test.treescript_builder.conftest import raise_exception, get_control_mode_write, get_control_mode_text_merge
from test.treescript_builder.tree.conftest import get_test_dir_with_sample1, sample_treescript_1
from treescript_builder.data.control_modes import WriteControlModes, TextMergeControlModes
from treescript_builder.data.instruction_data import InstructionData
from treescript_builder.operations import path_operations
from treescript_builder.operations.file_operations import build, _get_path_method, _trim_files
from treescript_builder.tree import validate_tree


def test_get_path_method_():
	assert _get_path_method(WriteControlModes(), False, False) == path_operations._try_copy


def test_get_path_method_move_files_():
	assert _get_path_method(WriteControlModes(), True, False) == path_operations._try_move


def test_get_path_method_overwrite_():
	assert _get_path_method(WriteControlModes(overwrite=True), False, False) == path_operations._ow_copy


def test_get_path_method_overwrite_move_files_():
	assert _get_path_method(WriteControlModes(overwrite=True), True, False) == path_operations._ow_move


def test_get_path_method_overwrite_exact_():
	assert _get_path_method(WriteControlModes(overwrite=True, exact_build=True), False, False) == path_operations._ow_exact_copy


def test_get_path_method_overwrite_exact_move_files_():
	assert _get_path_method(WriteControlModes(overwrite=True, exact_build=True), True, False) == path_operations._ow_exact_move


def test_get_path_method_prepend():
	assert _get_path_method(TextMergeControlModes(prepend_merge=True), False, False) == path_operations._prepend_copy


def test_get_path_method_prepend_move_files_():
	assert _get_path_method(TextMergeControlModes(prepend_merge=True), True, False) == path_operations._prepend_move


def test_get_path_method_append():
	assert _get_path_method(TextMergeControlModes(prepend_merge=False), False, False) == path_operations._append_copy


def test_get_path_method_append_move_files_():
	assert _get_path_method(TextMergeControlModes(prepend_merge=False), True, False) == path_operations._append_move


def test_build_one_directory_already_exists_returns_true(control_overwrite):
	test_instructions = (
		InstructionData(True, Path('./src'), None),
	)
	with pytest.MonkeyPatch().context() as m:
		m.setattr(Path, 'exists', lambda _: True)
		assert build(test_instructions, False, False, control_overwrite) == (True,)


def test_build_one_directory_does_not_exist_succeeds_returns_true(control_overwrite):
	test_instructions = (
		InstructionData(True, Path('./src'), None),
	)
	with pytest.MonkeyPatch().context() as m:
		m.setattr(Path, 'exists', lambda _: False)
		m.setattr(Path, 'mkdir', MagicMock())
		assert build(test_instructions, False, False, control_overwrite) == (True,)


def test_build_one_directory_does_not_exist_fails_returns_false(control_overwrite):
	test_instructions = (
		InstructionData(True, Path('./src'), None),
	)
	with pytest.MonkeyPatch().context() as m:
		m.setattr(Path, 'exists', lambda _: False)
		m.setattr(Path, 'mkdir', lambda *args, **kwargs: raise_exception('ioerror'))
		assert build(test_instructions, False, False, control_overwrite) == (False,)


def test_build_one_file_does_not_exist_succeeds_returns_true(control_overwrite):
	test_instructions = (
		InstructionData(False, Path('./data.txt'), None),
	)
	with pytest.MonkeyPatch().context() as m:
		m.setattr(Path, 'exists', lambda _: False)
		m.setattr(Path, 'touch', lambda *args, **kwargs: None)
		assert build(test_instructions, False, False, control_overwrite) == (True,)


def test_build_one_file_already_exists_touch_returns_true(control_overwrite):
	test_instructions = (
		InstructionData(False, Path('./data.txt'), None),
	)
	with pytest.MonkeyPatch().context() as m:
		m.setattr(Path, 'exists', lambda _: True)
		assert build(test_instructions, False, False, control_overwrite) == (True,)


def test_build_file_from_data_dir_get_sample_copies_data(control_overwrite):
	test_dir = get_test_dir_with_sample1()
	# Define Instruction Targets
	target_path = (test_dir_path := Path(test_dir.name)) / "target.tree"
	data_dir_path = test_dir_path / "data" / "sample.tree"
	# Create InstructionData
	test_input = (InstructionData(False, target_path, data_dir_path),)
	# Execute
	assert build(test_input, False, False, control_overwrite)
	# Validate
	assert target_path.exists()
	assert len(target_path.read_text()) == len(sample_treescript_1())
	

def test_build_append_target_dir_succeeds_returns_true(temp_cwd, control_text_append):
	""" Target Dir Instruct --> Succeeds, returns true """
	create_data_tree(root_dir := Path(temp_cwd.name))
	test_instructions = (DATA_TREE_TARGET_DIR_INSTRUCT,)
	assert (True,) == build(test_instructions, False, False, control_text_append)
	# Target file is not modified.
	assert '' == (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()


def test_build_append_target_dir_fails_returns_false(temp_cwd, control_text_append):
	""" Target Dir Instruct --> Fails, returns false """
	create_data_tree(root_dir := Path(temp_cwd.name))
	test_instructions = (DATA_TREE_TARGET_DIR_INSTRUCT,)
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'stat', lambda _, **kwargs: raise_exception('oserror'))
		assert (False,) == build(test_instructions, False, False, control_text_append)
	# Target file is not modified.
	assert  '' == (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()


def test_build_append_empty_target_file_no_data_succeeds_returns_true(temp_cwd, control_text_append):
	""" Existing File is Empty, no instruction data -> Succeeds, returns true. """
	create_data_tree(root_dir := Path(temp_cwd.name))
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA,)
	assert (True,) == build(test_instructions, False, False, control_text_append)
	# Target file is not modified.
	assert '' == (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()


def test_build_append_empty_target_file_with_data_succeeds_returns_true(temp_cwd, control_text_append):
	""" Existing File is Empty, with instruction data -> Succeeds, returns true. """
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=False)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_WITH_DATA,)
	assert (True,) == build(test_instructions, False, False, control_text_append)
	# DataFile is not modified.
	assert DATA_TREE_DATA_FILE_CONTENTS == (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()


def test_build_append_existing_file_no_data_succeeds_returns_true(temp_cwd, control_text_append):
	""" Existing File contains data, no instruction data -> Succeeds, returns true. """
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=True)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA,)
	assert (True,) == build(test_instructions, False, False, control_text_append)
	# Target file is not modified.
	assert DATA_TREE_TARGET_FILE_CONTENTS == (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()


def test_build_append_existing_file_with_data_succeeds_returns_true(temp_cwd, control_text_append):
	""" Existing File contains data, with instruction data -> Succeeds, returns true. """
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=True)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_WITH_DATA,)
	assert (True,) == build(test_instructions, False, False, control_text_append)
	# Target file is not modified.
	result = (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()
	assert result == DATA_TREE_TARGET_FILE_CONTENTS + DATA_TREE_DATA_FILE_CONTENTS


def test_build_append_empty_target_file_no_data_fails_returns_false(temp_cwd, control_text_append):
	""" Existing File is Empty, no instruction data -> Fails, returns false. """
	create_data_tree(root_dir := Path(temp_cwd.name), False)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA,)
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'touch', lambda _, **kwargs: raise_exception('oserror'))
		assert (False,) == build(test_instructions, False, False, control_text_append)
	assert '' == (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()


def test_build_append_empty_target_file_with_data_fails_returns_false(temp_cwd, control_text_append):
	""" Existing File is Empty, with instruction data -> Fails, returns false. """
	create_data_tree(root_dir := Path(temp_cwd.name), False)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_WITH_DATA,)
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'read_text', lambda _: raise_exception('oserror'))
		assert (False,) == build(test_instructions, False, False, control_text_append)
	assert '' == (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()


def test_build_append_existing_target_file_no_data_fails_returns_false(temp_cwd, control_text_append):
	""" Existing File contains data, no instruction data -> Fails, returns false. """
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=True)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA,)
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'touch', lambda _, **kwargs: raise_exception('oserror'))
		assert (False,) == build(test_instructions, False, False, control_text_append)
	# Target file is not modified.
	assert DATA_TREE_TARGET_FILE_CONTENTS == (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()


def test_build_append_existing_file_fails_returns_false(temp_cwd, control_text_append):
	""" Existing File contains data, with instruction data -> Fails, returns false. """
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=True)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_WITH_DATA,)
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'read_text', lambda _: raise_exception('ioerror'))
		assert (False,) == build(test_instructions, False, False, control_text_append)
	assert DATA_TREE_TARGET_FILE_CONTENTS == (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()


def test_build_prepend_empty_target_file_no_data_succeeds_returns_true(temp_cwd, control_text_prepend):
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=False)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA,)
	assert (True,) == build(test_instructions, False, False, control_text_prepend)
	assert '' == (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()


def test_build_prepend_empty_target_file_with_data_succeeds_returns_true(temp_cwd, control_text_prepend):
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=False)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_WITH_DATA,)
	assert (True,) == build(test_instructions, False, False, control_text_prepend)
	assert DATA_TREE_DATA_FILE_CONTENTS == (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()


def test_build_prepend_exiting_target_file_no_data_succeeds_returns_true(temp_cwd, control_text_prepend):
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=True)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA,)
	assert (True,) == build(test_instructions,False, False, control_text_prepend)
	assert DATA_TREE_TARGET_FILE_CONTENTS == (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()


def test_build_prepend_existing_target_file_with_data_succeeds_returns_true(temp_cwd, control_text_prepend):
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=True)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_WITH_DATA,)
	assert (True,) == build(test_instructions, False, False, control_text_prepend)
	result = (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()
	assert result == DATA_TREE_DATA_FILE_CONTENTS + DATA_TREE_TARGET_FILE_CONTENTS


def test_build_prepend_empty_target_file_no_data_fails_returns_false(temp_cwd, control_text_prepend):
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=False)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA,)
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'touch', lambda _, **kwargs: raise_exception('oserror'))
		assert (False,) == build(test_instructions, False, False, control_text_prepend)
	# Target file is not modified.
	assert '' == (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()


def test_build_prepend_empty_target_file_with_data_fails_returns_false(temp_cwd, control_text_prepend):
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=False)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_WITH_DATA,)
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'read_text', lambda _: raise_exception('oserror'))
		assert (False,) == build(test_instructions, False, False, control_text_prepend)
	# Target file is not modified.
	assert '' == (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()


def test_build_prepend_existing_target_file_no_data_fails_returns_false(temp_cwd, control_text_prepend):
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=True)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA,)
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'touch', lambda _, **kwargs: raise_exception('oserror'))
		assert (False,) == build(test_instructions, False, False, control_text_prepend)
	# Target file is not modified.
	assert DATA_TREE_TARGET_FILE_CONTENTS == (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()


def test_build_prepend_existing_target_file_with_data_fails_returns_false(temp_cwd, control_text_prepend):
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=True)
	test_instructions = (DATA_TREE_TARGET_FILE_INSTRUCT_WITH_DATA,)
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'read_text', lambda _: raise_exception('oserror'))
		assert (False,) == build(test_instructions, False, False, control_text_prepend)
	# Target file is not modified.
	assert DATA_TREE_TARGET_FILE_CONTENTS == (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()


def test_trim_src_dir_returns_true(control_overwrite):
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'rmdir', lambda _: True)
		i = (InstructionData(True, Path('src/'), None), )
		assert (True,) == _trim_files(False, control_overwrite, i)


def test_trim_file_returns_true(control_overwrite):
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'unlink', lambda _, **kwargs: True)
		i = (InstructionData(False, Path('data.txt'), None), )
		assert (True,) == _trim_files(False, control_overwrite, i)


def test_trim_file_error_returns_false(control_overwrite):
	with pytest.MonkeyPatch().context() as c:
		c.setattr(Path, 'unlink', lambda _: raise_exception('ioerror'))
		i = (InstructionData(True, Path('data.txt'), None), )
		assert (False,) == _trim_files(False, control_overwrite, i)


def test_trim_files_(temp_cwd, control_text_append):
	create_data_tree(root_dir := Path(temp_cwd.name), initial_target_content=True)
	assert (True,) == _trim_files(
		instructions=(DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA,),
		move_files=False,
		control_mode=control_text_append,
	)
	# Target file is not modified.
	assert DATA_TREE_TARGET_FILE_CONTENTS == (root_dir / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()


@pytest.mark.parametrize(
	'control_mode, expect_file_contents', [
		(get_control_mode_write(), DATA_TREE_TARGET_FILE_CONTENTS),
		(get_control_mode_write(overwrite=True), DATA_TREE_TARGET_FILE_CONTENTS),
		(get_control_mode_write(overwrite=True, exact=True), DATA_TREE_TARGET_FILE_CONTENTS),
		# Text Merges
		(get_control_mode_text_merge(is_prepend=False), DATA_TREE_TARGET_FILE_CONTENTS),
		(get_control_mode_text_merge(is_prepend=True), DATA_TREE_TARGET_FILE_CONTENTS),
	]
)
def test_trim_files_tempdir_data_tree_with_data_copy_files(control_mode, expect_file_contents):
	input_data, temp_dir = input_data_with_dir('data_tree', DATA_TREE_DATA_DIR_NAME, control_mode, move_files=False, is_trim=True)
	os.chdir(tempdir_path := Path(temp_dir.name))
	(target_dir := tempdir_path / DATA_TREE_TARGET_DIR_NAME).mkdir()
	(target_file := target_dir / DATA_TREE_TARGET_FILE_NAME).touch()
	target_file.write_text(DATA_TREE_TARGET_FILE_CONTENTS)
	#
	assert (True,) == _trim_files(
		move_files=False,
		control_mode=control_mode,
		instructions=validate_tree(input_data),
	)
	# TargetFiles are only modified by move operations.
	target_file_path = target_dir / DATA_TREE_TARGET_FILE_NAME
	assert expect_file_contents == target_file_path.read_text()
	# DataDir File contents.
	data_file_path = Path(temp_dir.name) / DATA_TREE_DATA_DIR_NAME / DATA_TREE_DATA_FILE_NAME
	assert expect_file_contents == data_file_path.read_text()


@pytest.mark.parametrize(
	'control_mode,v', [
		(get_control_mode_write(),1),
		(get_control_mode_write(overwrite=True),1),
		(get_control_mode_write(overwrite=True, exact=True),1),
		# Text Merges
		(get_control_mode_text_merge(is_prepend=False),1),
		(get_control_mode_text_merge(is_prepend=True),1),
	]
)
def test_trim_files_tempdir_data_tree_with_data_move_files_succeeds_returns_true(control_mode,v):
	input_data, temp_dir = input_data_with_dir('data_tree', DATA_TREE_DATA_DIR_NAME, control_mode, move_files=True, is_trim=True)
	os.chdir(tdir_path := Path(temp_dir.name))
	(target_dir := tdir_path / DATA_TREE_TARGET_DIR_NAME).mkdir()
	(target_file := target_dir / DATA_TREE_TARGET_FILE_NAME).touch()
	target_file.write_text(DATA_TREE_TARGET_FILE_CONTENTS)
	assert (True,) == _trim_files(
		move_files=True,
		control_mode=control_mode,
		instructions=validate_tree(input_data),
	)
	# TargetFiles are only modified by move operations.
	target_file_path = tdir_path / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME
	assert not target_file_path.exists()
	# DataDir File contents.
	data_file_path = tdir_path / DATA_TREE_DATA_DIR_NAME / DATA_TREE_DATA_FILE_NAME
	assert DATA_TREE_TARGET_FILE_CONTENTS == data_file_path.read_text()


@pytest.mark.parametrize(
	'control_mode,', [
		get_control_mode_text_merge(False),
		get_control_mode_text_merge(True),
	]
)
def test_trim_files_text_merge_tempdir_data_tree_with_data_copy_files_succeeds_returns_true(control_mode,):
	input_data, temp_data_dir = input_data_with_dir('data_tree', DATA_TREE_DATA_DIR_NAME, control_mode, False, True,)
	os.chdir(test_path := Path(temp_data_dir.name))
	(target_dir := test_path / DATA_TREE_TARGET_DIR_NAME).mkdir()
	(target_file := target_dir / DATA_TREE_TARGET_FILE_NAME).touch()
	target_file.write_text(DATA_TREE_TARGET_FILE_CONTENTS)
	#
	assert (True,) == _trim_files(
		move_files=False,
		control_mode=control_mode,
		instructions=validate_tree(input_data),
	)
	# Target Files were not modified.
	assert DATA_TREE_TARGET_FILE_CONTENTS == (test_path / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME).read_text()
	# DataDir contains Target File contents.
	assert DATA_TREE_TARGET_FILE_CONTENTS == (test_path / DATA_TREE_DATA_DIR_NAME / DATA_TREE_DATA_FILE_NAME).read_text()
