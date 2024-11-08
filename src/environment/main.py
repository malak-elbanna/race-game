#ai generated
from env import Environment

def run_game():
    # Initialize environment with a track length of 20
    environment = Environment(track_length=20)
    game_active = True
    
    while game_active and not environment.game_over():
        # Print current state
        print(f"\nCurrent Status:")
        print(f"Position: {environment.car.position}")
        print(f"Speed: {environment.car.speed}")
        print(f"Battery: {environment.car.battery:.1f}")
        print(f"Coins: {environment.car.coins}")
        
        # Get current segment info
        current_segment = environment.track.get_segment(environment.car.position)
        if current_segment:
            if hasattr(current_segment, 'terrain'):
                print(f"Current terrain: {current_segment.terrain}")
            elif hasattr(current_segment, 'type'):
                print(f"Obstacle ahead: {current_segment.type}")
            elif hasattr(current_segment, 'reward'):
                print(f"Reward ahead: {current_segment.reward}")
        
        # Get player action
        print("\nAvailable actions: accelerate, decelerate, recharge, move")
        action = input("Enter action: ").lower()
        
        if action in ['accelerate', 'decelerate', 'recharge', 'move']:
            environment.step(action)
            
            # Check if game should end
            if environment.car.battery <= 0:
                print("Game Over! Out of battery!")
                game_active = False
            elif environment.car.position >= environment.track.length:
                print(f"Congratulations! You finished the track!")
                print(f"Final coins collected: {environment.car.coins}")
                game_active = False
        else:
            print("Invalid action! Please try again.")

if __name__ == "__main__":
    run_game()