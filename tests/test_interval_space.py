from unittest import TestCase


class TestIntervalSpaces(TestCase):

    def test_imports(self):
        from interval_spaces.interval_space import IntervalSpace
        from interval_spaces.tree_space import TreeSpace, Node
        from interval_spaces.bucket_space import BucketSpace
