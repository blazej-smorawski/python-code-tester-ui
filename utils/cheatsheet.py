def tip_variables():
    return """### Zmienne 🎁
Zmienne to pudełka na dane. Możesz w nich trzymać liczby, tekst i inne wartości.

```python
# Deklaracja zmiennej
zmienna = 10

# Wyświetlanie wartości zmiennej
print("Wartość zmiennej:", zmienna)

# Instrukcja przypisania
nowa_zmienna = zmienna + 5
print("Nowa zmienna:", nowa_zmienna)
```
Tutaj `nowa_zmienna` to `zmienna + 5`.
"""

def tip_maths():
    return """### Podstawowe operacje matematyczne 🔢
Python działa jak kalkulator: dodaje, odejmuje, mnoży i dzieli.
```python
# Operacje matematyczne
wynik = 5 + 3
print("Wynik dodawania:", wynik)
```
"""

def tip_lists():
    return """### Listy 🛒
Lista przechowuje wiele wartości w jednym miejscu.
```python
# Operacje na listach
lista = [1, 2, 3, 4, 5]
print("Pierwszy element listy:", lista[0])
```
"""

def tip_loops():
    return """### Pętle 🔁
Pętle służą do powtarzania tych samych kroków.
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

def tip_ascii_conversion():
    return """### Konwersja znaku na numer ASCII i z powrotem 🔤
Każdy znak ma swój numer. `ord()` zamienia znak na liczbę, a `chr()` liczbę na znak.

```python
ord('A') # 65
chr(65)  # A
```
"""

def tip_dictionaries():
    return """### Słowniki 📚
Słownik przechowuje pary: klucz i wartość.

```python
slownik = {'klucz1': 'wartosc1', 'klucz2': 'wartosc2'}
klucz = 'klucz1'
slownik[klucz] = 'wartosc3'
if klucz in slownik:
    b = slownik[klucz]
```
"""

def tip_custom_print():
    return """### Wypisywanie z własnym separatorem i końcem linii 🖨️
Domyślnie `print()` rozdziela wartości spacją i przechodzi do nowej linii.

Parametr `sep` zmienia separator, a `end` zmienia znak końca linii.

```python
x = 'tekst'
print(x)
print(x, x, sep='')
print(x, x, sep='|')
print(x, end='')
print(x, end=' ')
```
"""

def tip_type_conversions():
    return """### Konwersje typów 🔄
Możesz zmieniać typ danych, np. liczbę na tekst i odwrotnie.
```python
liczba = 3
tekst = str(liczba)
liczba_calkowita = int(tekst)
zmiennoprzecinkowa = float('0.25')
```
"""
