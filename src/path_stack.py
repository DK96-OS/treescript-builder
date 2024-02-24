""" Path Stack Management.
"""
from pathlib import Path


class PathStack:
    """ A Stack of Directory names in a Path.
    """

    def __init__(self):
        # The Stack of Directories in the Path.
        self._stack = []

    def push(self, directory_name: str):
        """ Push a directory to the Path Stack.

        Parameters:
        - directory_name (str): The name of the next directory in the Path Stack.
        """
        self._stack.append(directory_name)

    def pop(self) -> str:
        """
        Pop the top of the Stack, and return the directory name.

        Returns:
        str : The String removed from the top of the Stack.
        """
        if len(self._stack) <= 0:
            return None
        return self._stack.pop()

    def join_stack(self) -> str:
        """
        Combines all elements in the path Stack to form the parent directory.

        Returns:
        String path representing the parent directory.
        """
        # Add each element in the path
        if len(self._stack) == 0:
            return "./"
        return "./" + "/".join(self._stack) + "/"

    def create_path(self, filename: str) -> Path:
        """
        Combines all Elements in the Stack and appends a File name.

        Parameters:
        - filename (str): The name of the file to append to the end of the path.

        Returns:
        str : The full path to the file.
        """
        if type(filename) is not str:
            return self.join_stack()
        return Path(self.join_stack() + filename)

    def reduce_depth(self, depth: int) -> bool:
        """
        Reduce the Depth of the Path Stack.
        Optionally, remove the directory if it is empty.

        Parameters:
        - depth (int): The depth to reduce the stack to.

        Returns:
        boolean : Whether the Reduction was successful, ie 1 or more Stack pops.
        """
        current_depth = self.get_depth()
        if current_depth < depth or depth < 0:
            return False
        if current_depth == depth:
            return True
        for _ in range(current_depth, depth, -1):
            self._stack.pop()
        return True

    def get_depth(self) -> int:
        """ Obtain the current Depth of the Stack.
        The state where the current directory is the path, ie: './' has a depth of 0.

        Returns:
        int : The number of elements in the Path Stack.
        """
        return len(self._stack)
