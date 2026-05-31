import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from scipy import stats
import time
from collections import defaultdict

def points_container(p1, p2, p3, point):
    
    d = 2 * (p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1]))
    if abs(d) < 1e-8: 
        return False # Współliniowość ?
    
    ax = ((p1[0]**2 + p1[1]**2) * (p2[1] - p3[1]) + (p2[0]**2 + p2[1]**2) * (p3[1] - p1[1]) + (p3[0]**2 + p3[1]**2) * (p1[1] - p2[1])) / d
    ay = ((p1[0]**2 + p1[1]**2) * (p3[0] - p2[0]) + (p2[0]**2 + p2[1]**2) * (p1[0] - p3[0]) + (p3[0]**2 + p3[1]**2) * (p2[0] - p1[0])) / d

   
    r = (ax - p1[0])**2 + (ay - p1[1])**2
    dist = (point[0] - ax)**2 + (point[1] - ay)**2

    # Zwracamy porównanie z błędu 
    return dist <= r + 1e-5


def bowyer_watson(points):
    min_x, min_y = np.min(points, axis=0)
    max_x, max_y = np.max(points, axis=0)

    dx, dy = max_x - min_x, max_y - min_y
    max_area = max(dx, dy)
    
    #super trójkąt
    p1 = [min_x - max_area, min_y - max_area]
    p2 = [min_x - max_area, max_y + 2 * max_area]
    p3 = [max_x + 2 * max_area, min_y - max_area]

    n = len(points)
    super_triangle = np.array([p1, p2, p3])
    all_points = np.append(points, super_triangle, axis=0)

    triangulation = [(n, n+1, n+2)] 

    for i, xy in enumerate(points):
        wrong_triangles = []
        for t in triangulation:
            if points_container(all_points[t[0]], all_points[t[1]], all_points[t[2]], xy):
                wrong_triangles.append(t)

        #szukanie zewnętrznych krawędzi
        edge_counts = defaultdict(int) #słownik który przypisuje deafaultową wartośc nawet jako jeszcze nie wie co to 
        
        for t in wrong_triangles:
            edges = [
                tuple(sorted((t[0], t[1]))),
                tuple(sorted((t[1], t[2]))),
                tuple(sorted((t[2], t[0])))
            ]
            for e in edges:
                edge_counts[e] += 1
                
        # Bierzemy tylko krawędzie występujące równe 1 raz
        polygon = [edge for edge, count in edge_counts.items() if count == 1]

    
        for t in wrong_triangles:
            triangulation.remove(t)
        
        for edge in polygon:
            triangulation.append((edge[0], edge[1], i)) 
    
   
    final_triangulation = []
    for t in triangulation:
        if t[0] < n and t[1] < n and t[2] < n:
            final_triangulation.append(t)

    return np.array(final_triangulation)


def calculate_triangle_quality(p1, p2, p3):
    a = np.linalg.norm(p2 - p1)
    b = np.linalg.norm(p3 - p2)
    c = np.linalg.norm(p1 - p3)
    s = (a + b + c) / 2.0
    
    heron = s * (s - a) * (s - b) * (s - c)
    if heron <= 1e-10: 
        return float('inf')
    
    quality = (a * b * c * s) / (8 * heron) #miara jakości R/2r
    return quality

def triangulation_analyze(points, simplices):
    qualities = []
    for simplex in simplices:
        p1, p2, p3 = points[simplex[0]], points[simplex[1]], points[simplex[2]]
        q = calculate_triangle_quality(p1, p2, p3)
        if q != float('inf'):
            qualities.append(q)
            
    qualities = np.array(qualities)
    rounded_q = np.round(qualities, 2)
    mode_result = stats.mode(rounded_q, keepdims=True)
    mode_val = mode_result.mode[0]
    
    stats_data = {
        "count": len(simplices),
        "median": np.median(qualities),
        "mode": mode_val,
        "qualities": qualities
    }
    return stats_data


if __name__ == "__main__":
    
    points = np.random.rand(50, 2) * 100

    # SciPy
    start_time_scipy = time.perf_counter()
    tri_scipy = Delaunay(points)
    time_scipy = time.perf_counter() - start_time_scipy
    stats_scipy = triangulation_analyze(points, tri_scipy.simplices)

    # Bowyer watson 
    start_time_bw = time.perf_counter()
    tri_custom_simplices = bowyer_watson(points)
    time_bw = time.perf_counter() - start_time_bw
    stats_bw = triangulation_analyze(points, tri_custom_simplices)

    
    print("SciPy ")
    print(f"Czas wykonania: {time_scipy:.6f} s")
    print(f"Liczba sympleksów: {stats_scipy['count']}")
    print(f"Mediana jakości: {stats_scipy['median']:.4f}")
    print(f"Moda jakości: {stats_scipy['mode']:.2f}")

    print("\nBowyer-Watson")
    print(f"Czas wykonania: {time_bw:.6f} s")
    print(f"Liczba sympleksów: {stats_bw['count']}")
    print(f"Mediana jakości: {stats_bw['median']:.4f}")
    print(f"Moda jakości: {stats_bw['mode']:.2f}")


    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    axs[0, 0].triplot(points[:,0], points[:,1], tri_scipy.simplices)
    axs[0, 0].plot(points[:,0], points[:,1], 'o', color='red')
    axs[0, 0].set_title('Biblioteka (SciPy)')

    axs[0, 1].triplot(points[:,0], points[:,1], tri_custom_simplices)
    axs[0, 1].plot(points[:,0], points[:,1], 'o', color='red')
    axs[0, 1].set_title('Własny Algorytm (Bowyer-Watson)')

  
    custom_max=10.0
    bins = np.linspace(1,custom_max, 20)
    axs[1,0].set_xlim(1, custom_max)
    axs[1,1].set_xlim(1, custom_max)

    axs[1, 0].hist(stats_scipy['qualities'], bins=bins, color='skyblue', edgecolor='black')
    axs[1, 0].set_title('SciPy')

    axs[1, 1].hist(stats_bw['qualities'], bins=bins, color='lightgreen', edgecolor='black')
    axs[1, 1].set_title('Bowyer-watson')

    plt.tight_layout()
    plt.show()