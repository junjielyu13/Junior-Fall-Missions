
euro = 434
# euro = int(input("Euro: "))
lista_De_Billetes = [500, 200, 100, 50, 20, 10, 5, 2, 1]  ##  1) order de la lista


for billete in lista_De_Billetes:       ## 2) bucle de la lista

    cantidad = euro // billete          ## 2) cantitdad del euro
    if cantidad > 0:  
        euro -= cantidad * billete

        if billete < 5:
            print(f"{cantidad} monedas de {billete} euros.")
        else:
            print(f"{cantidad} billetes de {billete} euros.")