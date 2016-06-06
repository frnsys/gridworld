import random
from environment import Environment
from render import save_gif


if __name__ == '__main__':
    steps = 100
    images = []

    # define the gridworld environment
    env = Environment([
        [-10,0,0,50],
        [0,10,100, 0, -100, 20],
        [0,0, None, 10, None, -10, None],
        [None,0, 5, 10, None, 500, 0]
    ])

    # start at a random position
    pos = random.choice(env.positions)
    env.render(pos)

    for i in range(steps):
        pos = random.choice(env.positions)
        images.append(env.render(pos))
    save_gif('test.gif', images)