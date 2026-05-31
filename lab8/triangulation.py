import numpy as np
from scipy import stats
from scipy.spatial import Delaunay
import time
import matplotlib.pyplot as plt
import matplotlib.tri as mtri

def calculate_triangle_quality(p1, p2, p3):
    a=np.linalg.norm(p2-p1) #obliczanie normy
    b=np.linalg.norm(p3-p2)
    c=np.linalg.norm(p1-p3)

    s=(a+b+c)/2.0

    heron = s*(s-a)*(s-b)*(s-c)
    if heron <= 1e-10:
        return float('inf')
    
    quality = (a*b*c*s)/(8*heron) #obliczanie wzoru na podstawie stosunku R/2r
    return quality

def triangulation_analyze(points, simplices):
    qualities=[]

    for simplex in simplices:
        p1, p2, p3 = points[simplex[0]], points[simplex[1]], points[simplex[2]]
        q = calculate_triangle_quality(p1, p2, p3)

        if q!=float('inf'):
            qualities.append(q)
        
    qualities=np.array(qualities)
    rounded_q=np.round(qualities,2)
    mode_result=stats.mode(rounded_q, keepdims =True)
    mode_val = mode_result.mode[0]

    stats_data={
        "count": len(simplices),
        "median": np.median(qualities),
        "mode" : mode_val,
        "qualities": qualities
    }
    return stats_data


#Generowanie danych
np.random.seed(1) #zamraża losowość punktów
points = np.random.rand(50,2)*100

#Metoda1: Delaunay - SciPy
start_time_scipy = time.perf_counter()
tri_scipy = Delaunay(points)
time_scipy= time.perf_counter() - start_time_scipy

stats_scipy = triangulation_analyze(points, tri_scipy.simplices)

#Metoda2: Triangulation- Matplotlib
start_time_mpl=time.perf_counter()
tri_mpl = mtri.Triangulation(points[:, 0], points[:, 1])
time_mpl = time.perf_counter() - start_time_mpl

stats_mpl = triangulation_analyze(points, tri_mpl.triangles)


print("--- Wyniki dla Metody 1: SciPy ---")
print(f"Czas wykonania: {time_scipy:.6f} s")
print(f"Liczba sympleksów: {stats_scipy['count']}")
print(f"Mediana jakości: {stats_scipy['median']:.4f}")
print(f"Moda jakości: {stats_scipy['mode']:.2f}")

print("\n--- Wyniki dla Metody 2: Matplotlib ---")
print(f"Czas wykonania: {time_mpl:.6f} s")
print(f"Liczba sympleksów: {stats_mpl['count']}")
print(f"Mediana jakości: {stats_mpl['median']:.4f}")
print(f"Moda jakości: {stats_mpl['mode']:.2f}")


#Rysowanie wykresów
fig, axs = plt.subplots(2,2, figsize=(12,10))

#triplot rystuje siatkę
axs[0,0].triplot(points[:, 0], points[:, 1], tri_scipy.simplices)
axs[0,0].plot(points[:, 0], points[:, 1],'o', color = 'red')
axs[0, 0].set_title('Triangulacja - SciPy')

axs[0, 1].triplot(points[:,0], points[:,1], tri_mpl.triangles)
axs[0, 1].plot(points[:,0], points[:,1], 'o', color='red')
axs[0, 1].set_title('Triangulacja - Matplotlib')


#linspace dzieli oś na 20 równych bins
#percentile obcina 5% najbardziej skrajnych trójkątów
bins = np.linspace(1, max(np.percentile(stats_scipy['qualities'], 95), np.percentile(stats_mpl['qualities'], 95)), 20)

axs[1, 0].hist(stats_scipy['qualities'], bins=bins, color='blue', edgecolor='black')
axs[1, 0].set_title('Histogram jakości - SciPy')
axs[1, 0].set_xlabel('Jakość')
axs[1, 0].set_ylabel('Liczba trójkątów')

axs[1, 1].hist(stats_mpl['qualities'], bins=bins, color='green', edgecolor='black')
axs[1, 1].set_title('Histogram jakości - Matplotlib')
axs[1, 1].set_xlabel('Jakość')
axs[1, 1].set_ylabel('Liczba trójkątów')
plt.show()