"""Module for a class that temporarily
holds notes for transferring between notebooks.
pylint rated 10.0/10
"""

class TemporaryHolder:  #temporarily holds notes for transfering between notebooks

    """Class that temporarily holds notes for transferring between notebooks."""

    def __init__(self):

        self.holder = []

    def load(self, index, note):

        """Loads in note at index"""

        self.holder.append((index, note))

    def holding(self):

        """True if it contains notes."""

        if self.holder:
            return True
        return False

    def size(self):

        """Returns size."""

        return len(self.holder)

    def get(self):

        """Gets the first note"""

        if self.holder:
            p_temp = self.holder.pop(0)
            return p_temp
        return False
