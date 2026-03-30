import math
import matplotlib.pyplot as plt

def file_load(plik):
    points = []
    try:
        with open(plik, 'r') as f:
            lines = f.readlines()
            if not lines:
                return []
            num_points = int(lines[0].strip())
            for line in lines[1:]:
                coords = line.split()
                if len(coords) == 2:
                    points.append((float(coords[0]), float(coords[1])))
    except FileNotFoundError:
        print(f"Błąd: Plik {plik} nie istnieje.")
    return points

def orientation(p, q ,r): # będzie sprawdzać czy puknt buduje zew ściane czy jest wewnątrz
    val = (q[1]- p[1])*(r[0] - q[0]) - (q[0]-p[0])*(r[1]-q[1])
    if val ==0: return 0
    return 1 if val>0 else 2

def distance(p1, p2):
    return  (((p2[0]-p1[0])**2)+((p2[1]-p1[0])**2))

def jarvis(points):
    n = len(points)
    if n<3:
        return points
    
    otoczka = []
    #najbardziej lewy punkt
    l =0
    for i in range(1, n):
        if points[i][0] <points[l][0]:
            l=i
    
    p =l
    while True:
        otoczka.append(points[p])
        q = (p+1) % n #chroni przed wyjściem poza zakres tablicy
        for i in range(n):
            if orientation(points[p], points[i], points[q]) ==2:
                q=i

        p=q
        if p == l: break
    return otoczka

def graham(points):
    n = len(points)
    if n<3:
        return points
    
    p0 =min(points, key=lambda p : (p[1], p[0])) # najniższa współrzędna y

    def angle(p):
        return math.atan2(p[1]- p0[1], p[0]-p0[0])
    
    sorted_points = sorted(points, key = lambda p: (angle(p), distance(p0, p)))
    otoczka = [sorted_points[0], sorted_points[1], sorted_points[2]]

    for i in range(3, n):
        while len(otoczka)>1 and orientation(otoczka[-2], otoczka[-1], sorted_points[i]) !=2:
            otoczka.pop()
        otoczka.append(sorted_points[i])

    return otoczka
        

def visualization(points, otoczka_jarvis, otoczka_graham):
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)#dzieli okno na siatke - 1 wiersz i 2 kolumny i rysuj w pierwszej z nich
    px, py =zip(*points) # robi dwie osobne listy dla X i Y
    plt.scatter(px, py, color='gray', alpha=0.5, label ='Punkty')
    ox, oy = zip(*(otoczka_jarvis + [otoczka_jarvis[0]])) # Zamknięcie pętli
    plt.plot(ox, oy, 'r-', linewidth=2, label='Otoczka')
    plt.title("Jarvis")
    plt.legend()

    plt.subplot(1,2,2)
    plt.scatter(px, py, color='blue', alpha=0.5, label='Punkty')
    ox, oy = zip(*(otoczka_graham + [otoczka_graham[0]]))
    plt.plot(ox, oy, 'b-', linewidth=2, label ='Otoczka')
    plt.title("Graham")
    plt.legend()


    plt.tight_layout()
    plt.show()


#points = file_load("ksztalt_2.txt")
#points = file_load("ksztalt_3.txt")
points = file_load("ksztalt_moj.txt")
otoczka_j = jarvis(points)
otoczka_g = graham(points)
print(f"Liczba punktów otoczki (Jarvis): {len(otoczka_j)}")
print(f"Liczba punktów otoczki (Graham): {len(otoczka_g)}")

visualization(points, otoczka_j, otoczka_g)