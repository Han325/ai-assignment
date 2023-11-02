# Definitions
RUBBISH_WEIGHTS = {
    "orange": 5,
    "teal": 10,
    "blue": 20,
    "purple": 30,
}

# Helper function to calculate the distance between the hexagons
def hex_distance(a, b):
    ax, ay = a
    bx, by = b
    return (abs(ax - bx) + abs(ax + ay - bx - by) + abs(ay - by)) / 2


class State:
    def __init__(self, position, collected_rubbish, energy_used):
        self.position = position
        self.collected_rubbish = collected_rubbish  # weights of collected rubbish
        self.energy_used = energy_used

    def energy_to_move(self):
        return 1 + len([w for w in self.collected_rubbish if w >= 10])
    
 
    def heuristic(state_position, rubbish_positions, goal_position):
        # Using the Manhattan distance heuristic. Adaptable to hexagonal grid

        # If all rubbish is collected, heuristic is just the distance to the disposal room
        if not rubbish_positions:
            return hex_distance(state_position, goal_position)
        
        # Otherwise, find the closest rubbish and compute the sum of the distances
        distances = [hex_distance(state_position, rubbish_pos) for rubbish_pos in rubbish_positions]
        closest_rubbish_distance = min(distances)
        disposal_distance = hex_distance(rubbish_positions[distances.index(closest_rubbish_distance)], goal_position)
        return closest_rubbish_distance + disposal_distance
    

def a_star_search(initial_position, goal_position, rubbish_positions):
    open_list = []  # priority queue, ordered by f = g + h
    closed_list = []
    start_state = State(initial_position, [], 0)
    # Calculate f for the start state
    h_start = State.heuristic(start_state.position, rubbish_positions, goal_position)
    f_start = start_state.energy_used + h_start  # g(n) is 0 for start state
    
    # Add start state to the open list
    open_list.append((f_start, start_state))
    
    while open_list:
        # TODO: Get the state with the lowest f from the open list
        # TODO: If this state is the goal, reconstruct the path and return it
        # TODO: Generate successor states and set their g, h, and f values
        # TODO: For each successor
        # - If successor is in the closed list and has a lower or equal f, skip
        # - If successor is in the open list and has a lower or equal f, skip
        # - Otherwise, add successor to the open list
        
        # TODO: Add the current state to the closed list
        pass

    # If no solution found
    return None

# Mapping figure 1 to code
# Define rooms with axial coordinates
entry_point = (-1, 2)  # Axial coordinates for the entry
disposal_room = (2, 3)  # Axial coordinates for the disposal room

# Define rubbish positions with their weights
rubbish_positions = {
    (1, 1): 5,   # Orange
    (0, 2): 5,   # Orange
    (1, 2): 5,   # Orange
    (2, 2): 5,   # Orange
    (-1, 3): 10,  # Green
    (0, 3): 10,  # Green
    (1, 3): 10,  # Green
    (0, 4): 20,  # Blue
    (2, 1): 20,  # Blue
    (-2, 2): 30  # Purple
}

# Calling the function
# a_star_search(initial_position=entry_point, goal_position=disposal_room, rubbish_positions=rubbish_positions)
