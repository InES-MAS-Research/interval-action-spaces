from interval_spaces.avl_tree import IntervalUnionTree
import numpy as np
from gym import Env
from gym.spaces import Box

num_steps = 10

payoffs = np.array([[[2, 2], [8, 1]],
                    [[3, 3], [1, 6]]])


def utility(x1, x2, agent):
    return (payoffs[0][0][agent] - payoffs[0][1][agent] - payoffs[1][0][agent] + payoffs[1][1][agent]) * x1 * x2 +\
           (payoffs[0][1][agent] - payoffs[1][1][agent]) * x1 + (payoffs[1][0][agent] - payoffs[1][1][agent]) * x2  +\
           payoffs[1][1][agent]


class ContinuousMatrixGameEnvironment(Env):

    def __init__(self):
        super(ContinuousMatrixGameEnvironment, self).__init__()

        self.observation_shape = (0.0, 10.0, 2)
        self.observation_space = Box(0.0, 10.0, shape=(2,))

        self.action_space: IntervalUnionTree = IntervalUnionTree(0.0, 1.0)

        self.current_step = 0

    def render(self, mode="human"):
        print(payoffs)

    def step(self, action):
        observation = [action[0], action[1]]
        rewards = {0: utility(action[0], action[1], 0), 1: utility(action[0], action[1], 1)}

        return observation, rewards


env = ContinuousMatrixGameEnvironment()
env.action_space.insert(1.3, 1.4)
env.action_space.insert(5.0, 6.6)
print(env.action_space.root_tree)
env.action_space.insert(1.6, 1.7)
print(env.action_space.root_tree)
env.action_space.insert(1.9, 2.0)
print(env.action_space.root_tree)
env.action_space.insert(1.7, 1.9)
print(env.action_space.root_tree)
env.action_space.insert(1., 2.)
print(env.action_space.size)
print(env.action_space.root_tree)

while True:
    actions = {0: env.action_space.sample(), 1: env.action_space.sample()}
    results = env.step(actions)
    print(results)

    if env.current_step >= num_steps:
        break

print('Done!')
