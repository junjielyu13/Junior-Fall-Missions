from math import sqrt

a = float(input("Valor de a: "))
b = float(input("Valor de b: "))
c = float(input("Valor de c: "))


if a!=0:
    if (b**2)-(4*a*c) < 0:
        print("Error de dominio matemático de sqrt")
    else:   
        x1 = (-b+sqrt( (b**2)-(4*a*c) ))/(2*a)
        x2 = (-b-sqrt( (b**2)-(4*a*c) ))/(2*a)

        print("solucion:", x1 , ",", x2)
        print(f"solucion: {x1} , {x2}")
    
else:
    print("No es una ecuacion de segundo grado")

