class Node:
    """Create entries from data to add into hash table."""
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node


class Data:
    """Create dictionary key and value for each data point."""
    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashTable:
    """Create hashtable"""
    def __init__(self, table_size):
        self.table_size = table_size
        self.hash_table = [None] * table_size

    def custom_hash(self, key):
        """Create custom key."""
        hash_value = 0
        for i in key:
            hash_value += ord(i)
            hash_value = (hash_value * ord(i)) % self.table_size
        return hash_value

    def add_key_value(self, key, value):
        """Add key/value pair to hash-map."""
        hashed_key = self.custom_hash(key)
        if not self.hash_table[hashed_key]:
            self.hash_table[hashed_key] = Node(Data(key, value), None)
        else:
            current = self.hash_table[hashed_key]
            while current.next_node:
                current = current.next_node
            current.next_node = Node(Data(key,value), None)

    def get_value(self, key):
        """Retrieve value using key."""
        hashed_key = self.custom_hash(key)
        if self.hash_table[hashed_key]:
            current = self.hash_table[hashed_key]
            if not current.next_node:
                return current.data.value
            while current.next_node:
                if key == current.data.key:
                    return current.data.value
                current = current.next_node
            if key == current.data.key:
                return current.data.value
        return None

    def print_table(self):
        """Print the hash_table."""
        print("{")
        for i, val in enumerate(self.hash_table):
            if val is not None:
                llist_string = ""
                node = val
                if node.next_node:
                    while node.next_node:
                        llist_string += (
                                str(node.data.key) + " : " + str(node.data.value) + " --> "
                        )
                        node = node.next_node
                    llist_string += (
                            str(node.data.key) + " : " + str(node.data.value) + " --> None"
                    )
                    print(f"    [{i}] {llist_string}")
                else:
                    print(f"    [{i}] {val.data.key} : {val.data.value}")
            else:
                print(f"    [{i}] {val}")
        print("}")


