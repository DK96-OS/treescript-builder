"""Tree State.
    A Key component in Tree Validation for Build operations.
"""
from typing import Optional

from tree.path_stack import PathStack


class TreeState:
    """
    Manages the State of the Tree during Validation.
    """

    def __init__(self):
        self._stack = PathStack()
        self._queue = []

    def get_current_depth(self) -> int:
        """
        Determine the Current Depth of the Tree.
            Includes Elements in both the Stack and the Queue.

        Returns:
        int - The total number of elements, combining stack and queue
        """
        return self._stack.get_depth() + len(self._queue)

    def get_current_path(self) -> str:
        """
        Obtain the Current Path of the Tree.

        Returns:
        str - A Path equivalent to the current Tree State.
        """
        if len(self._queue) > 0:
            self.process_queue()
        return self._stack.join_stack()
    
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

    def process_queue(self) -> Optional[str]:
        """
        Process the Directories in the Queue.
            Adds all directories from the Queue to the Stack.

        Returns:
        str (optional) - The whole directory from the Stack.
        """
        if len(self._queue) < 1:
            return None
        for element in self._queue:
            self._stack.push(element)
        self._queue.clear()
        # Return the new Path as a str
        return self._stack.join_stack()

    def reduce_depth(self, depth: int) -> bool: 
        """
        Pop an element from the stack.

        Parameters:
        - depth (int): The Depth to pop the Stack to.

        Returns:
        str - The directory that was popped from the Stack.
        """
        return self._stack.reduce_depth(depth)
