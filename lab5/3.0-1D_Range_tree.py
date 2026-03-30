import numpy as np
import matplotlib.pyplot as plt

def generate_points():
    
    #ilosc punktow
    n_1D = np.random.randint(20, 101)
    n_2D = np.random.randint(20, 101)

    set_1 = list(set(np.random.randint(0, 101, n_1D)))
    set_2 = list(set(tuple(p) for p in np.random.randint(0, 101, size=(n_2D, 2))))
    
    print(f"Generated {len(set_1)} unique points 1D.")
    print(f"Generated {len(set_2)} unique points 2D.")
    
    return set_1, set_2


class Node:
    def __init__(self, value):
        self.value = value
        self.right = None
        self.left = None

def build_1D_range_tree(points):
    if not points: return None

    mediana = len(points) //2
    root = Node(points[mediana])

    root.left = build_1D_range_tree(points[:mediana])
    root.right = build_1D_range_tree(points[mediana+1:])

    return root

def searching_for_range(node, x_min, x_max, result):
    if not node: return None

    if x_min <= node.value <= x_max:
         result.append(node.value)

    if node.value > x_min:
        searching_for_range(node.left, x_min, x_max, result)

    if node.value < x_max:
        searching_for_range(node.right, x_min, x_max, result)

    
def visualization_1D(set_1, x_min, x_max, f_points):
    plt.figure(figsize = (10, 3))

    plt.scatter(set_1, np.zeros_like(set_1), color = 'blue', alpha =0.5, label= 'All points', zorder = 2)
    plt.axvspan(x_min, x_max, color ='yellow', alpha = 0.5, label = f"Range [{x_min}, {x_max}]")

    if f_points:
        plt.scatter(f_points, np.zeros_like(f_points), color='red', alpha = 0.5, label="Found points", zorder=3)

    plt.yticks([]) # Ukrywamy oś Y, bo pracujemy w 1D
    plt.xlabel('X')
    plt.title('Visualization of range tree 1D')
    plt.legend()
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()  


if __name__ =="__main__":
    points_1D, points_2D = generate_points()

    points_1D.sort()
    tree_root = build_1D_range_tree(points_1D)

    range_min = int(input("Start of the range: "))
    range_max = int(input("End of the range: "))

    found_points =[]
    searching_for_range(tree_root, range_min, range_max, found_points)

    print(f"\nSzukany przedzial: [{range_min}, {range_max}]")
    print(f"Znaleziono {len(found_points)} punktow: {sorted(found_points)}")

    visualization_1D(points_1D, range_min, range_max, found_points)