class Node:
    """Create entries from data to add into binary search tree."""
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    """Nodes arranged for easy sorting."""
    def __init__(self):
        self.root = None

    def _insert_recursive(self, data, node):
        """Insert a node in the binary search tree based on blog_id number."""
        if data["id"] < node.data["id"]:
            if not node.left:
                node.left = Node(data)
            else:
                self._insert_recursive(data, node.left)
        elif data["id"] > node.data["id"]:
            if not node.right:
                node.right = Node(data)
            else:
                self._insert_recursive(data, node.right)
        return

    def insert(self, data):
        """Insert new note at root or call helper method."""
        if not self.root:
            self.root = Node(data)
        else:
            self._insert_recursive(data, self.root)

    def _search_recursive(self, blog_post_id, node):
        """
        Search for the correct node in the binary search tree.
        Return node or False if not in tree.
        """
        blog_post_id = int(blog_post_id)
        if blog_post_id == node.data["id"]:
            return node.data

        if blog_post_id < node.data["id"] and node.left is not None:
            if blog_post_id == node.left.data["id"]:
                return node.left.data
            return self._search_recursive(blog_post_id, node.left)

        if blog_post_id > node.data["id"] and node.right is not None:
            if blog_post_id == node.right.data["id"]:
                return node.right.data
            return self._search_recursive(blog_post_id, node.right)
        return False

    def search(self, blog_post_id):
        """Search for post in binary tree."""
        blog_post_id = str(blog_post_id)
        if not self.root:
            return None
        return self._search_recursive(blog_post_id, self.root)

