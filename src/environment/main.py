# main.py
from env import Environment

def run_simulation(track_length, steps):
    # Initialize environment
    env = Environment(track_length)
    
    # Print the initial environment setup
    print("Starting Simulation:")
    print(f"Track Length: {track_length}")
    print(f"Initial Car Position: {env.car.position}, Battery: {env.car.battery}, Speed: {env.car.speed}")

    # Simulate actions over a series of steps
    for step in range(steps):
        action = input("Enter action (accelerate, decelerate, recharge): ")
        env.step(action)
        
        # Check if the game is over after each action
        if env.game_over():
            print("Simulation ended.")
            break

        # Print current environment status
        print(f"Step {step + 1}")
        print(f"Car Position: {env.car.position}")
        print(f"Battery: {env.car.battery}")
        print(f"Speed: {env.car.speed}")
        print(f"Coins Collected: {env.car.coins}\n")

if __name__ == "__main__":
    # Define track length and number of steps for the simulation
    track_length = 20
    steps = 50

    # Run the simulation
    run_simulation(track_length, steps)
