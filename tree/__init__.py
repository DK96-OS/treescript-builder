"""The Tree Module.
"""
from input import InputData
from tree.tree_worker import TreeWorker


def build_tree(input_data: InputData):
	"""
	Build The Tree as defined by the InputData.

	Parameters:
	- input_data (str): The InputData produced by the Input Module.
	"""
    # Use this Worker to execute Stateful Procedural Operations
    worker = TreeWorker(input_data.data_dir)
    # Is Builder or Reverse
    if input_data.is_reversed:
        for data in input_data.get_tree_data():
            if not worker.remove(data):
                raise Exception(
                    "Invalid Operation: name=" + data.name + ", depth=" + data.depth
                )
        worker.cleanup_path_stack()
    else:
        for data in input_data.get_tree_data():
            if not worker.build(data):
                raise Exception(
                    "Invalid Operation: name=" + data.name + ", depth=" + data.depth
                )
