def tip_variables():
    return """### Zmienne 
Zmienne w Pythonie są jak magiczne pudełka 🎁, ale bardziej elastyczne! Możemy do nich wrzucać różne rzeczy, na przykład liczby czy słowa.

```python
# Deklaracja zmiennej
zmienna = 10

# Wyświetlanie wartości zmiennej
print("Wartość zmiennej:", zmienna)

# Instrukcja przypisania
nowa_zmienna = zmienna + 5
print("Nowa zmienna:", nowa_zmienna)
```
Zmienna `nowa_zmienna` przyjmuje wartość zmiennej `zmienna` powiększoną o 5. Zmienne mogą być elastyczne i zmieniać swoje wartości!
"""

def tip_maths():
    return """### Podstawowe Operacje Matematyczne
Python może nam służyć jako kalkulator 🔢. Potrafi dodawać, odejmować, mnożyć i dzielić!
```python
# Operacje matematyczne
wynik = 5 + 3
print("Wynik dodawania:", wynik)
```
"""

def tip_lists():
    return """### Listy
Listy to zbiory rzeczy, takie jak lista zakupów 🛒. Możemy trzymać różne przedmioty w jednej liście.
```python
# Operacje na listach
lista = [1, 2, 3, 4, 5]
print("Pierwszy element listy:", lista[0])
```
"""

def tip_loops():
    return """### Pętle 
Pętle pomagają nam robić to samo wiele razy.
```python
# Pętla for
for i in range(5):
    print("Liczba:", i)

a = 5
while a > 0:
    print("Liczba:", a)
    a = a - 1
```
"""

def tip_ifs():
    return """### Warunki
Warunki pozwalają nam podejmować decyzje jak w grze planszowej 🎲. Na przykład, czy liczba jest większa niż 5?
```python
# Warunek if
liczba = 8
if liczba > 5:
    print("Liczba jest większa niż 5")
```
"""

def tip_functions():
    return """### Funkcje
Funkcje to jak magiczne zaklęcia, które możemy używać wielokrotnie 🧙.
```python
# Funkcja dodawania
def dodaj(a, b):
    wynik = a + b
    return wynik

# Wywołanie funkcji
suma = dodaj(3, 4)
print("Wynik dodawania:", suma)
```
"""
