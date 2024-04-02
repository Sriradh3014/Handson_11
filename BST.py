class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, val):
        self.root = self._insert_recursive(self.root, val)

    def _insert_recursive(self, node, val):
        if not node:
            return TreeNode(val)
        if val < node.val:
            node.left = self._insert_recursive(node.left, val)
        elif val > node.val:
            node.right = self._insert_recursive(node.right, val)
        return node

    def delete(self, val):
        self.root = self._delete_recursive(self.root, val)

    def _delete_recursive(self, node, val):
        if not node:
            return node

        if val < node.val:
            node.left = self._delete_recursive(node.left, val)
        elif val > node.val:
            node.right = self._delete_recursive(node.right, val)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            min_node = self._find_min(node.right)
            node.val = min_node.val
            node.right = self._delete_recursive(node.right, min_node.val)
        return node

    def _find_min(self, node):
        while node.left:
            node = node.left
        return node

    def search(self, val):
        return self._search_recursive(self.root, val)

    def _search_recursive(self, node, val):
        if not node:
            return False
        if node.val == val:
            return True
        elif val < node.val:
            return self._search_recursive(node.left, val)
        else:
            return self._search_recursive(node.right, val)

    def inorder_traversal(self):
        result = []
        self._inorder_traversal_recursive(self.root, result)
        return result

    def _inorder_traversal_recursive(self, node, result):
        if node:
            self._inorder_traversal_recursive(node.left, result)
            result.append(node.val)
            self._inorder_traversal_recursive(node.right, result)

# Testing the implementation
bst = BST()
data = [10, 5, 15, 3, 7, 12, 17]

# Insertion
for num in data:
    bst.insert(num)

# Traversal (inorder)
print("Inorder Traversal:", bst.inorder_traversal())

# Searching
print("Is 7 present in the BST?", bst.search(7))
print("Is 20 present in the BST?", bst.search(20))

# Deletion
bst.delete(10)
print("After deleting 10, Inorder Traversal:", bst.inorder_traversal())
