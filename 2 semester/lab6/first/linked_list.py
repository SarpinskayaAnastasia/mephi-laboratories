class OnceNode:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        return f"{"{"}{str(self.data)}{"}"}"

    def __eq__(self, other):
        if isinstance(other, OnceNode):
            return self.data == other.data
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, OnceNode):
            return self.data != other.data
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, OnceNode):
            return self.data < other.data
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, OnceNode):
            return self.data > other.data
        return NotImplemented
