@startuml
!theme blueprint

metaclass "Tree Module" as INIT {
    __ Methods __
    + build_tree(InputData)
    - _process_input(InputData): tuple[InstructionData]
}

class "Instruction Data" as INSTRUCT {
    __ Fields __
    is_dir: bool
    path: Path
    data_path: Optional[Path]
}

metaclass "Tree Builder" as BUILDER {
    __ Methods __
    + build(tuple[InstructionData]): tuple[bool]
    - _build(InstructionData): bool
    - _create_file(Path, str): bool
    - _make_dir_exist(Path): bool
}

metaclass "Tree Trimmer" as TRIMMER {
    __ Methods __
    + trim(tuple[InstructionData]): tuple[bool]
    - _trim(InstructionData): bool
    - _extract_file(Path, Path): bool
    - _remove_dir(Path): bool
}

metaclass "Tree Validation" as TREEVAL {
    __ Methods __
    validate_tree(Generator[TreeData]): tuple[InstructionData]
    validate_with_data_dir(Generator[TreeData], DataDirectory): tuple[InstructionData]
}

INIT --> TREEVAL
TREEVAL --> INSTRUCT

INSTRUCT --> BUILDER
INSTRUCT --> TRIMMER


@enduml