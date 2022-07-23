from interval_spaces.interval_space import IntervalSpace
from decimal import *


class Node(object):
    def __init__(self, x: float = None, y: float = None, left: object = None, right: object = None, height: int = 1):
        self.x: Decimal = Decimal(f'{x}')
        self.y: Decimal = Decimal(f'{y}')
        self.l = left
        self.r = right
        self.h = height

    def __str__(self):
        return f'<Node ({float(self.x)},{float(self.y)}), height: {self.h}, left: {self.l}, right: {self.r}>'

    def __repr__(self):
        return self.__str__()


class IntervalUnionTree(IntervalSpace):
    root_tree = None
    size: Decimal = 0

    def __init__(self, x, y):
        super().__init__()
        getcontext().prec = 28

        self.root_tree = Node(x, y)
        self.size = Decimal(y) - Decimal(x)

    def __contains__(self, item):
        return self.contains(item)

    def contains(self, x, root: Node = 'root'):
        if root == 'root':
            root = self.root_tree

        x = Decimal(f'{x}')

        if not root:
            return False
        elif root.x <= x <= root.y:
            return True
        elif root.x > x:
            return self.contains(x, root.l)
        else:
            return self.contains(x, root.r)

    def nearest_elements(self, x, root: Node = 'root'):
        if root == 'root':
            root = self.root_tree

        x = Decimal(f'{x}')

        if x > root.y:
            return self._nearest_elements(x, x - root.y, root.y, root.r)
        elif x < root.x:
            return self._nearest_elements(x, root.x - x, root.x, root.l)
        else:
            return x

    def _nearest_elements(self, x, min_diff, min_value, root: Node = 'root'):
        if root == 'root':
            root = self.root_tree

        x = Decimal(f'{x}')
        min_diff = Decimal(f'{min_diff}')
        min_value = Decimal(f'{min_value}')

        if not root:
            return [min_value]
        elif x > root.y:
            distance = x - root.y
            return [min_value, root.y] if distance == min_diff else [
                min_value] if distance > min_diff else self._nearest_elements(x, distance, root.y, root.r)
        elif x < root.x:
            distance = root.x - x
            return [min_value, root.x] if distance == min_diff else [
                min_value] if distance > min_diff else self._nearest_elements(x, distance, root.x, root.l)
        else:
            return x

    def nearest_element(self, x, root: Node = 'root'):
        if root == 'root':
            root = self.root_tree

        x = Decimal(f'{x}')

        return self.nearest_elements(x, root)[-1]

    def last_interval_before_or_within(self, x, root: Node = 'root'):
        if root == 'root':
            root = self.root_tree

        x = Decimal(f'{x}')

        if root.x <= x <= root.y:
            return (root.x, root.y), True
        elif x < root.x:
            return self.last_interval_before_or_within(x, root.l) if root.l is not None else ((root.x, root.y), False)
        else:
            return self.last_interval_before_or_within(x, root.r) if root.r is not None else (
                (root.x, root.y), False) if x < root.y else ((None, None), False)

    def first_interval_after_or_within(self, x, root: Node = 'root'):
        if root == 'root':
            root = self.root_tree

        x = Decimal(f'{x}')

        if root.x <= x <= root.y:
            return (root.x, root.y), True
        elif x > root.y:
            return self.first_interval_after_or_within(x, root.r) if root.r is not None else ((root.x, root.y), False)
        else:
            return self.first_interval_after_or_within(x, root.l) if root.l is not None else (
                (root.x, root.y), False) if x > root.x else ((None, None), False)

    def smallest_interval(self, root: Node = 'root'):
        if root == 'root':
            root = self.root_tree

        if root is None or root.l is None:
            return root
        else:
            return self.smallest_interval(root.l)

    def insert(self, x, y, root: Node = 'root'):
        assert y > x, 'Lower must be larger than upper bound'

        if root == 'root':
            root = self.root_tree

        x = Decimal(f'{x}')
        y = Decimal(f'{y}')

        if not root:
            self.size += y - x
            return Node(x, y)
        elif y < root.x:
            root.l = self.insert(x, y, root.l)
        elif x > root.y:
            root.r = self.insert(x, y, root.r)
        else:
            old_size = root.y - root.x
            root.x = min(root.x, x)
            root.y = max(root.y, y)
            self.size += root.y - root.x - old_size

            updated = False
            if root.r is not None and root.y >= root.r.x:
                root.y = root.r.y
                updated = True

            if root.l is not None and root.x <= root.l.y:
                root.x = root.l.x
                updated = True

            if updated:
                root.r = self.remove(root.x, root.y, root.r)
                root.l = self.remove(root.x, root.y, root.l)

        root.h = 1 + max(self.getHeight(root.l),
                         self.getHeight(root.r))

        b = self.getBal(root)

        if b > 1 and y < root.l.x:
            return self.rRotate(root)

        if b < -1 and x > root.r.y:
            return self.lRotate(root)

        if b > 1 and x > root.l.y:
            root.l = self.lRotate(root.l)
            return self.rRotate(root)

        if b < -1 and y < root.r.x:
            root.r = self.rRotate(root.r)
            return self.lRotate(root)

        self.root_tree = root
        return root

    def sample(self) -> float:
        pass

    def remove(self, x, y, root: Node = 'root', adjust_size: bool = True):
        if root == 'root':
            root = self.root_tree

        x = Decimal(f'{x}')
        y = Decimal(f'{y}')

        if not root:
            return None
        elif (x >= root.x and y < root.y) or (x > root.x and y <= root.y):
            self.size -= root.y - x
            old_maximum = root.y
            root.y = x
            self.insert(y, old_maximum, root)
        elif x < root.x < y < root.y:
            self.size -= y - root.x
            root.x = y
            root.l = self.remove(x, y, root.l, adjust_size)
        elif root.x < x < root.y < y:
            self.size -= root.y - x
            root.y = x
            root.r = self.remove(x, y, root.r, adjust_size)
        elif y < root.x:
            root.l = self.remove(x, y, root.l, adjust_size)
        elif x > root.y:
            root.r = self.remove(x, y, root.r, adjust_size)
        else:
            if adjust_size:
                self.size -= root.y - root.x
            if root.l is None:
                return self.remove(x, y, root.r, adjust_size)
            elif root.r is None:
                return self.remove(x, y, root.l, adjust_size)
            rgt = self.smallest_interval(root.r)
            root.x = rgt.x
            root.y = rgt.y
            root.r = self.remove(rgt.x, rgt.y, root.r, adjust_size=False)
            root = self.remove(x, y, root, adjust_size)
        if not root:
            return None

        root.h = 1 + max(self.getHeight(root.l),
                         self.getHeight(root.r))

        b = self.getBal(root)

        if b > 1 and self.getBal(root.l) >= 0:
            return self.rRotate(Node(None, None))

        if b < -1 and self.getBal(root.r) <= 0:
            return self.lRotate(root)

        if b > 1 and self.getBal(root.l) < 0:
            root.l = self.lRotate(root.l)
            return self.rRotate(root)

        if b < -1 and self.getBal(root.r) > 0:
            root.r = self.rRotate(root.r)
            return self.lRotate(root)

        self.root_tree = root
        return root

    def lRotate(self, z: Node):
        y = z.r
        T2 = y.l

        y.l = z
        z.r = T2

        z.h = 1 + max(self.getHeight(z.l),
                      self.getHeight(z.r))
        y.h = 1 + max(self.getHeight(y.l),
                      self.getHeight(y.r))

        return y

    def rRotate(self, z: Node):
        y = z.l
        T3 = y.r

        y.r = z
        z.l = T3

        z.h = 1 + max(self.getHeight(z.l),
                      self.getHeight(z.r))
        y.h = 1 + max(self.getHeight(y.l),
                      self.getHeight(y.r))

        return y

    def getHeight(self, root: Node = 'root'):
        if root == 'root':
            root = self.root_tree

        if not root:
            return 0

        return root.h

    def getBal(self, root: Node = 'root'):
        if root == 'root':
            root = self.root_tree

        if not root:
            return 0

        return self.getHeight(root.l) - self.getHeight(root.r)

    def order(self, root: Node = 'root'):
        if root == 'root':
            root = self.root_tree

        ordered = []
        if root.l is not None:
            ordered = ordered + self.order(root.l)
        ordered.append((root.x, root.y))
        if root.r is not None:
            ordered = ordered + self.order(root.r)
        return ordered

    def __str__(self):
        return f'<IntervalUnionTree>'

    def __repr__(self):
        return self.__str__()
