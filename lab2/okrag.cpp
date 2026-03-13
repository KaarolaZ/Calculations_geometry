#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
using namespace std;

struct Point{
    double x,y;
};

// test

vector<Point> generate_polygon(double x0, double y0, double r, int n){
    vector<Point> vertices; //wierzchołki
    if(n<3) return vertices;

    vertices.reserve(n);  //Rezerwuje miejsce, ale rozmiar wektora to nadal 0. Elementy dodajemy przez push_back
    // Zamiast double pi = std::numbers::pi;
    const double pi = std::acos(-1.0);
    for(int i=0; i<n; i++){
        double angle=2.0*pi*i/n;

        Point p;
        p.x=x0+r*cos(angle);
        p.y=y0+r*sin(angle);

        vertices.push_back(p);
    }

return vertices;
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
        cout<<fixed<<setprecision(4)<<"( "<<p.x<<", "<<p.y<<")"<<endl;
    }


return 0;
}