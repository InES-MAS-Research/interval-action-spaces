from interval_spaces.avl_tree import IntervalUnionTree
import numpy as np
from gym import Env
from gym.spaces import Box
from random import uniform

num_steps = 20

payoffs = np.array([[[2, 2], [8, 1]],
                    [[3, 3], [1, 6]]])


def utility(x1, x2, agent):
    return (payoffs[0][0][agent] - payoffs[0][1][agent] - payoffs[1][0][agent] + payoffs[1][1][agent]) * x1 * x2 + \
           (payoffs[0][1][agent] - payoffs[1][1][agent]) * x1 + (payoffs[1][0][agent] - payoffs[1][1][agent]) * x2 + \
           payoffs[1][1][agent]


class ContinuousMatrixGameEnvironment(Env):

    def __init__(self):
        super(ContinuousMatrixGameEnvironment, self).__init__()

        self.observation_shape = (0.0, 10.0, 2)
        self.observation_space = Box(0.0, 10.0, shape=(2,))

        self.action_space: IntervalUnionTree = IntervalUnionTree(0.0, 1.0)

    def render(self, mode="human"):
        print(payoffs)

    def step(self, action):
        observation = [action[0], action[1]]
        rewards = {0: utility(action[0], action[1], 0), 1: utility(action[0], action[1], 1)}

        return observation, rewards


env = ContinuousMatrixGameEnvironment()

current_step = 0
next_step = 'remove'
while True:
    r1 = round(uniform(0.0, 1.0), 2)
    r2 = round(uniform(0.0, 1.0), 2)
    if r1 == r2:
        continue

    print(f'\n Round {current_step}')

    if next_step == 'insert':
        print(f'Expanding action space  by [{min(r1, r2)}, {max(r1, r2)}]')
        env.action_space.insert(min(r1, r2), max(r1, r2))
        next_step = 'remove'
    else:
        print(f'Reducing action space  by [{min(r1, r2)}, {max(r1, r2)}]')
        env.action_space.remove(min(r1, r2), max(r1, r2))
        next_step = 'insert'

    print(f'New action space: {env.action_space.order()}')
    print(f'Action space size: {env.action_space.size}')

    actions = {0: env.action_space.sample(), 1: env.action_space.sample()}
    print(f'Actions: {actions}')
    results = env.step(actions)
    print(f'Step: {results}')

    current_step += 1
    if current_step >= num_steps:
        break

print('\n Finished!')
