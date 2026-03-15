#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <SFML/Graphics.hpp>
using namespace std;

struct Point{
    double x,y;
};

// test

vector<Point> generate_polygon(double x0, double y0, double r, int n){
    vector<Point> vertices; 
    if(n<3) return vertices;

    vertices.reserve(n);  //Rezerwuje miejsce, ale rozmiar wektora to nadal 0. Elementy dodajemy przez push_back
    const double pi = acos(-1.0);
    for(int i=0; i<n; i++){
        double angle = 2.0*pi*i/n;

        Point p;
        p.x=x0+r*cos(angle);
        p.y=y0+r*sin(angle);

        vertices.push_back(p);
    }

return vertices;
}

void draw_polygon_scene(double x0, double y0, double r, int n){
    sf::RenderWindow window(sf::VideoMode({800, 600}), "Aproksymacja Okregu");
    window.setFramerateLimit(60);

    // Początkowy poziom przybliżenia
    float zoomLevel = 1.0f;
    sf::View view;
    view.setCenter({0.f, 0.f}); 

    // aktualizacja rozmiaru widoku
    auto updateView = [&]() {
        view.setSize({800.f * zoomLevel, -600.f * zoomLevel});    // Ujemne Y, aby zachować układ kartezjański
        window.setView(view);
    };
    updateView();

    // Rysowanie osi układu 
    sf::Vertex axes[] = {
        {{-10000.f, 0.f}, sf::Color::Black}, {{10000.f, 0.f}, sf::Color::Black},
        {{0.f, -10000.f}, sf::Color::Black}, {{0.f, 10000.f}, sf::Color::Black}
    };

    vector<Point> vertices = generate_polygon(x0, y0, r, n);
    
    //tworzenie kształtu
    sf::ConvexShape polygon;
    polygon.setPointCount(vertices.size());
    for (size_t i = 0; i < vertices.size(); i++) {
        polygon.setPoint(i, sf::Vector2f(vertices[i].x, vertices[i].y));
    }

    //wyglad wielokata
    polygon.setFillColor(sf::Color::Blue); 
    polygon.setOutlineColor(sf::Color::Blue);
    polygon.setOutlineThickness(1);

    //tworzenie okregu
    sf::CircleShape circle(static_cast<float>(r));
    circle.setOrigin({(float)r, (float)r});   //ustawia środek odniesienia
    circle.setPosition({(float)x0, (float)y0}); // ustawia środek odnoesienia dokładnie w (x0,y0)
    circle.setFillColor(sf::Color::Transparent);
    circle.setOutlineColor(sf::Color::Magenta); 
    circle.setOutlineThickness(1);

    while (window.isOpen()) {
        while (const std::optional event = window.pollEvent()) {
            if (event->is<sf::Event::Closed>()) window.close();
        
            // Obsługa Zoomu za pomocą rolki myszy
            if (const auto* mouseWheel = event->getIf<sf::Event::MouseWheelScrolled>()) {
                if (mouseWheel->wheel == sf::Mouse::Wheel::Vertical) {
                    if (mouseWheel->delta > 0) {
                        zoomLevel *= 0.9f; // Przybliżanie
                    } else {
                        zoomLevel *= 1.1f; // Oddalanie
                    }
                    updateView();
                }
            }
        }
        

        window.clear(sf::Color::White);
        window.draw(axes, 4, sf::PrimitiveType::Lines);
        window.draw(circle);  
        window.draw(polygon);  
        
        window.display();
    }
}

int main(){
    double x0;
    double y0;
    double r;
    int n;
    cout<<"Podaj wspolrzedna x srodka okregu: "; 
    cin>>x0;
    cout<<"Podaj wspolrzedna y srodka okregu: ";
    cin>>y0;
    cout<<"Podaj promien okregu: ";
    cin>>r;
    cout<<"Podaj liczbe wierzcholkow wielokata: ";
    cin>>n;

    vector<Point> polygon = generate_polygon(x0, y0, r, n);
   cout<<"Wierzcholki wielokata (n= "<<n<<"): "<<endl;
    for(auto& p : polygon){
        cout<<fixed<<setprecision(2)<<"( "<<p.x<<", "<<p.y<<")"<<endl;
    }

    draw_polygon_scene(x0, y0, r, n);


return 0;
}