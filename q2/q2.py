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
        # Get the state with the lowest f from the open list
        current_state = min(open_list, key=lambda x: x[0])[1]
        open_list = [item for item in open_list if item[1] != current_state]
        closed_list.append(current_state)

        # If this state is the goal, reconstruct the path and return it
        if current_state.position == goal_position:
            path = [current_state.position]
            while current_state.position != initial_position:
                current_state = min([state for state in closed_list if state.position == current_state.position],
                                   key=lambda x: x.energy_used)
                path.insert(0, current_state.position)
            return path

        # Generate successor states and set their g, h, and f values
        successors = []
        for neighbor in [(current_state.position[0] + 1, current_state.position[1]),
                         (current_state.position[0] - 1, current_state.position[1]),
                         (current_state.position[0], current_state.position[1] + 1),
                         (current_state.position[0], current_state.position[1] - 1)]:
            # Check if the neighbor is within the grid
            if neighbor[0] >= -2 and neighbor[1] >= -2:
                # Check if the neighbor is not blocked by rubbish
                if neighbor not in rubbish_positions or neighbor in current_state.collected_rubbish:
                    # Calculate the new state
                    collected_rubbish = current_state.collected_rubbish.copy()
                    if neighbor in rubbish_positions:
                        collected_rubbish.append(rubbish_positions[neighbor])
                    new_state = State(neighbor, collected_rubbish, current_state.energy_used + current_state.energy_to_move())
                    # Calculate h and f for the new state
                    h_new = State.heuristic(new_state.position, rubbish_positions, goal_position)
                    f_new = new_state.energy_used + h_new

                    successors.append((f_new, new_state))

        for successor in successors:
            # If successor is in the closed list and has a lower or equal f, skip
            if any(successor[1].position == state.position and successor[0] >= state.energy_used + State.heuristic(state.position, rubbish_positions, goal_position) for state in closed_list):
                continue
            # If successor is in the open list and has a lower or equal f, skip
            if any(successor[1].position == state[1].position and successor[0] >= state[0] for state in open_list):
                continue
            # Otherwise, add successor to the open list
            open_list.append(successor)

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
