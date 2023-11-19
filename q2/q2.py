import heapq  # Using heapq for a priority queue

# Definitions
RUBBISH_WEIGHTS = {
    "orange": 5,
    "teal": 10,
    "blue": 20,
    "purple": 30,
}

# Helper function to calculate the distance between hexagons
def hex_distance(a, b):
    ax, ay = a
    bx, by = b
    return (abs(ax - bx) + abs(ax + ay - bx - by) + abs(ay - by)) // 2

class State:
    def __init__(self, position, collected_rubbish, energy_used, parent=None):
        self.position = position
        self.collected_rubbish = collected_rubbish
        self.energy_used = energy_used
        self.parent = parent

    def __lt__(self, other):
        return self.energy_used < other.energy_used

    def is_goal(self, disposal_room, total_rubbish):
        return self.position == disposal_room and all(rubbish in self.collected_rubbish for rubbish in total_rubbish)

    def energy_to_move(self):
        additional_energy = sum(weight // 10 for weight in self.collected_rubbish)
        return 1 + additional_energy

    @staticmethod
    def heuristic(state_position, rubbish_positions, goal_position):
        if not rubbish_positions:
            return hex_distance(state_position, goal_position)

        closest_rubbish = min(rubbish_positions, key=lambda pos: hex_distance(state_position, pos))
        closest_rubbish_distance = hex_distance(state_position, closest_rubbish)
        disposal_distance = hex_distance(closest_rubbish, goal_position)

        return closest_rubbish_distance + disposal_distance

def a_star_search(entry_point, disposal_room, rubbish_positions):
    open_list = []  # Priority queue
    closed_set = set()  # Set to store visited states

    # Start with the entry point state
    start_state = State(entry_point, frozenset(), 0)
    start_state_f_score = start_state.energy_used + State.heuristic(start_state.position, rubbish_positions, disposal_room)
    heapq.heappush(open_list, (start_state_f_score, start_state))

    while open_list:
        current_f_score, current_state = heapq.heappop(open_list)

        # Check if we've reached the goal
        if current_state.is_goal(disposal_room, rubbish_positions.values()):
            # Reconstruct the path
            path = []
            while current_state:
                path.append(current_state.position)
                current_state = current_state.parent
            return path[::-1], current_f_score  # Return the reversed path and the total energy used

        closed_set.add((current_state.position, current_state.collected_rubbish))

        # Generate children
        for direction in [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]:
            # Get a new position based on the direction
            new_position = (current_state.position[0] + direction[0], current_state.position[1] + direction[1])

            # Skip invalid positions
            if new_position not in rubbish_positions and new_position != disposal_room:
                continue

            # Calculate the new state's collected rubbish
            new_collected_rubbish = set(current_state.collected_rubbish)
            if new_position in rubbish_positions:
                new_collected_rubbish.add(rubbish_positions[new_position])
            new_collected_rubbish = frozenset(new_collected_rubbish)  # Make it hashable

            # Create a new state based on the new position
            new_state = State(new_position, new_collected_rubbish, current_state.energy_used + current_state.energy_to_move(), current_state)

            # Skip if this new state has already been visited
            if (new_state.position, new_state.collected_rubbish) in closed_set:
                continue

            # Calculate the f score for the new state
            new_f_score = new_state.energy_used + State.heuristic(new_state.position, rubbish_positions, disposal_room)

            # Add the new state to the open list
            heapq.heappush(open_list, (new_f_score, new_state))

    # If no path is found
    return None, None

# Define rooms with axial coordinates
entry_point = (-1, 2)  # Axial coordinates for the entry
disposal_room = (2, 3)  # Axial coordinates for the disposal room

# Define rubbish positions with their weights
rubbish_positions = {
    (1, 1): 5,   # Orange
    (0, 2): 5,   # Orange
    (1, 2): 30,  # Purple
    (2, 2): 5,   # Orange
    (-1, 3): 10, # Teal
    (0, 3): 10,  # Teal
    (1, 3): 10,  # Teal
    (0, 4): 5,   # Orange
    (2, 1): 20,  # Blue
    (-2, 2): 30  # Purple
}

# Execute the search
path, energy_used = a_star_search(entry_point, disposal_room, rubbish_positions)

# Print the results
if path:
    print("Path to take:", path)
    print("Total energy used:", energy_used)
else:
    print("No path found.")
