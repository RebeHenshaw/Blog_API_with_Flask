class Node:
    """Create a node for the linked-list."""
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

    def __repr__(self):
        return f"Node: {self.data} "


class LinkedList:
    """Create an instance of linked list."""
    def __init__(self):
        self.head = None
        self.last_node = None

    def print_ll(self):
        """Create visual representation of nodes in the list."""
        ll_string = ""
        node = self.head
        if not node:
            print(None)
        else:
            while node:
                ll_string += f"{(str(node.data))} -->"
                node = node.next_node
        ll_string += "None"
        print(ll_string)

    def insert_first(self, data):
        """Insert a node at the beginning of a list."""
        if not self.head:
            self.head = Node(data=data, next_node=None)
            self.last_node = self.head
        node = Node(data=data, next_node=self.head)
        self.head = node

    def insert_last(self, data):
        """Insert a node at the end of the list."""
        if not self.head:
            self.insert_first(data)
            return
        self.last_node.next_node = Node(data, None)
        self.last_node = self.last_node.next_node

    def to_list(self):
        """Convert linked list to a python list structure."""
        l = []
        if self.head is None:
            return l

        node = self.head
        while node:
            l.append(node.data)
            node = node.next_node
        return l

    def get_user_by_id(self, user_id):
        """Get user by user id."""
        current = self.head
        while current:
            if current.data["id"] == int(user_id):
                return current.data
            current = current.next_node
        return "User not found"

