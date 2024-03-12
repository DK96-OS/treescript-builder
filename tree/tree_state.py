"""Tree State.
    A Key component in Tree Validation for Build operations.
"""
from pathlib import Path
from sys import exit
from typing import Generator, Optional

from input.tree_data import TreeData
from tree.path_stack import PathStack


class TreeState:
    """
    Manages the State of the Tree during Validation.
    """

    def __init__(self):
        self._stack = PathStack()
        self._queue = []
        self._prev_line_number = 0

    def validate_tree_data(self, node: TreeData) -> int:
        """
        Ensure that the next TreeData is valid, relative to current state.
            Calculate the change in depth, occurring with this TreeData.

        Parameters:
        - node (TreeData): The next TreeData in the sequence to Validate.

        Returns:
        int - The difference between the TreeData depth and the TreeState depth.

        Raises:
        SystemExit - When the TreeData is invalid, relative to the current TreeState.
        """
        self._update_line_number(node.line_number)
        # Calculate the Change in Depth
        if node.depth < 0:
            exit("Invalid Depth Value")
        state_depth = self.get_current_depth()
        if state_depth == 0:
            state_depth = -1
        delta = node.depth - state_depth
        if delta > 1:
            exit(f"You have jumped {delta - 1} steps in the tree on line: {node.line_number}")
        return delta

    def get_current_depth(self) -> int:
        """
        Determine the Current Depth of the Tree.
            Includes Elements in both the Stack and the Queue.

        Returns:
        int - The total number of elements, combining stack and queue
        """
        return self._stack.get_depth() + len(self._queue)

    def get_current_path(self) -> Path:
        """
        Obtain the Current Path of the Tree.

        Returns:
        str - A Path equivalent to the current Tree State.
        """
        if len(self._queue) > 0:
        	self.process_queue()
        return Path(self._stack.join_stack())
    
    def add_to_queue(self, dir_name: str):
        """
        Add a directory to the Queue.

        Parameters:
        - dir_name (str): The name of the Directory to enqueue.
        """
        self._queue.append(dir_name)

    def add_to_stack(self, dir_name: str):
        """
        Add a directory to the Stack.
        
        Parameters:
        - dir_name (str): The name of the Directory.
        """
        self._stack.push(dir_name)

    def process_queue(self) -> Optional[Path]:
        """
        Process the Directories in the Queue.
            Adds all directories from the Queue to the Stack.

        Returns:
        Path (optional) - The whole Path from the Stack.
        """
        if len(self._queue) < 1:
            return None
        for element in self._queue:
            self._stack.push(element)
        self._queue.clear()
        # Return the new Path as a str
        return Path(self._stack.join_stack())

    def process_stack(self, depth: int) -> Generator[Path, None, None]:
        """
        Pop the Stack to the Desired Depth.

        Parameters:
        - depth (int): The depth to process the stack to.

        Returns:
        Generator[Path] - Provides a Path for each entry in the Stack.
        """
        if depth < 0:
            exit('Invalid Depth')
        while depth < self._stack.get_depth():
            yield self._stack.create_path(self._stack.pop())

    def reduce_depth(self, depth: int) -> bool: 
        """
        Pop an element from the stack.

        Parameters:
        - depth (int): The Depth to pop the Stack to.

        Returns:
        bool - Whether the depth reduction succeeded, ie. 0 or more elements popped.
        """
        return self._stack.reduce_depth(depth)

    def _update_line_number(self, line_number: int):
        """
        Validate the Line Number is always increasing.

        Parameters:
        - line_number (int): The line number from the next TreeData.

        Raises:
        SystemExit - When the Line Number does not increase.
        """
        if self._prev_line_number < line_number:
            self._prev_line_number = line_number
        else:
            exit("Invalid Tree Data Sequence")
