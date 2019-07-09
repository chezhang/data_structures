class Dic:
    def __init__(self, data = None):
        self.root = None
        if type(data) == dict:
            for key, val in data.iteritems():
                self[key] = val
        elif data:
            for item in data:
                if type(item) == tuple or type(item) == list:
                    if len(item) == 2:
                        key, val = item
                        if key.__hash__:
                            self[key] = val
                        else:
                            raise Exception('Un-hashable key: {}'.format(key))
                    else:
                        raise Exception('Incorrect length of key value pair: {}'.format(item))
                elif item.__hash__:
                    self[item] = None
                else:
                    raise Exception('Unsupported type: {}'.format(type(item)))

    class Node:
        def __init__(self, key, val = None, parent = None):
            self.key = key
            self.val = val
            self.height = 1
            self.parent = parent
            self.left = None
            self.right = None

        @property
        def left_height(self):
            return 0 if not self.left else self.left.height

        @property
        def right_height(self):
            return 0 if not self.right else self.right.height

        def update_height(self):
            newHeight = max(self.left_height, self.right_height) + 1
            changed = newHeight != self.height
            self.height = newHeight
            return changed

        def balance(self):
            heightDiff = self.left_height - self.right_height
            if abs(heightDiff) > 2:
                raise Exception('height error')
            if heightDiff == 2:
                self.left.rotate_left()
                return self.rotate_right()
            if heightDiff == -2:
                self.right.rotate_right()
                return self.rotate_left()
            return self

        def rotate_right(self):
            new = self
            if self.left_height > self.right_height:
                new = self.left
                self.left = new.right
                new.right = self
                if self.left:
                    self.left.parent = self
                self.update_parent(new)
                self.update_height()
                new.update_height()
            return new

        def rotate_left(self):
            new = self
            if self.left_height < self.right_height:
                new = self.right
                self.right = new.left
                new.left = self
                if self.right:
                    self.right.parent = self
                self.update_parent(new)
                self.update_height()
                new.update_height()
            return new

        def update_parent(self, new):
            parent = self.parent
            if parent:
                if parent.left == self:
                    parent.left = new
                else:
                    parent.right = new
            if new:
                new.parent = self.parent
                self.parent = new

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

    def __find_node(node, key, parent = None, isLeft = None, insert = False):
        if node:
            if key < node.key:
                return Dic.__find_node(node.left, key, node, True, insert)
            elif key > node.key:
                return Dic.__find_node(node.right, key, node, False, insert)
        elif insert and parent:
            node = Dic.Node(key, parent = parent)
            if isLeft:
                parent.left = node
            else:
                parent.right = node
        return node

    def __getitem__(self, key):
        node = Dic.__find_node(self.root, key)
        if node:
            return node.val
        else:
            raise Exception('No value found for key: {}'.format(key))

    def __setitem__(self, key, val):
        if self.root:
            node = Dic.__find_node(self.root, key, insert = True)
            node.val = val
            self.__update_insert(node.parent)
        else:
            self.root = Dic.Node(key, val)

    def __remove_node(self, node):
        if node:
            if node.height == 1:
                if node == self.root:
                    self.root = None
                else:
                    node.update_parent(None)
                    self.__update_remove(node.parent)
            else:
                scapegoat = node.precursor() if node.left_height > node.right_height else node.successor()
                node.key, node.val = scapegoat.key, scapegoat.val
                self.__remove_node(scapegoat)

    def __update_insert(self, node):
        if node and node.update_height():
            new = node.balance()
            if node == self.root:
                self.root = new
            self.__update_insert(new.parent)

    def __update_remove(self, node):
        if node:
            new = node.balance()
            if new == node:
                node.update_height()
            elif node == self.root:
                self.root = new
            self.__update_remove(node.parent)
    
    def __nodes(self, node):
        if node:
            if node.left:
                yield from self.__nodes(node.left)
            yield node
            if node.right:
                yield from self.__nodes(node.right)

    def __nodes_reverse(self, node):
        if node:
            if node.right:
                yield from self.__nodes_reverse(node.right)
            yield node
            if node.left:
                yield from self.__nodes_reverse(node.left)

    def get(self, key):
        node = Dic.__find_node(self.root, key)
        if node:
            return node.val
        else:
            return None

    def remove(self, key):
        self.__remove_node(Dic.__find_node(self.root, key))

    def display_as_key(self, width_factor = 1):
        if width_factor >= 0:
            width = 2 ** (width_factor + 1) - 2 if width_factor > 0 else 1
            queue = [self.root]
            height = 0 if not self.root else self.root.height
            while any(queue):
                nextLevel = []
                formatter = '{{:^{}}}'.format(2 ** (height + width_factor))
                for node in queue:
                    if node:
                        key = node.key if len(str(node.key)) <= width else '?' * width
                        print(formatter.format(key), end = '')
                        nextLevel += [node.left, node.right]
                    else:
                        print(formatter.format('x' * width), end = '')
                        nextLevel += [None] * 2
                queue = nextLevel
                height -= 1
                print()

    def pairs(self, reverse = False):
        nodes = self.__nodes_reverse(self.root) if reverse else self.__nodes(self.root)
        yield from ((node.key, node.val) for node in nodes)        

    def precursor_pair(self, key):
        node = Dic.__find_node(self.root, key)
        if node:
            pre = node.precursor()
            if pre:
                return (pre.key, pre.val)
        return (None, None)
        
    def successor_pair(self, key):
        node = Dic.__find_node(self.root, key)
        if node:
            suc = node.successor()
            if suc:
                return (suc.key, suc.val)
        return (None, None)

def main():
    test()

def test():
    def check(node):
        if node:
            if abs(node.left_height - node.right_height) > 1 or node.height != max(node.left_height, node.right_height) + 1:
                print('Height error')
                return False
            elif node.left and node.left.parent != node or node.right and node.right.parent != node:
                print('Parent error')
                return False
            else:
                return check(node.left) and check(node.right)
        return True

    import random
    test_count = 100
    sample_range = 100
    for count in range(test_count):
        print('Test number: {}'.format(count))
        tree = Dic()
        sample = random.sample(range(sample_range), random.randint(0, sample_range))
        print('Insert: {}'.format(sample))
        for i in sample:
            tree[i] = 0
            if tree[i] != 0:
                print('Index error')
                return
            if not check(tree.root):
                return

        sample.sort()
        if not sample == [key for key, val in tree.pairs()] == [key for key, val in tree.pairs(reverse = True)][::-1]:
            print('Sort error')
            return

        keys_remove = random.sample(sample, random.randint(0, len(sample)))
        print('Remove: {}'.format(keys_remove))
        for key in keys_remove:
            tree.remove(key)
            if not check(tree.root):
                return

        random.shuffle(keys_remove)
        for key in keys_remove:
            tree[key] = 0
        if sample != [key for key, val in tree.pairs()]:
            print('Sort error')
            return
        
        if sample:
            for i in range(10):
                index = random.randint(0, len(sample) - 1)
                if index > 0 and sample[index - 1] != tree.precursor_pair(sample[index])[0]:
                    print('Precursor error')
                    return
                if index < len(sample) - 1 and sample[index + 1] != tree.successor_pair(sample[index])[0]:
                    print('Successor error')
                    return
                if not check(tree.root):
                    return
        print()

if __name__ == '__main__':
    main()
