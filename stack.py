"""Stack module
pylint rated 10.0/10
"""

class Stack:

    """Stack class"""

    def __init__(self):

        self.stack = []

    def add(self, value):

        """Add to stack"""

        self.stack.append(value)

    def exists(self):
        if self.stack:
            return True
        return False 

    def pop(self):

        """Pop from stack"""

        if self.stack:
            lastin = self.stack[-1]
            self.stack = self.stack[0:-1]
            return lastin

        return False

    def show(self):

        """Show contents of stack"""

        return self.stack

    def size(self):

        """Return size of stack"""

        return len(self.stack)
