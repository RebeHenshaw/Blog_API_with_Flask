class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node


class Queue:
    """Create entries from data to add into queue."""
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, data):
        """Replace tail with newly added node. Return nothing."""
        if self.head is None and self.tail is None:
            self.head = Node(data, None)
            self.tail = self.head
            return
        self.tail.next_node = Node(data, None)
        self.tail = self.tail.next_node
        return

    def dequeue(self):
        """Remove and return head from queue."""
        if not self.head:
            return None
        removed = self.head
        if self.head == self.tail:
            self.tail = None
        self.head = self.head.next_node
        return removed

