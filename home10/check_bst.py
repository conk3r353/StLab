def checkBST(root):
    if root is None:
        return True
    stack = [(float('-inf'), root, float('+inf'))]
    while stack:
        minimal_value, node, maximal_value = stack.pop()
        if not (minimal_value < node.data < maximal_value):
            return False
        if node.left is not None:
            stack.append((minimal_value, node.left, node.data))
        if node.right is not None: 
            stack.append((node.data, node.right, maximal_value))
    return True