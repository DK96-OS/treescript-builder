@startuml
!theme blueprint

metaclass "Tree Validation" as TREEVAL {
    __ Methods __
    + validate_build(Generator[TreeData], Optional[DataDirectory]): tuple[InstructionData]
    + validate_trim(Generator[TreeData], Optional[DataDirectory]): tuple[InstructionData]
}

class "Tree State" as TREESTATE {
    __ Fields __
    - stack: PathStack
    - queue: list[str]
    - prev_line_number: int
    __ Methods __
    + validate_tree_data(TreeData): int
    + get_current_depth(): int
    + get_current_path(): Path
    + add_to_queue(str)
    + add_to_stack(str)
    + process_queue(): Optional[Path]
    + reduce_depth(int): bool
    - _update_line_number(int)
}

class "Instruction Data" as INSTRUCT {
    __ Fields __
    is_dir: bool
    path: Path
    data_path: Optional[Path]
}

class "Tree Data" as TREEDATA {
    __ Fields __
    line_number: int
    depth: int
    is_dir: bool
    name: str
    data_label: str
}

class "Path Stack" as PSTACK {
    __ Methods __
    + push(str)
    + pop(): str
    + join_stack(): str
    + create_path(str): Path
    + reduce_depth(int): bool
    + get_depth(): int
}

class "Data Directory" as DATADIR {
    __ Methods __
    + search_label(str): Optional[Path]
    + get_path(str): Path
}

TREEDATA -r-> TREEVAL

DATADIR -d-> TREEVAL

TREEVAL -r-> INSTRUCT

TREEVAL -d-> TREESTATE
TREEVAL -d-> PSTACK
TREESTATE -l-> PSTACK

@enduml
