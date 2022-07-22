from tests import interval_spaces_test
from interval_spaces.avl_tree import IntervalUnionTree


class AVLTreeTest(interval_spaces_test.IntervalSpacesTest):

    def insert_intervals(self):
        expected = '<Node (1.9,2.0), left: <Node (1.3,1.4), left: <Node (0.0,1.0), left: None, right: None>, ' \
                   'right: <Node (1.46,1.48), left: <Node (1.42,1.45), left: None, right: None>, right: <Node (1.6,' \
                   '1.7), left: None, right: None>>>, right: <Node (5.0,10), left: None, right: <Node (22.4,50.0), ' \
                   'left: None, right: None>>> '

        tree = IntervalUnionTree(0.0, 1.0)
        tree.insert(1.3, 1.4)
        tree.insert(5.0, 6.6)
        tree.insert(1.6, 1.7)
        tree.insert(1.9, 2.0)
        tree.insert(6, 10)
        tree.insert(22.4, 50.0)
        tree.insert(1.42, 1.45)
        tree.insert(1.46, 1.48)

        assert repr(tree.root_tree) == expected

    def order_intervals(self):
        pass

    def remove_intervals(self):
        pass
