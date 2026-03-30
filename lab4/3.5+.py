import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpath

# WCZYTYWANIE Z PLIKU 
def load_craft_figure(filename):
    try:
        return np.loadtxt(filename, skiprows=1)
    except Exception as e:
        print(f"Error while loading craft1_ksztalt.txt: {e}")
        return None
    
def load_missiles(filename):
    try: 
        return np.loadtxt(filename)
    except Exception as e:
        print(f"Error while loading missiles.txt: {e}")
        return None
    
def load_space_craft(filename):
    try:
        data = np.loadtxt(filename)
        if data.shape == (2, 2):
            return data[0], data[1]
        else: 
            print("Wrong shape in space_craft.txt")
            return None, None
    except Exception as e:
        print(f"Error while loading space_craft.txt: {e}")
        return None, None
    
#GEOMETRIA
def bounding_box(points):
    min_coords = np.min(points, axis=0)
    max_coords = np.max(points, axis=0)
    return np.array([min_coords[0], min_coords[1], max_coords[0], max_coords[1]])

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0: return 0
    return 1 if val > 0 else 2

def jarvis(points):
    n = len(points)
    if n < 3: return points
    
    otoczka = []
    l = 0
    for i in range(1, n):
        if points[i][0] < points[l][0]:
            l = i
            
    p = l
    while True:
        otoczka.append(points[p])
        q = (p + 1) % n
        for i in range(n):
            if orientation(points[p], points[i], points[q]) == 2:
                q = i
        p = q
        if p == l: break
    return otoczka

#SYMULACJA 
def simulation():

    craft_cloud = load_craft_figure("craft1_ksztalt.txt")
    ship_data = load_space_craft("space_craft1.txt")
    missiles = load_missiles("missiles1.txt")

    if craft_cloud is None or ship_data[0] is None or missiles is None:
        print("Nie wczytano wszystkich danych. Zamykam program.")
        return

    ship_position, ship_velocity = ship_data
    
    plt.close("all")
    fig, ax = plt.subplots(figsize=(8,8))
    
    # Pętla czasu
    time_steps = np.arange(0.0, 2.1, 0.1)

    for current_time in time_steps:
        ax.clear()
        ax.set_xlim(-200, 1000)
        ax.set_ylim(-200,1000)
        ax.set_title(f"Czas: {current_time:.1f} s")

        # Ruch statku
        current_ship_position = ship_position + ship_velocity * current_time
        current_craft_points = craft_cloud + current_ship_position  # przesuwa każdy punkt statku o wartosc obliczona wyzej

        # Otoczka (Jarvis)
        points_as_list = current_craft_points.tolist()
        my_hull_points = jarvis(points_as_list)

        if my_hull_points:
            h_plot = my_hull_points + [my_hull_points[0]] #zamyka wielokat 
            hx, hy = zip(*h_plot) #rozdziela punkty na x i y osobno 
            ax.plot(hx, hy, 'b-', label="My Hull - statek")
            
        # Bounding Box rysowanie
        b_box = bounding_box(current_craft_points)
        rect = plt.Rectangle((b_box[0], b_box[1]), b_box[2]-b_box[0], b_box[3]-b_box[1], linewidth=1, edgecolor='g', facecolor='none', linestyle='--', label='Box')
        ax.add_patch(rect)

        # Cała chmura punktów statku
        ax.scatter(current_craft_points[:, 0], current_craft_points[:, 1], color='pink', s=5, alpha=0.5)

        # Obliczanie ruchu pocisków i rysowanie
        #warunek na to żeby stworzyc tablie dwuwymiarową
        if len(missiles.shape) == 1:
            m_list = missiles.reshape(1, -1)
        else:
            m_list = missiles

        for i, m in enumerate(m_list):
            if current_time >= m[0]:
                # Wyliczamy, gdzie pocisk jest TERAZ
                dt = current_time - m[0]
                m_x = m[1] + m[3] * dt #miejsce startu + (prędkość pocisku * czas lotu)
                m_y = m[2] + m[4] * dt
                
                # Rysowanie pocisku
                ax.scatter(m_x, m_y, color='green', s=50, marker='x')

                # Czy punkt pocisku jest wewnątrz zielonego prostokąta
                if (b_box[0] <= m_x <= b_box[2]) and (b_box[1] <= m_y <= b_box[3]):
                    
                    # Możliwa kolizja
                    if my_hull_points:
                        hull_path = mpath.Path(my_hull_points + [my_hull_points[0]]) # domknięta ścieżkę otoczki
                        # czy punkt pocisku znajduje się W ŚRODKU kadłuba?
                        if hull_path.contains_point((m_x, m_y)):
                            ax.scatter(m_x, m_y, color='red', s=400, marker='x')
                            ax.text(m_x, m_y + 40, "Kolizja", color='red', fontsize=16, fontweight='bold')
        
        ax.legend(loc='upper right')
        ax.grid(True, linestyle=':', alpha=0.5)
        
        plt.draw()
        plt.pause(0.1)
    
    plt.show(block=True)
if __name__ == "__main__":
    simulation()