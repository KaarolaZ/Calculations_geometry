#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <sstream>
#include <chrono>
#include <algorithm>
#include <map>
using namespace std;

struct Point{
    double x,y;
};

// Struktura Bounding Box (Pudełko otaczające)
struct Bounding_Box{
    double minX, maxX, minY, maxY;
};

class Polygon{
public:
    int id;
    vector<Point>vertices;
    Bounding_Box b;
};

bool contains_basic(const Point& p, const vector<Point>& polygon){
    int n = polygon.size();
    int cut_count = 0;

    for(int i =0; i<n ; i++){
        int j;
        if(i==0){
            j = n-1; // Jeśli jesteśmy na pierwszym wierzchołku, poprzednim jest wierzchołek ostatni
        }else{
            j = i - 1; // W każdym innym przypadku poprzednim wierzchołkiem jest po prostu ten o jeden indeks mniejszy
        }

        Point p1 = polygon[i];
        Point p2 = polygon[j];

        //Sprawdzamy czy y jest na wysokości danej krawędzi
        bool is_y_between = (p1.y > p.y) != (p2.y > p.y);

        if(is_y_between){
            //wspolrzedna x miejsca, gdzie promien przecina krawedz
            double x_cut = (p2.x - p1.x) * (p.y - p1.y) / (p2.y - p1.y) + p1.x;
        // Jeśli nasz punkt (p.x) znajduje się na lewo od miejsca przecięcia, to znaczy, że promień (rzucany w prawo) fizycznie przeciął tę krawędź.
           if(p.x<x_cut) cut_count++;
        }
    }
    // - nieparzysta liczba przecięć = punkt jest WNĘTRZU (zwróci true)
    // - parzysta liczba przecięć (lub 0) = punkt jest NA ZEWNĄTRZ (zwróci false)
    return (cut_count % 2 !=0);
}

//Obliczanie Bounding Box dla wielokąta
Bounding_Box calculate_bounding_box(const vector<Point> polygon){
    Bounding_Box bb = {polygon[0].x, polygon[0].x, polygon[0].y, polygon[0].y};
    for (const auto& p : polygon) {
        bb.minX = min(bb.minX, p.x);
        bb.maxX = max(bb.maxX, p.x);
        bb.minY = min(bb.minY, p.y);
        bb.maxY = max(bb.maxY, p.y);
    }
    return bb;
}

bool contains_optimized(const Point& p, const vector<Point>& polygon, Bounding_Box& bb){
    //jeśli punkt jest poza "pudełkiem", na 100% nie jest w wielokącie
    if (p.x < bb.minX || p.x > bb.maxX || p.y < bb.minY || p.y > bb.maxY) {
        return false;
    }
    return contains_basic(p, polygon);
}


