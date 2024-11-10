import random

class Obstacles:
    obs = ["wall", "animal", 'mud']

    def __init__(self, obstacle):
        self.type = obstacle

    @classmethod
    def random_obstacle(cls):
        obstacle = random.choice(cls.obs)
        return cls(obstacle)

    def impact(self, car):
        if self.type == "wall":
            car.speed = max(0, car.speed - 2)
        elif self.type == "animal":
            car.decelerate()
            car.battery -= 3
        elif self.type == "mud":
            car.speed = max(1, car.speed * 0.7)


class Rewards:
    rews = ["small_coin", 'big_coin', "benzene", 'speed_boost', 'nitro_boost']

    def __init__(self, reward):
        self.reward = reward

    @classmethod
    def random_reward(cls):
        reward = random.choice(cls.rews)
        return cls(reward)

    def impact(self, car):
        if self.reward == "small_coin":
            car.collect_coin(1)
        elif self.reward == "big_coin":
            car.collect_coin(10)
        elif self.reward == "benzene":
            car.battery = min(car.battery + 10, car.MAX_BATTERY)
        elif self.reward == "speed_boost":
            car.speed = min(car.speed + 1, car.MAX_SPEED)
        elif self.reward == "nitro_boost":
            car.speed = min(car.speed * 1.5, car.MAX_SPEED)


class Terrain:
    types = {"sand": 0.7, "snow": 0.8, "asphalt": 1}
    terrains = ['sand', 'asphalt', 'snow']

    def __init__(self, terrain):
        self.terrain = terrain
        self.speed_mult = self.types[terrain]

    @classmethod
    def random_terrain(cls):
        return random.choice(Terrain.terrains)

    def get_mult(self):
        return self.speed_mult


class Track:
    def __init__(self, length):
        self.length = length
        self.segments = []
        self.init_track(length)
    
    def init_track(self, length):
        # Create a list of 5 rows, each row corresponding to one of the 5 track levels
        for i in range(length//2):
            # Column with 5 rows for each segment: [terrain, obstacle/reward]
            terrain_column = []
            obstacle_reward_column = []

            # Randomly choose terrain for all 5 rows in this column
            terrain_type = random.choice(Terrain.terrains)  # Random terrain type for the column
            for j in range(5):
                terrain_column.append(Terrain(terrain_type))  # All rows in this column have the same terrain

            # Random obstacles/rewards for each row in this column
            for j in range(5):
                obstacle_reward_column.append(random.choice([Obstacles.random_obstacle(), Rewards.random_reward()]))

            # Each column will contain terrain and obstacle/reward in 5 rows
            self.segments.append((terrain_column, obstacle_reward_column))
        
        # Add the ending line column at the end of the track (filled with '#')
        self.segments.append([('#', '#', '#', '#', '#')]*5)  # End line column
        
        # Print the shape of the track (number of rows and columns)
        print(f"Track Shape: {5} rows x {length+1} columns")

    def print_track(self):
        for i in range(5):  # We have 5 rows
            row = ""
            for segment in self.segments:  # Iterate over columns
                if isinstance(segment, tuple):  # Terrain and obstacle/reward columns
                    terrain_segment = segment[0][i]  # Terrain of the i-th row in this column
                    obstacle_reward_segment = segment[1][i]  # Obstacle/Reward of the i-th row in this column
                    row += f"{terrain_segment.terrain} | {obstacle_reward_segment.reward if isinstance(obstacle_reward_segment, Rewards) else obstacle_reward_segment.type} | "
                else:
                    # This is the ending line column
                    row += "# | "
            print(row.strip("| "))


class Car:
    MAX_BATTERY = 100
    MAX_SPEED = 5

    def __init__(self, track_length):
        self.position = [0, 0]  # Starting position at top-left of the track
        self.speed = 1
        self.battery = 100
        self.track = Track(track_length)
        self.coins = 0

    def accelerate(self):
        self.speed = min(self.speed + 1, self.MAX_SPEED)

    def decelerate(self):
        self.speed = max(self.speed - 1, 1)

    def recharge(self):
        if self.battery <= 70:
            self.battery = min(self.battery + 20, self.MAX_BATTERY)
            return True
        return False

    def collect_coin(self, amount):
        self.coins += amount

    def move(self, action):
        # Determine movement based on the action
        if action == 'up' and self.position[0] > 0:
            self.position[0] -= 1
        elif action == 'down' and self.position[0] < 4:
            self.position[0] += 1
        elif action == 'left' and self.position[1] > 0:
            self.position[1] -= 1
        elif action == 'right' and self.position[1] < self.track.length:
            self.position[1] += 1

        self.battery -= (self.speed * 0.2)
        self.battery = max(0, self.battery)

        seg_info = self.track.get_segment(self.position)

        if isinstance(seg_info, Terrain):
            original = self.speed
            self.speed = max(1, min(original * seg_info.get_mult(), self.MAX_SPEED))

        elif isinstance(seg_info, Obstacles):
            seg_info.impact(self)

        elif isinstance(seg_info, Rewards):
            seg_info.impact(self)

    def get_position(self):
        return self.position

    def game_over(self):
        print(f"\nPosition: {self.position} \n Battery: {self.battery} \nSpeed: {self.speed} \n")
        return self.position[1] >= self.track.length  # Car reaches the finish line

class Environment:
    def __init__(self, track_length):
        self.track = Track(track_length)
        self.car = Car(track_length)
        self.rebuild()

    def rebuild(self):
        self.car.position = 0
        self.car.battery = 100
        self.car.speed = 1
        self.car.coins = 0

    def step(self, action):
        if action == 'accelerate':
            self.car.accelerate()
        elif action == 'decelerate':
            self.car.decelerate()
        elif action == 'recharge':
            self.car.recharge()

        self.car.move()

        if self.game_over():
            print("Game Over")
            return True

    def game_over(self):
        print(f"\nPosition: {self.car.position} \n Battery: {self.car.battery} \nSpeed: {self.car.speed} \n")
        return self.car.position >= self.track.length or self.car.battery <= 0 or self.car.speed == 0
# Now to test:

def main():
    track_length = 10
    env = Environment(track_length)
    print("Track with Finish Line:")
    env.track.print_track()

if __name__ == "__main__":
    main()
