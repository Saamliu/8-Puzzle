"""
8-Puzzle Solver

This Python script solves the 8-Puzzle problem using the A* search algorithm.
It calculates the Manhattan distance as the heuristic function.

Author: Hirasawa
Date: 2024-08-26
Version: 1.1

"""

import heapq

class PuzzleNode:
    """
    Represents a node in the puzzle search tree.

    Attributes:
        state (list of list of int): The current puzzle state.
        goal_state (list of list of int): The goal puzzle state.
        parent (PuzzleNode, optional): The parent node.
        action (int, optional): The action that led to this state.
        cost (int, optional): The cost from the start state to this state.
        heuristic (int): The heuristic value calculated using the Manhattan distance.
        total_cost (int): The sum of the cost and heuristic value.
    """
    def __init__(self, current_state, target_state, parent=None, action=None, cost=0):
        self.state = current_state
        self.goal_state = target_state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = self.calculate_heuristic()
        self.total_cost = self.cost + self.heuristic

    def calculate_heuristic(self):
        """
        Calculate the Manhattan distance heuristic.

        Returns:
            int: The Manhattan distance.
        """
        return calculate_manhattan_distance(self.state, self.goal_state)

    def __lt__(self, other):
        """
        Less-than comparison based on total cost (cost + heuristic).

        Returns:
            bool: True if this node's total cost is less than the other node's.
        """
        return self.total_cost < other.total_cost

    def get_neighbors(self):
        """
        Generate all neighbor states of the current state.

        Returns:
            list: List of PuzzleNode objects representing the neighbor states.
        """
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        zero_pos = find_position(self.state, 0)
        for dx, dy in directions:
            new_pos = (zero_pos[0] + dx, zero_pos[1] + dy)
            if 0 <= new_pos[0] < 3 and 0 <= new_pos[1] < 3:
                new_state = [row[:] for row in self.state]
                new_state[zero_pos[0]][zero_pos[1]], new_state[new_pos[0]][new_pos[1]] = new_state[new_pos[0]][new_pos[1]], new_state[zero_pos[0]][zero_pos[1]]
                neighbors.append(PuzzleNode(new_state, self.goal_state, self, self.state[new_pos[0]][new_pos[1]], self.cost + 1))
        return neighbors

def calculate_manhattan_distance(state, target_goal_state):
    """
    Calculate the Manhattan distance between the current state and the goal state.

    Parameters:
        state (list of list of int): The current puzzle state.
        target_goal_state (list of list of int): The goal puzzle state.

    Returns:
        int: The Manhattan distance.
    """
    distance = 0
    goal_positions = {value: find_position(target_goal_state, value) for value in range(1, 9)}
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                goal_row, goal_col = goal_positions[state[i][j]]
                distance += abs(i - goal_row) + abs(j - goal_col)
    return distance

def find_position(state, value):
    """
    Find the position of a value in a 2D puzzle state.

    Parameters:
        state (list of list of int): The puzzle state.
        value (int): The value to find.

    Returns:
        tuple: The (row, col) position of the value.
    """
    for i in range(3):
        for j in range(3):
            if state[i][j] == value:
                return i, j
    return None

class AStarSearch:
    """
    Implements the A* search algorithm.
    """
    def search(self, start_initial_state, target_goal_state):
        """
        Perform A* search to find the solution to the 8-Puzzle problem.

        Parameters:
            start_initial_state (list of list of int): The initial state.
            target_goal_state (list of list of int): The goal state.

        Returns:
            PuzzleNode: The solution node if found, otherwise None.
        """
        initial_node = PuzzleNode(start_initial_state, target_goal_state)
        frontier = [initial_node]
        explored = set()
        visited_states = set()
        while frontier:
            current_node = heapq.heappop(frontier)
            if current_node.state == target_goal_state:
                return current_node
            state_tuple = tuple(map(tuple, current_node.state))
            if state_tuple not in visited_states:
                visited_states.add(state_tuple)
                explored.add(state_tuple)
                for neighbor in current_node.get_neighbors():
                    if tuple(map(tuple, neighbor.state)) not in explored:
                        heapq.heappush(frontier, neighbor)
        return None

def is_solvable(puzzle):
    """
    Check if the puzzle is solvable by counting inversions.

    Parameters:
        puzzle (list of list of int): The puzzle state.

    Returns:
        bool: True if solvable, otherwise False.
    """
    flattened_puzzle = [num for row in puzzle for num in row if num != 0]
    inversions = 0
    for i in range(len(flattened_puzzle)):
        for j in range(i + 1, len(flattened_puzzle)):
            if flattened_puzzle[i] > flattened_puzzle[j]:
                inversions += 1
    return inversions % 2 == 0

def print_solution(node):
    """
    Print the solution path from the initial state to the goal state.

    Parameters:
        node (PuzzleNode): The solution node.
    """
    path = []
    move_sequence = []
    while node:
        path.append(node)
        if node.action is not None:
            move_sequence.append(node.action)
        node = node.parent
    path.reverse()
    move_sequence.reverse()

    print(f"It takes {len(move_sequence)} steps to move from the initial state to the goal state. The movement sequence is: {''.join(map(str, move_sequence))}")
    print()

    print("The specific movement steps are as follows:")
    print("Initial state:")
    for row in path[0].state:
        print(row)
    print()

    for i in range(1, len(path)):
        print(f"Step {i}: Move {path[i].action}")
        for row in path[i].state:
            print(row)
        print()

def get_user_input(prompt):
    """
    Get and validate user input for the puzzle state.

    Parameters:
        prompt (str): The prompt message.

    Returns:
        list of list of int: The valid puzzle state input.
    """
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print("Input cannot be empty. Please enter 9 digits.")
            continue
        if len(user_input) != 9 or not user_input.isdigit():
            print("Input must be exactly 9 digits.")
            continue
        if len(set(user_input)) != 9 or not all(char in '012345678' for char in user_input):
            print("Input must contain all numbers from 0 to 8 without repetition.")
            continue
        return [[int(user_input[i * 3 + j]) for j in range(3)] for i in range(3)]

def main():
    """
    Main function to execute the 8-Puzzle solver.
    """
    initial_state = get_user_input("Please enter the 9 numbers of the initial state in sequence (0 represents the blank space): ")
    goal_state = get_user_input("Please enter the 9 numbers of the goal state in sequence (0 represents the blank space): ")

    if initial_state == goal_state:
        print("The initial state and the goal state are the same. No need for search.")
    else:
        if is_solvable(initial_state):
            search_algorithm = AStarSearch()
            solution_node = search_algorithm.search(initial_state, goal_state)
            if solution_node:
                print_solution(solution_node)
            else:
                print("No solution.")
        else:
            print("The puzzle is not solvable.")

if __name__ == "__main__":
    main()
