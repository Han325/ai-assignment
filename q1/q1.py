# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 13:52:05 2023

@title: Artifical Intelligence Assignment 2 Question 1 - River Crossing Puzzle using Depth-Limited Search
"""

# Collections module used for the Counters container.
# Time module used to find the time taken to reach the solution and the delay when displaying the path.
import collections
import time

# Definition for the River Crossing Puzzle problem class.
class Puzzle:
    # Class variables for the unexpanded and expanded states in the search.
    unexpanded = []
    expanded = []

    def __init__(self, start_state, max_depth) -> None:
        self.unexpanded.append(start_state)
        self.max_depth = max_depth

    # Depth First Search algorithm with depth limit.
    def DFS(self):
        # Loop until a solution is found or depth limit is reached.
        while True:
            try:
                # Get the last state from the unexpanded list (LIFO).
                node = self.unexpanded[-1]
               # Check if the state is valid.
                if node.isValid():
                    # Check if the state is the goal state.
                    if node.isGoal():
                        # Display that the solution is found and path.
                        self.displayPath(node, 0.5)
                        print('Solution Found at Depth: ', node.depth)
                        return

                    # Check if the state can be expanded further.
                    if not self.checkExpansion(node):
                        # Mark the state as expanded, remove from unexpanded.
                        self.expanded.append(node)
                        self.unexpanded.pop(-1)

                        # If depth limit is not reached, add children to unexpanded.
                        if node.depth < self.max_depth:
                            self.unexpanded.extend(node.generator())
                    else:
                        # If state has been expanded before, remove from unexpanded.
                        self.unexpanded.pop(-1)
                else:
                    # If state is not valid, remove from unexpanded.
                    self.unexpanded.pop(-1)
            except IndexError:
                # Catch IndexError (empty unexpanded list) and print depth limit.
                print('Depth Limit : {}'.format(self.max_depth))
                return

    # Method to check if given state has been expanded before through comparison.
    def checkExpansion(self, state):
        # Loop through the list of expanded states.
        for node in self.expanded:
            # Check if the current expanded state is equal to the given state.
            if (collections.Counter(node.origin) == collections.Counter(state.origin) and
                collections.Counter(node.destination) == collections.Counter(state.destination) and
                    node.transport == state.transport):
                # If there is a match, the state has been expanded before.
                return True
        # If no match is found, the state has not been expanded before.
        return False

    # Display the path (current state) from the root state to the given state with a delay between each step.
    def displayPath(self, state, delay):
        # Print the representation of the current state.
        print(state.show(), '\n')
        # Loop until the root state (parent is None)
        while state.parent != None:
            # Introduce a delay for visualization purposes.
            time.sleep(delay)
            # Move to the parent state and prints its representation.
            state = state.parent
            print(state.show(), '\n')

# Definition of the Agent class.
class Agent:
    def __init__(self, agent, can_operate):
        self.agent = agent
        # Attribute used to determine if Agent is allowed to operate the transport.
        self.can_operate = can_operate

    def show(self):
        return("Agent: {}".format(self.agent))

# Definition of the State class, representing a state in the puzzle.
class State:
    # Initialize the State object with specific attributes.
    def __init__(self, destination, origin, transport, depth, parent):
        self.origin = origin
        self.destination = destination
        self.transport = transport
        self.depth = depth
        self.parent = parent

    # Method to generate possible successor states based on the current state.
    def generator(self):
        states = []

        # Determine the current and other locations based on the transport location.
        if self.transport:
            current_location = self.destination
            other_location = self.origin
        else:
            current_location = self.origin
            other_location = self.destination

        # Iterate over agents in the current location to generate successor states.
        for agent in current_location:
            for agent2 in current_location:
                # Create copies of current and other locations to avoid modifying the original state.
                current_location_copy = current_location.copy()
                other_location_copy = other_location.copy()

                # Skip iteration if the same agent is selected twice.
                if agent == agent2:
                    continue
                if not agent.can_operate and not agent2.can_operate:
                    continue
                if not self.transportValidation([agent, agent2]):
                    continue

                # Update the current location.
                current_location_copy.remove(agent)
                current_location_copy.remove(agent2)

                # Update the other location.
                other_location_copy.append(agent)
                other_location_copy.append(agent2)

                # Create a new state based on the transport location.
                if self.transport:
                    new_state = State(
                        current_location_copy, other_location_copy, False, self.depth + 1, self)
                else:
                    new_state = State(
                        other_location_copy, current_location_copy, True, self.depth + 1, self)

                # Append the new state to the list if it's not already present.
                if not new_state in states:
                    states.append(new_state)

            # Iterate over agents in the current location for single-agent movements.
            for Agent in current_location:
                # Create copies of current and other locations to avoid modifying the original state.
                current_location_copy = current_location.copy()
                other_location_copy = other_location.copy()

                if Agent.can_operate:
                    # Update the current and other locations for a single-agent movement.
                    current_location_copy.remove(Agent)
                    other_location_copy.append(Agent)

                    # Create a new state based on the transport location.
                    if self.transport:
                        new_state = State(
                            current_location_copy, other_location_copy, False, self.depth + 1, self)
                    else:
                        new_state = State(
                            other_location_copy, current_location_copy, True, self.depth + 1, self)
                    states.append(new_state)

        return states

    # Method to check if the current state is valid based on location validation.
    def isValid(self):
        if self.locationValidation(self.origin) and self.locationValidation(self.destination):
            return True
        return False

    # Method to check the validity of a given location based on the rules of the puzzle.
    def locationValidation(self, location):
        if mother not in location and father not in location and child in location:
            return False
        elif criminal in location and len(location) > 1 and policeman not in location:
            return False
        else:
            return True

    # Method to check the validity of current agents on the transport based on the rules of the puzzle.
    def transportValidation(self, transport):
        if criminal in transport and policeman not in transport:
            return False
        else:
            return True

    # Method to check if the current state is the goal state by checking if Origin is empty.
    def isGoal(self):
        if len(self.origin) == 0:
            return True
        return False

    # Definition of the show method for this State, displays a formatted representation of the current state.
    def show(self):
        result = 'Origin: {}\nDestination: {}\nTransport is at {}'.format(
            [item.show() for item in self.destination],
            [item.show() for item in self.origin],
            'Origin <-' if self.transport else 'Destination ->'
        )
        return result

# Create unique agent objects.
mother = Agent("Mother", True)
father = Agent("Father", True)
child = Agent("Child", False)
criminal = Agent("Criminal", False)
policeman = Agent("Policeman", True)

# Initial state space where each agent is at the origin.
INITIAL_STATE = State([], [policeman, criminal, child,
                      father, mother], False, 0, None)

# Definition of the main function, with a max depth of 20.
def main():
    Puzzle(INITIAL_STATE, 20).DFS()

if __name__ == '__main__':
    # Record the start time.
    start = time.time()
    main()
    # Record the end time.
    end = time.time()
    # Print elapsed time.
    print(end - start)
