#include <iostream>
#include <algorithm>
#include <cmath>
#include <optional>
#include <SFML/Graphics.hpp>
using namespace std;

struct Point{
    double x, y;
};
struct Vector{
    double dx, dy;
};
struct Line{
    double A, B, C; 
};

//1) Wyznaczenie równania prostej, do której należy dany odcinek
Line line_from_points(Point p1, Point p2){
    double A = p1.y - p2.y;
    double B = p2.x - p1.x;
    double C = -A * p1.x - B * p1.y;
    return {A, B, C};
}

//2)Sprawdzenie przynależności punktu do prostej
bool point_on_line(Line l, Point p){
    return abs(l.A*p.x + l.B*p.y +l.C)<1e-9;  // niweluje drobne błędy w zaokrąglaniu współrzędnych.
}
//3)Sprawdzenie przynależności punktu do odcinka
bool point_on_segment(Point p, Point p1, Point p2){
    if (!point_on_line(line_from_points(p1, p2), p)) return false;

    return ((p.x>= min(p1.x, p2.x)- 1e-9) && (p.x <= max(p1.x, p2.x)+1e-9)) && ((p.y>= min(p1.y, p2.y)- 1e-9) && (p.y <= max(p1.y, p2.y)+1e-9));
}

//4)  Określenie położenia punktu względem prostej
void point_position(Line l, Point p){
    double value = l.A*p.x + l.B*p.y +l.C;
    if(abs(value)< 1e-9){  //==0
        cout<<"Punkt na linii"<<endl; 
    }else if(value<0){
        cout<<"Strona lewa"<<endl;
    }else cout<<"Strona prawa"<<endl;
}

//5) Dokonanie translacji odcinka o podany wektor
void vector_transalte(Point &p1, Point &p2, double dx, double dy){
    p1.x += dx;
    p1.y +=dy;
    p2.x +=dx;
    p2.y +=dy;
}

//6)Dokonanie odbicia danego punktu względem linii
Point reflect_points(Line l, Point p){
    double d = l.A*l.A + l.B*l.B;  //kwadrat dł wektora normalnego
    double k= -2*(l.A*p.x +l.B*p.y +l.C)/d; // odl do miejsca docelowego
    return {p.x+k*l.A, p.y+k*l.B};
}

void run_tests() {
   
    Point p1{0, 0}, p2{4, 4};
    Line l = line_from_points(p1, p2);
    
    std::cout << "TESTY\n";
    std::cout << "1. Rownanie: " << l.A << "x + " << l.B << "y + " << l.C << " = 0\n";
    
    Point testP{0, 4}; 
    std::cout << "2. Czy (2,2) na prostej? " << (point_on_line(l, {2,2}) ? "TAK" : "NIE") << "\n";
    
    std::cout << "3. Pozycja punktu (0,4): "; 
    point_position(l, testP);
    
    Point reflected = reflect_points(l, testP);
    std::cout << "4. Odbicie punktu (0,4): (" << reflected.x << ", " << reflected.y << ")\n";
}

void draw_scene(Point p1, Point p2, Point testP) {
    sf::RenderWindow window(sf::VideoMode({800, 600}), "Wizualizacja Geometrii");
    window.setFramerateLimit(60);

    while (window.isOpen()) {
       while (const std::optional event = window.pollEvent()) {
    if (event->is<sf::Event::Closed>()) {
        window.close();
    }
    else if (const auto* mouseMoved = event->getIf<sf::Event::MouseMoved>()) {
        testP.x = mouseMoved->position.x;
        testP.y = mouseMoved->position.y;
    }
}

        Line l = line_from_points(p1, p2);
        Point reflected = reflect_points(l, testP);

        window.clear(sf::Color::White);

        // --- Rysowanie nieskończonej prostej (szara) ---
        sf::Vertex line_inf[2];
        line_inf[0] = { {0.f, static_cast<float>((-l.C - l.A * 0) / l.B)}, sf::Color(200, 200, 200) };
        line_inf[1] = { {800.f, static_cast<float>((-l.C - l.A * 800) / l.B)}, sf::Color(200, 200, 200) };

        window.draw(line_inf, 2, sf::PrimitiveType::Lines);

        // --- Rysowanie odcinka (czarny) ---
       sf::Vertex segment[2];
        segment[0] = { {static_cast<float>(p1.x), static_cast<float>(p1.y)}, sf::Color::Black };
        segment[1] = { {static_cast<float>(p2.x), static_cast<float>(p2.y)}, sf::Color::Black };
        window.draw(segment, 2, sf::PrimitiveType::Lines);

        // --- Punkt testowy (Czerwony, niebieski na odcinku) ---
        sf::CircleShape cTest(6);
        cTest.setOrigin({6.f, 6.f});
        cTest.setPosition({static_cast<float>(testP.x), static_cast<float>(testP.y)});
        cTest.setFillColor(point_on_segment(testP, p1, p2) ? sf::Color::Blue : sf::Color::Red);
        window.draw(cTest);

        // --- Punkt odbity (Zielony) ---
        sf::CircleShape cRefl(6.f);
        cRefl.setOrigin({6.f, 6.f});
        cRefl.setPosition({static_cast<float>(reflected.x), static_cast<float>(reflected.y)});
        cRefl.setFillColor(sf::Color::Green);
        window.draw(cRefl);

        // Linia łącząca punkt z odbiciem (pokazuje prostopadłość)
        sf::Vertex connection[2];
           connection[0] = { {static_cast<float>(testP.x), static_cast<float>(testP.y)}, sf::Color(150, 150, 150, 100) };
        connection[1] = { {static_cast<float>(reflected.x), static_cast<float>(reflected.y)}, sf::Color(150, 150, 150, 100) };
        window.draw(connection, 2, sf::PrimitiveType::Lines);

        window.display();
    }
}

int main(){
    //run_tests();
Point p1{200, 200}, p2{600, 450};
    Point testP{100, 400};

    draw_scene(p1, p2, testP);
    return 0;
}