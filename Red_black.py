class Node:
    def __init__(self, key, color='RED'):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.color = color


class RedBlackTree:
    def __init__(self):
        self.nil = Node(None, color='BLACK')  # Sentinel node
        self.root = self.nil

    def insert(self, key):
        new_node = Node(key)
        new_node.left = self.nil
        new_node.right = self.nil

        parent = None
        current = self.root

        while current != self.nil:
            parent = current
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent
        if parent is None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        new_node.color = 'RED'
        self._fix_insert(new_node)

    def _fix_insert(self, node):
        while node != self.root and node.parent.color == 'RED':
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == 'RED':
                    node.parent.color = 'BLACK'
                    uncle.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    self._right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.color == 'RED':
                    node.parent.color = 'BLACK'
                    uncle.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    self._left_rotate(node.parent.parent)

        self.root.color = 'BLACK'

    def _left_rotate(self, node):
        right_child = node.right
        node.right = right_child.left
        if right_child.left != self.nil:
            right_child.left.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left, node.parent, node.parent, right_child.parent = node, right_child, right_child, node

    def _right_rotate(self, node):
        left_child = node.left
        node.left = left_child.right
        if left_child.right != self.nil:
            left_child.right.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        left_child.right, node.parent, node.parent, left_child.parent = node, left_child, left_child, node

    def inorder_traversal(self):
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, node, result):
        if node != self.nil:
            self._inorder_traversal(node.left, result)
            result.append((node.key, node.color))
            self._inorder_traversal(node.right, result)

    def delete(self, key):
        node = self._search(key)
        if node == self.nil:
            return

        self._delete_node(node)

    def _delete_node(self, node):
        temp = node
        temp_original_color = temp.color

        if node.left == self.nil:
            x = node.right
            self._transplant(node, node.right)
        elif node.right == self.nil:
            x = node.left
            self._transplant(node, node.left)
        else:
            temp = self._tree_minimum(node.right)
            temp_original_color = temp.color
            x = temp.right
            if temp.parent == node:
                x.parent = temp
            else:
                self._transplant(temp, temp.right)
                temp.right = node.right
                temp.right.parent = temp

            self._transplant(node, temp)
            temp.left = node.left
            temp.left.parent = temp
            temp.color = node.color

        if temp_original_color == 'BLACK':
            self._delete_fixup(x)

    def _delete_fixup(self, node):
        while node != self.root and node.color == 'BLACK':
            if node == node.parent.left:
                sibling = node.parent.right
                if sibling.color == 'RED':
                    sibling.color = 'BLACK'
                    node.parent.color = 'RED'
                    self._left_rotate(node.parent)
                    sibling = node.parent.right
                if sibling.left.color == 'BLACK' and sibling.right.color == 'BLACK':
                    sibling.color = 'RED'
                    node = node.parent
                else:
                    if sibling.right.color == 'BLACK':
                        sibling.left.color = 'BLACK'
                        sibling.color = 'RED'
                        self._right_rotate(sibling)
                        sibling = node.parent.right
                    sibling.color = node.parent.color
                    node.parent.color = 'BLACK'
                    sibling.right.color = 'BLACK'
                    self._left_rotate(node.parent)
                    node = self.root
            else:
                sibling = node.parent.left
                if sibling.color == 'RED':
                    sibling.color = 'BLACK'
                    node.parent.color = 'RED'
                    self._right_rotate(node.parent)
                    sibling = node.parent.left
                if sibling.right.color == 'BLACK' and sibling.left.color == 'BLACK':
                    sibling.color = 'RED'
                    node = node.parent
                else:
                    if sibling.left.color == 'BLACK':
                        sibling.right.color = 'BLACK'
                        sibling.color = 'RED'
                        self._left_rotate(sibling)
                        sibling = node.parent.left
                    sibling.color = node.parent.color
                    node.parent.color = 'BLACK'
                    sibling.left.color = 'BLACK'
                    self._right_rotate(node.parent)
                    node = self.root

        node.color = 'BLACK'

    def _transplant(self, u, v):
        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _search(self, key):
        current = self.root
        while current != self.nil:
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return self.nil

    def _tree_minimum(self, node):
        while node.left != self.nil:
            node = node.left
        return node


# Driver code
if __name__ == "__main__":
    # Create a Red-Black Tree instance
    rb_tree = RedBlackTree()

    # Insert some keys into the Red-Black Tree
    keys = [10, 20, 5, 30, 15, 25]
    for key in keys:
        rb_tree.insert(key)

    # Perform inorder traversal and print the resulting tree structure
    print("Inorder Traversal:")
    for key, color in rb_tree.inorder_traversal():
        parent_key = rb_tree.nil.key if key == rb_tree.root.key else rb_tree.nil.key if key < rb_tree.root.key else rb_tree.root.key
        print(f"Key: {key}, Color: {color}, Parent: {parent_key}")

    # Delete a node from the Red-Black Tree
    rb_tree.delete(20)

    # Perform inorder traversal and print the resulting tree structure after deletion
    print("\nInorder Traversal after deleting 20:")
    for key, color in rb_tree.inorder_traversal():
        parent_key = rb_tree.nil.key if key == rb_tree.root.key else rb_tree.nil.key if key < rb_tree.root.key else rb_tree.root.key
        print(f"Key: {key}, Color: {color}, Parent: {parent_key}")
