#include <iostream>
#include <vector>
#include <cmath>
#include <cassert> 
#include <stdexcept>
using namespace std;

struct Point{
    double x,y;
};

class Polygon{
public:
    vector<Point>vertices;

    // Metoda pomocnicza do liczenia pola dowolnych 3 punktów
    float area(Point p1, Point p2, Point p3){
        
        float a = sqrt(pow(p2.x - p1.x, 2) + pow(p2.y - p1.y, 2));
        float b = sqrt(pow(p3.x - p2.x, 2) + pow(p3.y - p2.y, 2));
        float c = sqrt(pow(p1.x - p3.x, 2) + pow(p1.y - p3.y, 2));

        float s = (a + b + c) / 2.0f;
        float val= (s * (s - a) * (s - b) * (s - c));
        return (val > 0) ? sqrt(val) : 0.0f;
    }

    // Metoda sprawdzająca czy obiekt jest trójkątem i licząca jego pole
    float calculate_area(){
        if(vertices.size() != 3){
            throw invalid_argument("Ta figura nie jest trojkatem");
        }
    return area(vertices[0], vertices[1], vertices[2]);
    }

     bool contains(Point p) {
        if (vertices.size() != 3) return false;
        float area_abc = calculate_area(); // Tu sprawdzi czy to trójkąt
        float area_pab = area(p, vertices[0], vertices[1]);
        float area_pbc = area(p, vertices[1], vertices[2]);
        float area_pca = area(p, vertices[2], vertices[0]);

        return abs((area_pab + area_pbc + area_pca) - area_abc) < 0.01f;
    }

};

void test() {
    Polygon t;
    t.vertices = {{0,0}, {10,0}, {5,10}}; // Trójkąt równoramienny

    // Test 1: Punkt w środku
    assert(t.contains({5, 5}) == true);
    // Test 2: Punkt na zewnątrz
    assert(t.contains({20, 20}) == false);
    // Test 3: Punkt na krawędzi (wymaga uwagi na błędy zaokrągleń!)
    assert(t.contains({5, 0}) == true); 
    std::cout << "Wszystkie testy przynależności zaliczone!" << std::endl;
}

int main(){

    try{
        test();
    }catch (exception& e){
        cout << "Wystapil blad podczas testow: " << e.what() << endl;
        return 1;
    }
    
    return 0;
}