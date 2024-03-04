"""File Tree Builder Main Startup Script.
"""


def main():
    """
    Validates Arguments, then runs File Tree Builder.
    """
    import sys
    from input import parse_arguments
    from tree import build_tree
    # Validate and Process Input
    build_tree(parse_arguments(sys.argv))
    

if __name__ == "__main__":
    main()
