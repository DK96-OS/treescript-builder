"""File Tree Builder Main Startup Script.
"""


def main():
    """
    Validates Arguments, then runs File Tree Builder.
    """
    import sys
    from input import validate_input_arguments, read_input_instructions
    from tree.tree_worker import TreeWorker
    # Validate CL Arguments
    input_data = validate_input_arguments(sys.argv)
    # Use this Worker to execute Stateful Procedural Operations
    worker = TreeWorker(input_data.data_dir)
    # Is Builder or Reverse
    if input_data.is_reversed:
        for data in read_input_instructions(input_data.tree_input):
            if not worker.remove(data):
                raise Exception(
                    "Invalid Operation: name=" + data.name + ", depth=" + data.depth
                )
        worker.cleanup_path_stack()
    else:
        for data in read_input_instructions(input_data.tree_input):
            if not worker.build(data):
                raise Exception(
                    "Invalid Operation: name=" + data.name + ", depth=" + data.depth
                )


if __name__ == "__main__":
    main()
