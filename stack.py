class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

class Stack:
    def __init__(self):
        self.top = None

    def peek(self):
        return self.top

    def push(self, data):
        current_top = self.top
        new_top = Node(data, current_top)
        self.top = new_top

    def pop(self):
        if not self.top:
            return None
        removed = self.top
        self.top = self.top.next_node
        return removed
