from decimal import Decimal
from tests import test_interval_spaces
from interval_spaces.avl_tree import IntervalUnionTree, Node


class AVLTreeTest(test_interval_spaces.TestIntervalSpaces):
    tree = IntervalUnionTree(0.0, 1.0)

    def test_insert_intervals(self):
        expected = Node(1.9, 2.0, height=4,
                        left=Node(1.3, 1.4, height=3,
                                  left=Node(0.0, 1.0, height=1),
                                  right=Node(1.46, 1.48, height=2,
                                             left=Node(1.42, 1.45, height=1),
                                             right=Node(1.6, 1.7, height=1))),
                        right=Node(5.0, 10.0, height=2,
                                   right=Node(22.4, 50.0, height=1)))

        self.tree.insert(1.3, 1.4)
        self.tree.insert(5.0, 6.6)
        self.tree.insert(1.6, 1.7)
        self.tree.insert(1.9, 2.0)
        self.tree.insert(6, 10)
        self.tree.insert(22.4, 50.0)
        self.tree.insert(1.42, 1.45)
        self.tree.insert(1.46, 1.48)

        assert repr(self.tree.root_tree) == repr(expected)

    def test_order_intervals(self):
        expected = [(0.0, 1.0), (1.3, 1.4), (1.42, 1.45), (1.46, 1.48),
                    (1.6, 1.7), (1.9, 2.0), (5.0, 10.0), (22.4, 50.0)]

        print(self.tree.order())

        assert repr(self.tree.order()) == repr(expected)

    def test_remove_intervals(self):
        expected = Node(1.95, 2.0, height=3,
                        left=Node(1.6, 1.65, height=2,
                                  left=Node(0.0, 0.5, height=1),
                                  right=None),
                        right=Node(22.4, 30.0, height=2,
                                   left=Node(5.0, 10.0, height=1),
                                   right=Node(48.0, 50.0, height=1)))  # 15.2

        self.tree.remove(0.8, 1.5)
        self.tree.remove(0.5, 1.3)
        self.tree.remove(30.0, 48.0)
        self.tree.remove(1.65, 1.95)

        assert repr(self.tree.root_tree) == repr(expected)

    def test_tree_size(self):
        assert self.tree.size == Decimal(f'{15.20}')

    def test_tree_sample(self):
        print(self.tree.sample())
