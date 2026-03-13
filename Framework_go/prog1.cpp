#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <fstream>
#include <sstream>
#include <SFML/Graphics.hpp>
using namespace std;

class Point{
public:
    int ID;
    double x, y;

    Point(int ID, double x, double y) : ID(ID), x(x), y(y) {}
};

class Element{
public:
    int ID;

    vector<Point*> points; 
    Element(int ID) : ID(ID) {}

    void add_point(Point* point){
        points.push_back(point);
    }

    string get_type() {
        if(points.size() == 2) return "Linia";
        if(points.size() > 2) return "Wielokat";
        return "Nieznany";
    }

    void draw(sf::RenderWindow& window, float scale) {
        float h = static_cast<float>(window.getSize().y); // Pobieranie wysokości okna
        if (points.size() == 2) {
            // Rysowanie linii
            //scale do przeliczania wspolrzednych mat na piksele
            sf::Vertex line[] = {
                sf::Vertex{sf::Vector2f(static_cast<float>(points[0]->x * scale), 600.f - static_cast<float>(points[0]->y * scale)), sf::Color::Black},
                sf::Vertex{sf::Vector2f(static_cast<float>(points[1]->x * scale), 600.f - static_cast<float>(points[1]->y * scale)), sf::Color::Black}
            };
            
            window.draw(line, 2, sf::PrimitiveType::Lines);
        } 
        else if (points.size() > 2) {
            // Rysowanie wielokąta 
            sf::ConvexShape convex;
            convex.setPointCount(points.size());
            convex.setFillColor(sf::Color(100, 150, 250, 150)); 
            convex.setOutlineColor(sf::Color::White);
            convex.setOutlineThickness(1.f);

            for (size_t i = 0; i < points.size(); ++i) {
                // Konwersja na float i odwrócenie osi Y
                convex.setPoint(i, sf::Vector2f(static_cast<float>(points[i]->x * scale), 600.f - static_cast<float>(points[i]->y * scale)));
            }
            window.draw(convex);
        }
    }
    
};

class Geometry_manage {
public: 
    map<int, Point*> all_points;  // szukanie po ID
    vector<Element*> all_elements;

    void load_from_file(const string& filename) {
        ifstream file(filename);
        if (!file.is_open()) {
        cout << "BLAD: Nie moge otworzyc pliku: " << filename << endl;
        // Sprawdzmy, gdzie program teraz jest:
        system("cd"); 
        return;
        }

        string line;
        string mode = "";
        
        while(getline(file, line)){
            if(line.empty() || line[0] == 'I') continue; // pomijamy puste linie
            
            if (line.find("*NODES") != string::npos) {   //Jeśli szukany tekst nie zostanie odnaleziony, funkcja nie może zwrócić poprawnego indeksu, więc zwraca właśnie npos
                mode = "NODES";
                continue;
            }
            
            if (line.find("*ELEMENTS") != string::npos) { 
                mode = "ELEMENTS";
                continue;
            }

       stringstream ss(line);
            if (mode == "NODES") {
                int ID;
                double x, y;
                if (ss >> ID >> x >> y) {
                    all_points[ID] = new Point(ID, x, y);
                }
            } 
            else if (mode == "ELEMENTS") {
                int elID, node_id;
                if (!(ss >> elID)) continue;

                Element* el = new Element(elID);
            while (ss>>node_id){
                if(all_points.count(node_id)) 
                el->add_point(all_points[node_id]);
            }
            all_elements.push_back(el);
        }
        }
        file.close();
    }

    ~Geometry_manage() {
   for (auto& pair : all_points) delete pair.second;
        for (Element* el : all_elements) delete el;
    }
};

//siatka
void grid(sf::RenderWindow& window, float scale) {
    float w = static_cast<float>(window.getSize().x);
    float h = static_cast<float>(window.getSize().y);
    sf::Color gridCol(230, 230, 230); //linie siatki
    sf::Color mainCol(150, 150, 150); //linie osi X, Y

    for (float x = 0; x <= w; x += scale) {
        sf::Vertex l[] = { sf::Vertex{{x, 0}, (x==0 ? mainCol : gridCol)}, sf::Vertex{{x, h}, (x==0 ? mainCol : gridCol)} };
        window.draw(l, 2, sf::PrimitiveType::Lines);
    }
    for (float y = 0; y <= h; y += scale) {
        sf::Vertex l[] = { sf::Vertex{{0, h-y}, (y==0 ? mainCol : gridCol)}, sf::Vertex{{w, h-y}, (y==0 ? mainCol : gridCol)} };
        window.draw(l, 2, sf::PrimitiveType::Lines);
    }
}


int main() {
    Geometry_manage geo;
    geo.load_from_file("Wspolrzedne.txt"); // Wczytywanie danych z pliku [cite: 12]

    // test 
    cout << "Zaladowano " << geo.all_points.size() << " punktow." << endl;
    cout << "Zaladowano " << geo.all_elements.size() << " elementow." << endl;
    for(auto* el : geo.all_elements) {
        cout << "Element ID: " << el->ID << ", Typ: " << el->get_type() << ", Liczba wezlow: " << el->points.size() << endl;
    }

   const float w = 800.f, h = 600.f, scale = 60.f;  
    sf::RenderWindow window(sf::VideoMode({(unsigned int)w, (unsigned int)h}), "Geometria Obliczeniowa"); // wczytywanie okna graficznego

    while (window.isOpen()) {
       
        while (const std::optional event = window.pollEvent()) { //pollEvent sprawdza czy użytkownik nie chce zamknąc okna
            if (event->is<sf::Event::Closed>()) window.close();
        }
        //Renderownie
        window.clear(sf::Color::White); 
        grid(window, scale);

        for (Element* el : geo.all_elements) el->draw(window, scale);

        for (auto const& [id, p] : geo.all_points) {
            sf::CircleShape dot(4.f);
            dot.setFillColor(sf::Color::Blue);
            dot.setOrigin({4.f, 4.f}); // Centrowanie kropki
            dot.setPosition({static_cast<float>(p->x * scale), h - static_cast<float>(p->y * scale)});
            window.draw(dot);
        }

        window.display();
    }
    return 0;

   
}


// Do poprawnego uruchomienia potrzebne są pliki: 
// sfml-audio-3.dll 
// sfml-graphics-3.dll 
// sfml-network-3.dll 
// sfml-network-d-3.dll 
// sfml-system-3.dll 
// sfml-system-d-3.dll 
// sfml-window-3.dll