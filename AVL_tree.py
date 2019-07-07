class AVL:
    def __init__(self, data = None):
        self.root = None
        if type(data) == dict:
            for k, v in data.iteritems():
                self.insert(k, v)
        elif data:
            for i in data:
                if type(i) == int:
                    self.insert(i, None)
                else:
                    raise Exception('Type {} is not supported'.format(type(i)))

    class Node:
        def __init__(self, key, val, parent = None):
            self.key = key
            self.val = val
            self.height = 1
            self.parent = parent
            self.left = None
            self.right = None

        def leftHeight(self):
            return 0 if not self.left else self.left.height

        def rightHeight(self):
            return 0 if not self.right else self.right.height

        def updateHeight(self):
            newHeight = max(self.leftHeight(), self.rightHeight()) + 1
            changed = newHeight != self.height
            self.height = newHeight
            return changed

        def balance(self):
            heightDiff = self.leftHeight() - self.rightHeight()
            if abs(heightDiff) > 2:
                raise Exception('height error')
            if heightDiff == 2:
                self.left.rotateLeft()
                return self.rotateRight()
            if heightDiff == -2:
                self.right.rotateRight()
                return self.rotateLeft()
            return self

        def rotateRight(self):
            new = self
            if self.leftHeight() > self.rightHeight():
                new = self.left
                self.left = new.right
                new.right = self
                if self.left:
                    self.left.parent = self
                self.updateParent(new)
                self.updateHeight()
                new.updateHeight()
            return new
                
        def rotateLeft(self):
            new = self
            if self.leftHeight() < self.rightHeight():
                new = self.right
                self.right = new.left
                new.left = self
                if self.right:
                    self.right.parent = self
                self.updateParent(new)
                self.updateHeight()
                new.updateHeight()
            return new

        def updateParent(self, new):
            parent = self.parent
            if parent:
                if parent.left == self:
                    parent.left = new
                else:
                    parent.right = new
            new.parent = self.parent
            self.parent = new

        def keysInOrder(self):
            if self.left:
                for i in self.left.keysInOrder():
                    yield i
            yield self.key
            if self.right:
                for i in self.right.keysInOrder():
                    yield i

        def precursor(self):
            if self.left:
                node = self.left
                while node.right:
                    node = node.right
                return node
            node = self
            while node.parent and node.parent.left == node:
                node = node.parent
            return node.parent

        def successor(self):
            if self.right:
                node = self.right
                while node.left:
                    node = node.left
                return node
            node = self
            while node.parent and node.parent.right == node:
                node = node.parent
            return node.parent

    def insert(self, key, val):
        self.root = self.__insertInternal(self.root, key, val)

    def __insertInternal(self, node, key, val):
        if node:
            if key == node.key:
                node.val = val
            else:
                if key < node.key:
                    node.left = self.__insertInternal(node.left, key, val)
                    node.left.parent = node
                else:
                    node.right = self.__insertInternal(node.right, key, val)
                    node.right.parent = node
                if node.updateHeight():
                    node = node.balance()
        else:
            node = AVL.Node(key, val)
        return node

    def insert_bak(self, key, val):
        if self.root:
            node = self.root
            while node:
                if key < node.key:
                    if node.left:
                        node = node.left
                    else:
                        node.left = AVL.Node(key, val, node)
                        self.__update(node)
                        node = None
                elif key > node.key:
                    if node.right:
                        node = node.right
                    else:
                        node.right = AVL.Node(key, val, node)
                        self.__update(node)
                        node = None
                else:
                    node.val = val
                    node = None
        else:
            self.root = AVL.Node(key, val)

    def __update(self, node):
        if node and node.updateHeight():
            new = node.balance()
            if node == self.root:
                self.root = new
            self.__update(new.parent)

    def display(self):
        queue = [self.root]
        height = 0 if not self.root else self.root.height
        while any(queue):
            nextLevel = []
            formatter = '{{:^{}}}'.format(2 ** (height + 1))
            for node in queue:
                if node:
                    print(formatter.format(node.key), end = '')
                    nextLevel += [node.left, node.right]
                else:
                    print(formatter.format('xx'), end = '')
                    nextLevel += [None] * 2
            queue = nextLevel
            height -= 1 
            print()
    
    def keysInOrder(self):
        if self.root:
            yield from self.root.keysInOrder()

    def lastNode(self):
        node = self.root
        if not node:
            return None
        while node.right:
            node = node.right
        return node

    def firstNode(self):
        if not self.root:
            return None
        node = self.root
        while node.left:
            node = node.left
        return node

def main():
    test()

def test():
    import random
    for count in range(100):
        print('Test number: {}'.format(count))
        tree = AVL()
        sample = random.sample(range(100), random.randint(0, 100))
        print(sample)
        for i in sample:
            tree.insert(i, 0)
        sample.sort()
        keys1 = list(tree.keysInOrder())
        keys2 = []
        keys3 = []
        node = tree.lastNode()
        while node:
            keys2.append(node.key)
            node = node.precursor()
        node = tree.firstNode()
        while node:
            keys3.append(node.key)
            node = node.successor()
        if not sample == keys1 == keys2[::-1] == keys3:
            print(sample)
            print(keys1)
            print(keys2[::-1])
            print(keys3)
            print('Error')
            break
        print()

if __name__ == '__main__':
    main()
