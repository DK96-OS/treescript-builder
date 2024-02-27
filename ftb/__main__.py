"""File Tree Builder
"""


def main():
    """Validates Arguments, then runs File Tree Builder."""
    import sys
    import input
    import src.input_line_reader
    from src.tree_worker import TreeWorker
    # Validate CL Arguments
    input_data = input.validate_input_arguments(sys.argv)
    # Process all Lines of text into procedural data
    procedural_data_sequence = src.input_line_reader.process_many_lines(input_data.tree_input)
    if len(procedural_data_sequence) < 1:
        raise SystemExit("Empty Procedure")
    # Use this Worker to execute Stateful Procedural Operations
    worker = TreeWorker(input_data.data_dir)
    # Process one line at a time
    for data in procedural_data_sequence:
        if not worker.build(data):
            raise Exception(
                "Invalid Operation: name=" + data.name + ", depth=" + data.depth
            )


if __name__ == "__main__":
    main()