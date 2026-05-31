from svgpathtools import svg2paths
import matplotlib.pyplot as plt


# Ekstrakcja Konturu (Z filtrem na tło)
def extract_loops_from_svg(svg_path, num_nodes_per_loop=40):
    paths, attributes = svg2paths(svg_path)
    if not paths:
        raise ValueError("Nie znaleziono ścieżek w pliku!")

    all_loops = []
    
    for path in paths: 
        if path.length() < 10:
            continue
        # Rozbijamy na pod-ścieżki (ciało, oczy)
        subpaths = path.continuous_subpaths()
        
        for subpath in subpaths:
            nodes = []
            for i in range(num_nodes_per_loop):
                t = i / float(num_nodes_per_loop) #t rośnie od 0 do 1 i pobiera liczbę punktów
                pt = subpath.point(t)
                nodes.append((pt.real, -pt.imag)) # Odwracamy Y dla wykresu
                
            nodes.reverse() 
            all_loops.append(nodes)
            
    return all_loops

def build_front_from_loops(loops):

    all_nodes = []
    front_edges = []
    
    current_idx = 0
    for loop in loops:
        n = len(loop)
        for i in range(n):
            all_nodes.append(loop[i])
            
            # Łączymy punkt tylko z następnym punktem W TEJ SAMEJ PĘTLI
            start_node = current_idx + i
            end_node = current_idx + ((i + 1) % n)
            front_edges.append((start_node, end_node))
            
        current_idx += n 
        
    return all_nodes, front_edges



def visualize_front(nodes, edges, title="Kontur wyciągnięty z SVG"):
    plt.figure(figsize=(8, 8))
    
    xs = [p[0] for p in nodes]
    ys = [p[1] for p in nodes]
    

    plt.scatter(xs, ys, color='green', s=5, zorder=3, label='Węzły startowe')
    
    for edge in edges:
        start_idx, end_idx = edge
        sp = nodes[start_idx]
        ep = nodes[end_idx]
        
        dx = ep[0] - sp[0]
        dy = ep[1] - sp[1]
        
        plt.quiver(sp[0], sp[1], dx, dy, 
                   angles='xy', scale_units='xy', scale=1, color='blue', 
                   width=0.005, headwidth=4, headlength=6, alpha= 0.5,zorder=2)

    plt.title(title)
    plt.grid( linestyle='--', alpha=0.5)
    plt.axis('equal') 
    plt.show()


if __name__ == "__main__":
    
    plik_svg = "pacman_duch.svg" 
    
    # Decydujemy, z ilu węzłów ma się składać pojedyncza pętla konturu
    ilosc_wezlow = 40 
    
    print(f"Czytanie wektorów z pliku: {plik_svg}...")
    
    petle = extract_loops_from_svg(plik_svg, ilosc_wezlow)
    
    węzły, odcinki = build_front_from_loops(petle)
    
    print(f"zbudowano front składający się z {len(węzły)} węzłów i {len(odcinki)} odcinków.")
    
    visualize_front(węzły, odcinki, title=f"Front startowy SVG: {plik_svg}")