class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def _height(self, node):
        if node is None:
            return 0
        return node.height

    def _balance(self, node):
        if node is None:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _fix_height(self, node):
        node.height = max(self._height(node.left), self._height(node.right)) + 1

    def _left_rotate(self, x):
        y = x.right
        t2 = y.left

        y.left = x
        x.right = t2

        self._fix_height(x)
        self._fix_height(y)

        return y

    def _right_rotate(self, y):
        x = y.left
        t2 = x.right

        x.right = y
        y.left = t2

        self._fix_height(y)
        self._fix_height(x)

        return x

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return AVLNode(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        self._fix_height(node)

        balance = self._balance(node)

        # Left Left Case
        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)

        # Right Right Case
        if balance < -1 and key > node.right.key:
            return self._left_rotate(node)

        # Left Right Case
        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Right Left Case
        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp

            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)

        if node is None:
            return node

        self._fix_height(node)

        balance = self._balance(node)

        # Left Left Case
        if balance > 1 and self._balance(node.left) >= 0:
            return self._right_rotate(node)

        # Left Right Case
        if balance > 1 and self._balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Right Right Case
        if balance < -1 and self._balance(node.right) <= 0:
            return self._left_rotate(node)

        # Right Left Case
        if balance < -1 and self._balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder_traversal(self):
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, node, result):
        if node is not None:
            self._inorder_traversal(node.left, result)
            result.append(node.key)
            self._inorder_traversal(node.right, result)


# Testing the AVL Tree implementation
avl_tree = AVLTree()
data = [10, 5, 15, 3, 7, 12, 17]

# Insertion
for num in data:
    avl_tree.insert(num)

# Traversal (inorder)
print("Inorder Traversal:", avl_tree.inorder_traversal())

# Deletion
avl_tree.delete(15)
print("After deleting 15, Inorder Traversal:", avl_tree.inorder_traversal())
