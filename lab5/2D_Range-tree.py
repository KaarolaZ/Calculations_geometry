import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# Węzeł dla wewnętrznych drzew Y
class Node1D:
    def __init__(self, point):
        self.point = point #(x,y)
        self.right = None
        self.left = None

class Node2D:
    def __init__(self, point, min_x, max_x):
        self.point = point 
        self.min_x = min_x
        self.max_x = max_x
        self.right = None
        self.left = None
        self.y_tree = None # Korzeń dodatkowego drzewa Y dla tego poddrzewa
        
def build_1D_tree(points_sorted_by_y):
    if not points_sorted_by_y: return None

    mediana = len(points_sorted_by_y) //2
    root = Node1D(points_sorted_by_y[mediana])

    root.left = build_1D_tree(points_sorted_by_y[:mediana])
    root.right = build_1D_tree(points_sorted_by_y[mediana+1:])

    return root

def build_2D_tree(points_sorted_by_x):
    if not points_sorted_by_x: return None

    mediana = len(points_sorted_by_x) //2
    #węzeł zapisujący od razu, jaki zakres X obejmuje to poddrzewo
    node = Node2D(points_sorted_by_x[mediana], points_sorted_by_x[0][0], points_sorted_by_x[-1][0])

    node.left = build_2D_tree(points_sorted_by_x[:mediana])
    node.right = build_2D_tree(points_sorted_by_x[mediana+1:])

    # Sortujemy wszystkie punkty z tego poddrzewa po osi Y i budujemy z nich drzewo Y
    points_sorted_by_y = sorted(points_sorted_by_x, key=lambda p:p[1])
    node.y_tree = build_1D_tree(points_sorted_by_y)
    return node

def searching_for_range(node, y_min, y_max, result):
    if not node: return None

    if y_min <= node.point[1] <= y_max:
        result.append(node.point)

    if node.point[1] > y_min:
        searching_for_range(node.left, y_min, y_max, result)

    if node.point[1] < y_max:
        searching_for_range(node.right, y_min, y_max, result)

def searching_2D_tree(node, x_min, x_max, y_min, y_max, result):
    if not node: return None

    # Jeśli poddrzewo w całości mieści się w naszym zakresie X,
    # nie musimy już martwić się osią X. Przeszukujemy tylko jego drzewo Y.
    if x_min <= node.min_x and node.max_x <= x_max:
        searching_for_range(node.y_tree, y_min, y_max, result)
        return
    
    # W przeciwnym razie sprawdzamy punkt w bieżącym węźle 
    if(x_min <= node.point[0] <= x_max) and (y_min <= node.point[1] <= y_max):
        result.append(node.point)

    # Idziemy w lewo, jeśli jest tam szansa na znalezienie czegoś >= x_min
    if node.left and x_min <=node.left.max_x:
        searching_2D_tree(node.left, x_min, x_max, y_min, y_max, result)

    # Idziemy w prawo, jeśli jest szansa na znalezienie czegoś <= x_max
    if node.right and x_max >= node.right.min_x:
        searching_2D_tree(node.right, x_min, x_max, y_min, y_max, result)


def visualization_2D(points, x_min, x_max, y_min, y_max, found):
    plt.figure(figsize=(8,8))
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    plt.scatter(xs, ys, c='pink', alpha= 0.5, label='All points')

    # Rysowanie prostokąta
    rect = patches.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, 
                             linewidth=2, color='blue', alpha=0.2)
    plt.gca().add_patch(rect)

    # Zaznaczanie znalezionych punktów
    if found:
        fx = [p[0] for p in found]
        fy = [p[1] for p in found]
        plt.scatter(fx, fy, c='red', label='Znalezione punkty')
        
    plt.title(f'Wyszukiwanie 2D: X[{x_min}-{x_max}], Y[{y_min}-{y_max}]')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True, linestyle='-', alpha=0.6)
    plt.legend(loc='upper right')
    plt.show()


#pomiar pamięci
def count_total_nodes(node):
    if not node: return 0

    def count_y(y_node):
        if not y_node: return 0
        return 1+ count_y(y_node.left) + count_y(y_node.right)

    y_tree_size = count_y(node.y_tree)
    # Pamięć = 1 (węzeł X) + rozmiar jego drzewa Y + to samo dla dzieci
    return 1 + y_tree_size + count_total_nodes(node.left) + count_total_nodes(node.right)

def visualize_memory_usage():
    sizes = [10, 50, 100, 200, 300, 500, 800, 1000]
    memory_usage = []
    
    for n in sizes:
        pts = list(set([tuple(p) for p in np.random.randint(0, 1000, size=(n, 2))]))
        pts.sort(key=lambda p: p[0])
        tree = build_2D_tree(pts)
        memory_usage.append(count_total_nodes(tree))
        
    plt.figure(figsize=(8, 4))
    plt.plot(sizes, memory_usage, color='blue', linestyle='-')
    plt.title('Złożoność pamięciowa Drzewa 2D')
    plt.xlabel('Liczba punktów')
    plt.ylabel('Pamięć')
    plt.grid(True, linestyle='-', alpha=0.6)
    plt.show()

if __name__ == "__main__":
  
        n_2D = np.random.randint(20, 101)
        set_2 = list(set(tuple(p) for p in np.random.randint(0, 101, size=(n_2D, 2))))
        # Drzewo X MUSI być  posortowane po X
        set_2.sort(key=lambda p: p[0])
        
        root_2d = build_2D_tree(set_2)
        
        # Parametry zapytaniack
        x1, x2 = 20, 60
        y1, y2 = 10, 90
        found_points = []
        
        searching_2D_tree(root_2d, x1, x2, y1, y2, found_points)
        print(f"Znaleziono {len(found_points)} punktów w zadanym oknie.")
        
        visualization_2D(set_2, x1, x2, y1, y2, found_points)
        
        visualize_memory_usage()