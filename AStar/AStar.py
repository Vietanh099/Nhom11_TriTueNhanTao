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
                edges.setdefault(u, []).append((v, cost))
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
        out.write("Bảng các bước thực hiện A*:\n\n")
        out.write("{:<4} {:<4} {:<8} {:<6} {:<6} {:<6} {}\n".format("TT", "TTK", "k(u,v)", "h(v)", "g(v)", "f(v)", "Danh sách L / Kết quả"))
        out.write("-------------------------------------------------------------------------------\n")

        while open_list:
            f, g, node, path = heapq.heappop(open_list)
            h_val = heuristics.get(node, 0)

            # Nếu đến đích: in kết quả ngay trong bảng
            if node == goal:
                result_str = f"Đường đi: {'->'.join(path)}, Chi phí: {g}"
                out.write("{:<4} {:<4} {:<8} {:<6} {:<6} {:<6} {}\n".format(node, "-", "-", h_val, g, "-", result_str))
                out.write("-------------------------------------------------------------------------------\n")
                return

            closed_list.add(node)
            expanded_nodes = []

            # Mở rộng node hiện tại
            for neighbor, cost in edges.get(node, []):
                if neighbor in closed_list:
                    continue
                g_new = g + cost
                h_new = heuristics.get(neighbor, 0)
                f_new = g_new + h_new
                heapq.heappush(open_list, (f_new, g_new, neighbor, path + [neighbor]))
                expanded_nodes.append((neighbor, cost, h_new, g_new, f_new))

            # Tạo Danh sách L: gộp theo node, lấy f nhỏ nhất cho mỗi node, sau đó lấy top 4
            best_f_by_node = {}
            for f_val, _, n, _ in open_list:
                if n not in best_f_by_node or f_val < best_f_by_node[n]:
                    best_f_by_node[n] = f_val
            danh_sach_L_sorted = sorted(best_f_by_node.items(), key=lambda x: x[1])[:4]
            danh_sach_L_str = ", ".join([f"{n}{fv}" for n, fv in danh_sach_L_sorted])

            # In các dòng mở rộng: chỉ dòng đầu có TT và Danh sách L
            for i, (neighbor, cost, h_new, g_new, f_new) in enumerate(expanded_nodes):
                tt_val = node if i == 0 else ""
                dsL_val = danh_sach_L_str if i == 0 else ""
                out.write("{:<4} {:<4} {:<8} {:<6} {:<6} {:<6} {}\n".format(tt_val, neighbor, cost, h_new, g_new, f_new, dsL_val))

        out.write("-------------------------------------------------------------------------------\n")
        out.write("\nKhông tìm thấy đường đi!\n")


if __name__ == "__main__":
    edges, heuristics, start, goal = read_input(r"./AStar/input.txt")
    a_star(edges, heuristics, start, goal, "./AStar/output.txt")