#ai generated
from env import Environment
import random

class GameSimulator:
    def __init__(self, track_length=20):
        self.environment = Environment(track_length)
        self.history = []
        
    def log_state(self, action):
        state = {
            'action': action,
            'position': self.environment.car.position,
            'speed': self.environment.car.speed,
            'battery': self.environment.car.battery,
            'coins': self.environment.car.coins
        }
        
        segment = self.environment.track.get_segment(self.environment.car.position)
        if segment:
            if hasattr(segment, 'terrain'):
                state['segment'] = f"Terrain: {segment.terrain}"
            elif hasattr(segment, 'type'):
                state['segment'] = f"Obstacle: {segment.type}"
            elif hasattr(segment, 'reward'):
                state['segment'] = f"Reward: {segment.reward}"
                
        self.history.append(state)
        
    def run_simulation(self, strategy="balanced"):
        """
        Strategies:
        - aggressive: Maximum speed, minimal recharging
        - conservative: Maintain low speed, frequent recharging
        - balanced: Mix of speed and battery management
        - exploit: Try to exploit game mechanics
        """
        game_active = True
        turns = 0
        max_turns = 100  # Prevent infinite loops
        
        while game_active and turns < max_turns:
            turns += 1
            
            # Get current state
            current_battery = self.environment.car.battery
            current_speed = self.environment.car.speed
            current_segment = self.environment.track.get_segment(self.environment.car.position)
            
            # Choose action based on strategy
            action = self._choose_action(strategy, current_battery, current_speed, current_segment)
            
            # Log state before action
            self.log_state(action)
            
            # Execute action
            self.environment.step(action)
            
            # Check end conditions
            if self.environment.car.battery <= 0:
                print(f"Game Over! Out of battery! Position: {self.environment.car.position}")
                game_active = False
            elif self.environment.car.position >= self.environment.track.length:
                print(f"Track Completed! Coins: {self.environment.car.coins}")
                game_active = False
                
        return self._analyze_simulation()
    
    def _choose_action(self, strategy, battery, speed, segment):
        if strategy == "aggressive":
            if battery < 20:
                return "recharge"
            elif speed < 5:
                return "accelerate"
            return "move"
            
        elif strategy == "conservative":
            if battery < 50:
                return "recharge"
            elif speed > 2:
                return "decelerate"
            return "move"
            
        elif strategy == "balanced":
            if battery < 30:
                return "recharge"
            elif speed < 3 and battery > 50:
                return "accelerate"
            return "move"
            
        elif strategy == "exploit":
            # Try to exploit game mechanics
            if battery > 70:  # Testing recharge at high battery
                return "recharge"
            elif speed == 1:  # Testing extreme acceleration
                return "accelerate"
            return "move"
    
    def _analyze_simulation(self):
        vulnerabilities = []
        
        # Check for potential issues
        for i in range(len(self.history)-1):
            current = self.history[i]
            next_state = self.history[i+1]
            
            # Battery drain inconsistencies
            if next_state['battery'] > current['battery'] and current['action'] != 'recharge':
                vulnerabilities.append(f"Battery increased without recharge at turn {i}")
                
            # Speed anomalies
            if next_state['speed'] < current['speed'] and current['action'] not in ['decelerate']:
                vulnerabilities.append(f"Unexpected speed decrease at turn {i}")
                
            # Position movement issues
            if next_state['position'] <= current['position'] and current['action'] == 'move':
                vulnerabilities.append(f"No forward movement despite move action at turn {i}")
                
            # Battery drain vs speed correlation
            if current['action'] == 'move':
                expected_drain = current['speed'] * 0.3
                actual_drain = current['battery'] - next_state['battery']
                if abs(expected_drain - actual_drain) > 0.1:
                    vulnerabilities.append(f"Inconsistent battery drain at turn {i}")
        
        return {
            'turns_taken': len(self.history),
            'final_position': self.environment.car.position,
            'final_speed': self.history[-1]['speed'],
            'final_battery': self.history[-1]['battery'],
            'coins_collected': self.history[-1]['coins'],
            'vulnerabilities': vulnerabilities
        }

def run_comprehensive_test():
    print("Running comprehensive game simulation...")
    
    strategies = ["aggressive", "conservative", "balanced", "exploit"]
    results = {}
    
    for strategy in strategies:
        print(f"\nTesting {strategy} strategy:")
        simulator = GameSimulator(track_length=20)
        results[strategy] = simulator.run_simulation(strategy)
        
        print(f"Results for {strategy}:")
        print(f"Turns taken: {results[strategy]['turns_taken']}")
        print(f"Final position: {results[strategy]['final_position']}")
        print(f"Final speed: {results[strategy]['final_speed']}")
        print(f"Final battery: {results[strategy]['final_battery']:.1f}")
        print(f"Coins collected: {results[strategy]['coins_collected']}")
        print("\nVulnerabilities found:")
        for vuln in results[strategy]['vulnerabilities']:
            print(f"- {vuln}")
            
    return results

if __name__ == "__main__":
    results = run_comprehensive_test()