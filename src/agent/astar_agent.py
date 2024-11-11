from src.environment.env import Environment
from src.environment.terrain import Terrain
from src.environment.obs_reward import Obstacles
import copy

def get_successors(environment, path):
    actions = ["accelerate", "decelerate", "recharge", "move"]
    state = path[-1][0]
    position = state[0]  
    successors = []

    for action in actions:
        env_copy = copy.deepcopy(environment)

        env_copy.car.position = position
        env_copy.car.speed = state[1]
        env_copy.car.battery = state[2]

        env_copy.step(action)
        new_state = env_copy.get_state()

        new_position = new_state[0]
        
        if new_position > position:
            segment = env_copy.track.get_segment(new_position)
            cost = 1

            new_speed = new_state[1]
            if isinstance(segment, Terrain):
                cost += max(1, new_speed * segment.get_mult())

            elif isinstance(segment, Obstacles):
                cost += max(1, new_speed * 1.5)

            successors.append((new_state, cost))
    return successors

