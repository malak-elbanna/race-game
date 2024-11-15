from src.environment.env import Environment
from src.environment.terrain import Terrain
from src.environment.obs_reward import Obstacles
from src.environment.car import Car
from src.agent.visualize import Visualizer
import heapq
import copy
import time

def visualize(solution, track_length):
    for step in solution:
        state = step[0]
        position = state[0]

        if position >= track_length:
            track_length = position + 1

        track = ['_'] * track_length
        if position < track_length:
            track[position] = '🏎️'
        print(''.join(track))

        time.sleep(0.5)
    print("Goal Reached!")

def heuristic(car_position, goal_position, speed, battery, track_length):
    distance_to_goal = goal_position - car_position
    battery_penalty = (100 - battery) * 0.5  
    speed_penalty = (Car.MAX_SPEED - speed) * 0.3  

    steps_to_goal = 0
    if speed > 0:
        steps_to_goal = distance_to_goal / speed
    else:
        steps_to_goal = float('inf')

    battery_consumption = steps_to_goal * 0.2 * speed

    if battery_consumption > battery:
        return track_length - car_position + 100

    return distance_to_goal + battery_penalty + speed_penalty

def path_cost(path, goal, length):
    current = path[-1][0]
    car_position = current[0]
    h_cost = heuristic(car_position, goal, current[1], current[2], length)
    return h_cost

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

def greedy(environment, goal, visualizer=None):
    initial_state = environment.get_state()
    frontier = []
    heapq.heappush(frontier, (0, [(initial_state, 0)]))  
    visited = {}

    while frontier:
        f_cost, path = heapq.heappop(frontier)
        state = path[-1][0]
        
        if state[0] >= goal:
            return path

        if environment.game_over():
            continue

        if state in visited and visited[state] <= f_cost:
            continue

        visited[state] = f_cost

        successors = get_successors(environment, path)
        for new_state, cost in successors:
            if visualizer:
                visualizer.add_state(state, new_state, action="move")

            if new_state not in visited or visited[new_state] > f_cost + cost:
                new_path = path + [(new_state, cost)]
                heapq.heappush(frontier, (path_cost(new_path, goal, environment.track.length), new_path))

    return None  

def main():
    env = Environment(track_length=1000)  
    visualizer = Visualizer()
    solution = greedy(env, env.track.length - 1, visualizer)

    if solution:
        print("Solution path:", solution)
        total_cost = 0
        for i, cost in solution:
            total_cost += cost

        print("Total cost:", total_cost)

        #visualize(solution, env.track.length)
        visualizer.show_graph(solution)
    else:
        print("no solution")
        visualizer.show_graph()

main()
