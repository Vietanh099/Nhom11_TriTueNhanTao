import heapq

def read_input(filename):
    edges = {}
    heuristics = {}
    start, goal = None, None

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) == 3 and parts[2].isdigit():
                u, v, cost = parts[0], parts[1], int(parts[2])
                if u not in edges:
                    edges[u] = []
                edges[u].append((v, cost))
            elif len(parts) == 2 and parts[1].isdigit():
                heuristics[parts[0]] = int(parts[1])
            elif parts[0] == "START":
                start = parts[1]
            elif parts[0] == "GOAL":
                goal = parts[1]

    return edges, heuristics, start, goal

def a_star(edges, heuristics, start, goal, output_file):
    open_list = []
    heapq.heappush(open_list, (heuristics[start], 0, start, [start]))
    closed_list = set()

    with open(output_file, "w", encoding="utf-8") as out:
        out.write("Bảng các bước thực hiện A*:\n")
        out.write("Node\tg\t h\t f\t Path\n")

        while open_list:
            f, g, node, path = heapq.heappop(open_list)
            out.write(f"{node}\t{g}\t{heuristics[node]}\t{f}\t{'->'.join(path)}\n")

            if node == goal:
                out.write("\nKết quả:\n")
                out.write(f"Đường đi: {' -> '.join(path)}\n")
                out.write(f"Chi phí: {g}\n")
                return

            closed_list.add(node)

            for neighbor, cost in edges.get(node, []):
                if neighbor in closed_list:
                    continue
                g_new = g + cost
                f_new = g_new + heuristics[neighbor]
                heapq.heappush(open_list, (f_new, g_new, neighbor, path + [neighbor]))

    # Nếu không tìm thấy
    with open(output_file, "a", encoding="utf-8") as out:
        out.write("\nKhông tìm thấy đường đi!\n")

if __name__ == "__main__":
    edges, heuristics, start, goal = read_input(r"./AStar_NhanhCan/input.txt")
    a_star(edges, heuristics, start, goal, "./AStar_NhanhCan/output.txt")