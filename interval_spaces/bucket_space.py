from interval_spaces.interval_space import IntervalSpace
import math
import numpy as np
from decimal import Decimal
from random import uniform


class BucketSpace(IntervalSpace):

    def __init__(self, a, b, *, bucket_width=1.0, epsilon=0.01):
        super().__init__()
        self.a, self.b, self.bucket_width, self.epsilon = Decimal(f'{a}'), Decimal(f'{b}'), Decimal(f'{bucket_width}'), Decimal(f'{epsilon}')
        self.number_of_buckets = math.ceil((self.b - self.a) / self.bucket_width)
        self.buckets = np.ones((self.number_of_buckets,), dtype=bool)

    def __str__(self):
        intervals = ' '.join(f'[{float(a)}, {float(b)})' for a, b in self.intervals) if self.intervals else '()'
        return f'<BucketSpace {intervals}>'

    def __repr__(self):
        return self.__str__()

    def __bool__(self):
        return bool(np.any(self.buckets))

    def __contains__(self, item):
        return self.contains(item)

    def contains(self, x):
        return False if x < self.a or x >= self.b else self.buckets[self._bucket(x)]

    def sample(self):
        if not self.intervals:
            return None
        else:
            x = Decimal(f'{uniform(0.0, float(self.b - self.a))}')

            for i, (a, b) in enumerate(self.intervals):
                if x > Decimal(b) - Decimal(a):
                    x -= Decimal(b) - Decimal(a)
                else:
                    return Decimal(a) + x

        return self.intervals[-1][1]

    def clone(self):
        space = BucketSpace(self.a, self.b, bucket_width=self.bucket_width, epsilon=self.epsilon)
        space.buckets = np.copy(self.buckets)
        return space

    def clone_and_remove(self, x):
        space = self.clone()
        space.remove(x)
        return space

    def remove(self, x, with_epsilon=True):
        x = Decimal(f'{x}')

        if with_epsilon:
            self._set(x, False)
        else:
            self.buckets[self._bucket(x)] = False

    def add(self, x, with_epsilon=True):
        x = Decimal(f'{x}')

        if with_epsilon:
            self._set(x)
        else:
            self.buckets[self._bucket(x)] = True

    @property
    def intervals(self):
        a, intervals = None, []
        for i in range(self.number_of_buckets):
            if a is None:
                if self.buckets[i]:
                    a = self.a + i * self.bucket_width
            elif not self.buckets[i]:
                intervals.append((float(a), float(self.a + i * self.bucket_width)))
                a = None
            elif i == self.number_of_buckets - 1:
                intervals.append((float(a), float(self.b)))

        return intervals

    def _bucket(self, x):
        return math.floor((x - self.a) / self.bucket_width)

    def _set(self, x, value=True):
        lower_bucket = self._bucket(x - self.epsilon) if x - self.epsilon >= self.a else None
        upper_bucket = self._bucket(x + self.epsilon) if x + self.epsilon <= self.b else None

        if lower_bucket is None:
            if upper_bucket is None:
                self.buckets = np.ones((self.number_of_buckets,), dtype=bool) if value else np.zeros(
                    (self.number_of_buckets,), dtype=bool)
            else:
                self.buckets[:upper_bucket + 1] = value
        else:
            if upper_bucket is None:
                self.buckets[lower_bucket:] = value
            else:
                self.buckets[lower_bucket:upper_bucket + 1] = value

    def __hash__(self):
        return hash((self.a, self.b, self.bucket_width, tuple(self.intervals)))

    def __eq__(self, other):
        return (self.a, self.b, self.bucket_width, tuple(self.intervals)) == (
            other.a, other.b, other.bucket_width, tuple(other.intervals))
