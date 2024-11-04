import heapq

# Tọa độ các hướng đi trong lưới (lên, xuống, trái, phải)
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def a_star(start, goal, grid):
    # Hàm heuristic: sử dụng khoảng cách Manhattan
    def heuristic(cell, goal):
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

    # Khởi tạo danh sách mở (open list) với điểm bắt đầu
    open_list = []
    heapq.heappush(open_list, (0, start))

    # Khởi tạo từ điển lưu chi phí từ điểm bắt đầu tới mỗi ô
    g_cost = {start: 0}

    # Khởi tạo từ điển lưu cha của mỗi ô để truy vết đường đi
    came_from = {start: None}

    while open_list:
        # Lấy ô có giá trị f(n) nhỏ nhất từ open list
        _, current = heapq.heappop(open_list)

        # Nếu đã đến đích thì dừng
        if current == goal:
            return reconstruct_path(came_from, current)

        # Xét các ô lân cận
        for direction in DIRECTIONS:
            neighbor = (current[0] + direction[0], current[1] + direction[1])

            # Kiểm tra xem ô này có trong lưới và không phải chướng ngại vật
            if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and grid[neighbor[0]][neighbor[1]] == 0:
                tentative_g_cost = g_cost[current] + 1  # Chi phí từ start đến neighbor thông qua current

                # Nếu chi phí này thấp hơn chi phí hiện tại đến ô lân cận
                if neighbor not in g_cost or tentative_g_cost < g_cost[neighbor]:
                    g_cost[neighbor] = tentative_g_cost
                    f_cost = tentative_g_cost + heuristic(neighbor, goal)  # f(n) = g(n) + h(n)
                    heapq.heappush(open_list, (f_cost, neighbor))
                    came_from[neighbor] = current

    return None  # Không tìm thấy đường đi

# Hàm truy vết lại đường đi từ điểm cuối về điểm đầu
def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from and came_from[current] is not None:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

# Ví dụ sử dụng
grid = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 1, 0, 0]
]

start = (0, 0)
goal = (4, 4)

path = a_star(start, goal, grid)

if path:
    print("Đường đi ngắn nhất:", path)
else:
    print("Không tìm thấy đường đi!")