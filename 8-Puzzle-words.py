import heapq

color_to_number = {
    "blue": 1, "green": 2, "orange": 3,
    "purple": 4, "pink": 5, "red": 6,
    "yellow": 7, "cyan": 8, "blank": 0
}

number_to_color = {v: k for k, v in color_to_number.items()}

class PuzzleNode:
    def __init__(self, current_state, target_state, parent=None, action=None, cost=0):
        self.state = current_state
        self.goal_state = target_state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = self.calculate_heuristic()
        self.total_cost = self.cost + self.heuristic

    def calculate_heuristic(self):
        return calculate_manhattan_distance(self.state, self.goal_state)

    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def get_neighbors(self):
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
    distance = 0
    goal_positions = {value: find_position(target_goal_state, value) for value in range(1, 9)}
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                goal_row, goal_col = goal_positions[state[i][j]]
                distance += abs(i - goal_row) + abs(j - goal_col)
    return distance

def find_position(state, value):
    for i in range(3):
        for j in range(3):
            if state[i][j] == value:
                return i, j
    return None

class AStarSearch:
    def search(self, start_initial_state, target_goal_state):
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
    flattened_puzzle = [num for row in puzzle for num in row if num != 0]
    inversions = 0
    for i in range(len(flattened_puzzle)):
        for j in range(i + 1, len(flattened_puzzle)):
            if flattened_puzzle[i] > flattened_puzzle[j]:
                inversions += 1
    return inversions % 2 == 0

def print_solution(node):
    path = []
    move_sequence = []
    while node:
        path.append(node)
        if node.action is not None:
            move_sequence.append(number_to_color[node.action])
        node = node.parent
    path.reverse()
    move_sequence.reverse()

    print(f"It takes {len(move_sequence)} steps to move from the initial state to the goal state. The movement sequence is: {' '.join(move_sequence)}")
    print()

    print("The specific movement steps are as follows:")
    print("Initial state:")
    for row in path[0].state:
        print([number_to_color[num] for num in row])
    print()

    for i in range(1, len(path)):
        print(f"Step {i}: Move {number_to_color[path[i].action]}")
        for row in path[i].state:
            print([number_to_color[num] for num in row])
        print()


def get_user_input(prompt):
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print("Input cannot be empty. Please enter 9 colors separated by spaces.")
            continue
        colors = user_input.split()
        if len(colors) != 9:
            print("Input must contain exactly 9 colors.")
            continue
        if len(set(colors)) != 9 or not all(color in color_to_number for color in colors):
            print("Input must contain all specified colors without repetition.")
            continue
        return [[color_to_number[colors[i * 3 + j]] for j in range(3)] for i in range(3)]

def main():
    initial_state = get_user_input("Please enter the 9 colors of the initial state in sequence (e.g., blue green orange purple pink red yellow cyan blank): ")
    goal_state = get_user_input("Please enter the 9 colors of the goal state in sequence (e.g., blue green orange purple pink red yellow cyan blank): ")

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
