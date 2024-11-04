from copy import deepcopy

# Hàm kiểm tra trạng thái hiện tại có phải trạng thái đích không
def is_goal(state, goal):
    return state == goal

# Hàm tìm vị trí của ô trống (được biểu diễn bằng 0)
def find_empty(state):
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 0:
                return i, j

# Hàm hoán đổi vị trí của ô trống và ô liền kề
def swap(state, x1, y1, x2, y2):
    new_state = deepcopy(state)
    new_state[x1][y1], new_state[x2][y2] = new_state[x2][y2], new_state[x1][y1]
    return new_state

# Hàm sinh ra các trạng thái con từ trạng thái hiện tại
def get_neighbors(state):
    neighbors = []
    x, y = find_empty(state)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Lên, Xuống, Trái, Phải

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < len(state) and 0 <= new_y < len(state[0]):
            new_state = swap(state, x, y, new_x, new_y)
            neighbors.append(new_state)

    return neighbors

# Thuật toán DFS
def dfs(start, goal, depth_limit=50):
    stack = [(start, [])]  # Stack chứa trạng thái và đường đi hiện tại
    visited = set()

    while stack:
        current_state, path = stack.pop()

        # Chuyển trạng thái hiện tại thành tuple để có thể lưu vào set
        current_tuple = tuple(map(tuple, current_state))

        if current_tuple in visited:
            continue

        visited.add(current_tuple)

        if is_goal(current_state, goal):
            return path + [current_state]  # Trả về đường đi từ start đến goal

        if len(path) < depth_limit:  # Giới hạn độ sâu để tránh lặp vô tận
            for neighbor in get_neighbors(current_state):
                stack.append((neighbor, path + [current_state]))

    return None  # Nếu không tìm thấy giải pháp

# Hàm in ra trạng thái của puzzle
def print_state(state):
    for row in state:
        print(' '.join(str(x) for x in row))
    print()

# Ví dụ chạy với puzzle 3x3 (8-puzzle)
start_state = [
    [1, 2, 3],
    [4, 0, 5],  # 0 là ô trống
    [6, 7, 8]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

path = dfs(start_state, goal_state)

if path:
    print("Đã tìm thấy đường đi đến trạng thái đích:")
    for step in path:
        print_state(step)
else:
    print("Không tìm thấy giải pháp.")