int main(){
    
 
    vector<Point> test_points;
    ifstream plik_z_pkt("punkty.txt");

    if(!plik_z_pkt.is_open()){
        cout << "Blad: Nie udalo sie otworzyc pliku punkty.txt!" << endl;
        return 1;
    }

    string linia;
    while (getline(plik_z_pkt, linia)) {
        if (linia.empty() || linia[0] == '*') continue; 

        stringstream ss(linia);
        int id; double x, y;
        if (ss >> id >> x >> y) {
            test_points.push_back({x, y}); 
        }
    }
    plik_z_pkt.close();

    // Wczytywanie wielokątów z pliku wielokaty.txt
    vector<Polygon> lista_wielokatow;
    map<int, Point> wierzcholki; // Mapa do przechowywania węzłów: ID -> Punkt
    ifstream plik_wielokaty("wielokaty.txt");

    if (!plik_wielokaty.is_open()) {
        cout << "Blad: Nie udalo sie otworzyc pliku wielokaty.txt!" << endl;
    } else {
        bool czytamy_wezly = false;
        bool czytamy_elementy = false;

        while (getline(plik_wielokaty, linia)) {
            if (linia.empty()) continue;
            
            // Wykrywanie sekcji w pliku
            if (linia.find("*NODES") != string::npos) {
                czytamy_wezly = true; czytamy_elementy = false; continue;
            } else if (linia.find("*ELEMENTS") != string::npos) {
                czytamy_wezly = false; czytamy_elementy = true; continue;
            } else if (linia[0] == '*' || linia[0] == 'I') {
                continue; // Pomijamy inne nagłówki
            }

            stringstream ss(linia);
            if (czytamy_wezly) {
                int idWezla; double x, y;
                if (ss >> idWezla >> x >> y) {
                    wierzcholki[idWezla] = {x, y};
                }
            } else if (czytamy_elementy) {
                Polygon nowy_poly;
                if (ss >> nowy_poly.id) {
                    int id_wezla;
                    while (ss >> id_wezla) {
                        nowy_poly.vertices.push_back(wierzcholki[id_wezla]);
                    }
                    lista_wielokatow.push_back(nowy_poly);
                }
            }
        }
        plik_wielokaty.close();
    }

    // ETAP 3: Wybór wielokąta przez użytkownika
    cout << "Dostepne ID wielokatow: ";
    for (const auto& w : lista_wielokatow) cout << w.id << ", ";
    cout << "\nPodaj ID wielokata, ktory chcesz sprawdzic: ";
    
    int wybrane_id;
    cin >> wybrane_id;

    Polygon wybrany_wielokat;
    bool znaleziono = false;
    for (const auto& w : lista_wielokatow) {
        if (w.id == wybrane_id) {
            wybrany_wielokat = w;
            znaleziono = true;
            break;
        }
    }

    if (!znaleziono) {
        cout << "Nie znaleziono wielokata o podanym ID. Koniec programu." << endl;
        return 1;
    }

    cout << "\nRozpoczynam testy dla " << test_points.size() << " punktow..." << endl;

    // ETAP 4: Metoda podstawowa i pomiar czasu

    int punkty_w_srodku_basic = 0;
    auto start_basic = chrono::high_resolution_clock::now();
    
    for (const auto& p : test_points) {
        if (contains_basic(p, wybrany_wielokat.vertices)) {
            punkty_w_srodku_basic++;
        }
    }
    
    auto end_basic = chrono::high_resolution_clock::now();
    chrono::duration<double, milli> czas_basic = end_basic - start_basic;

    cout << "\n--- METODA PODSTAWOWA ---" << endl;
    cout << "Punktow wewnatrz: " << punkty_w_srodku_basic << endl;
    cout << "Czas wykonania:   " << czas_basic.count() << " ms" << endl;

   
    // ETAP 5: Metoda zoptymalizowana i pomiar czasu
    int punkty_w_srodku_opt = 0;
    
    // Obliczamy Bounding Box TYLKO RAZ przed wejściem w pętlę
    wybrany_wielokat.b = calculate_bounding_box(wybrany_wielokat.vertices);
    
    auto start_opt = chrono::high_resolution_clock::now();
    
    for (const auto& p : test_points) {
        if (contains_optimized(p, wybrany_wielokat.vertices, wybrany_wielokat.b)) {
            punkty_w_srodku_opt++;
        }
    }
    
    auto end_opt = chrono::high_resolution_clock::now();
    chrono::duration<double, milli> czas_opt = end_opt - start_opt;

    cout << "\n--- METODA ZOPTYMALIZOWANA (Bounding Box) ---" << endl;
    cout << "Punktow wewnatrz: " << punkty_w_srodku_opt << endl;
    cout << "Czas wykonania:   " << czas_opt.count() << " ms" << endl;


    // ETAP 6: Porównanie wyników
    cout << "\n--- PODSUMOWANIE ---" << endl;
    if (czas_opt.count() > 0.001) { // Zabezpieczenie przed dzieleniem przez bliskie zeru
        double przyspieszenie = czas_basic.count() / czas_opt.count();
        cout << "Optymalizacja przyspieszyla dzialanie algorytmu ok. " << przyspieszenie << " razy" << endl;
    } else {
        cout << "too fast to count the multiplier" << endl;
    }

    return 0;
}