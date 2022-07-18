from spaces.continuous.continuous import DiscontinuousContinuousActionSpace


class Node(object):
    def __init__(self, x: float = None, y: float = None):
        self.x = x
        self.y = y
        self.l = None
        self.r = None
        self.h = 1

    def __str__(self):
        return f'<Node ({self.x},{self.y}), left: {self.l}, right: {self.r}>'

    def __repr__(self):
        return self.__str__()


class IntervalUnionTree(DiscontinuousContinuousActionSpace):
    root_tree = None

    def __init__(self, x, y):
        super().__init__()
        self.root_tree = Node(x, y)

    def __contains__(self, item):
        return self.contains(item)

    def contains(self, x, root: Node = 'root'):
        if root == 'root':
            root = self.root_tree

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

        if x > root.y:
            return self._nearest_elements(x, x - root.y, root.y, root.r)
        elif x < root.x:
            return self._nearest_elements(x, root.x - x, root.x, root.l)
        else:
            return x

    def _nearest_elements(self, x, min_diff, min_value, root: Node = 'root'):
        if root == 'root':
            root = self.root_tree

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

        return self.nearest_elements(x, root)[-1]

    def last_interval_before_or_within(self, x, root: Node = 'root'):
        if root == 'root':
            root = self.root_tree

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
        if root == 'root':
            root = self.root_tree

        if not root:
            return Node(x, y)
        elif y < root.x:
            root.l = self.insert(x, y, root.l)
        elif x > root.y:
            root.r = self.insert(x, y, root.r)
        else:
            root.x = min(root.x, x)
            root.y = max(root.y, y)

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

    def remove(self, x, y, root: Node = 'root'):
        if root == 'root':
            root = self.root_tree

        if not root:
            return None
        elif x > root.x and y < root.y:
            old_maximum = root.y
            root.y = x
            self.insert(y, old_maximum, root)
        elif x < root.x < y < root.y:
            root.x = y
            root.l = self.remove(x, y, root.l)
        elif root.x < x < root.y < y:
            root.y = x
            root.r = self.remove(x, y, root.r)
        elif y < root.x:
            root.l = self.remove(x, y, root.l)
        elif x > root.y:
            root.r = self.remove(x, y, root.r)
        else:
            if root.l is None:
                return self.remove(x, y, root.r)
            elif root.r is None:
                return self.remove(x, y, root.l)
            rgt = self.smallest_interval(root.r)
            root.x = rgt.x
            root.y = rgt.y
            root.r = self.remove(rgt.x, rgt.y, root.r)
            root = self.remove(x, y, root)
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
