@startuml
!theme blueprint

entity "Argument Data" as ARGDATA {
	__ Fields __
	+ input_file_path_str: str
    + data_dir_path_str: str | None
    + is_reversed: bool
}

metaclass "Argument Parser" as ARGPARSE {
	__ Methods __
	+ parse_arguments(list[str])
	- validate_arguments(str, str, bool)
	- define_arguments()
}

class "Data Directory" as DATADIR {
	__ Fields __
	- _data_dir: Path
	__ Methods __
	+ validate_build(TreeData): Path | None
	+ validate_trim(TreeData): Path | None
	- search_label(str): Path
}

metaclass "File Validation" as FILEVAL {
	__ Methods __
	+ validate_input_file(str)
	+ validate_directory(str)
	+ get_file_extension(str)
}

entity "Input Data" as INDATA {
	__ Fields __
	+ tree_input: str
    + data_dir: DataDirectory | None
    + is_reversed: bool
	__ Methods __
	+ get_tree_data(): Generator[TreeData]
}

metaclass "Line Reader" as LINEREAD {
	__ Fields __
	SPACE_CHARS
	__ Methods __
	+ read_input_tree(str): Generator[TreeData]
	- process_line(str): TreeData
	- calculate_depth(str): int
}

metaclass "String Validation" as STRVAL {
	__ Methods __
	+ validate_name(str): bool
	+ validate_data_label(str): bool
	+ validate_dir_name(str): str | None
	- validate_slash_char(str):
	- filter_slash_chars(str): str | None
}

interface "System Inputs" as SYS

entity "Tree Data" as TREEDATA {
	__ Fields __
	+ line_number: int
	+ depth: int
    + is_dir: bool
    + name: str
    + data_label: str
}

SYS --> ARGPARSE : "processed by"

ARGPARSE --> ARGDATA : returns
ARGPARSE -right-> STRVAL : uses

ARGDATA --> FILEVAL : "processed by"

DATADIR --> INDATA

FILEVAL --> INDATA : returns
FILEVAL -right-> STRVAL : uses
FILEVAL -left-> DATADIR : validates

INDATA --> LINEREAD : uses
INDATA -right-> TREEDATA : "generates many"

@enduml
