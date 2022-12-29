
# what_Is_Range = list(range(0,100)) 
# print(what_Is_Range)

# for i in range(0,10



euro = 434

if euro >= 500:
    cantidad = int(euro / 500)  
    if cantidad > 0:
        euro -= cantidad * 500
        print(f"{cantidad} billetes de 500 euros.")
    
if euro >= 200:
    cantidad = int(euro / 200)
    if cantidad > 0:  
        euro -= cantidad * 200
        print(f"{cantidad} billetes de 200 euros.")

if euro >= 100:
    cantidad = int(euro / 100)
    if cantidad > 0:  
        euro -= cantidad * 100
        print(f"{cantidad} billetes de 100 euros.")


if euro >= 50:
    cantidad = int(euro / 50)
    if cantidad > 0:  
        euro -= cantidad * 50
        print(f"{cantidad} billetes de 50 euros.")


if euro >= 20:
    cantidad = int(euro / 20)
    if cantidad > 0:  
        euro -= cantidad * 20
        print(f"{cantidad} billetes de 20 euros.")


if euro >= 10:
    cantidad = int(euro / 10)
    if cantidad > 0:  
        euro -= cantidad * 10
        print(f"{cantidad} billetes de 10 euros.")


if euro >= 5:
    cantidad = int(euro / 5)
    if cantidad > 0:  
        euro -= cantidad * 5
        print(f"{cantidad} billetes de 5 euros.")


if euro >= 2:
    cantidad = int(euro / 2)
    if cantidad > 0:  
        euro -= cantidad * 2
        print(f"{cantidad} monedas de 2 euros.")

if euro >= 1:
    cantidad = int(euro / 1)
    if cantidad > 0:  
        euro -= cantidad * 1
        print(f"{cantidad} monedas de 1 euros.")