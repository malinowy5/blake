# Blake
Implementacja algorytmu Blake w języku Python oraz testy zgodności z implementacją referencyjną w języku C.

## Używanie

```Python
from main import Blake # Zakładając, że plik z implementacją to main.py

blake = Blake(256) # Tworzenie obiektu Blake-256

# Proste haszowanie, czyta wszystkie dane na raz
result = blake.Hash("I do pieca")
print(f"BLAKE-256: {result}")

blake = Blake(256) # Nowy obiekt
# Haszowanie czytając dane w kawałkach
blake.Update(b"I ")
blake.Update(b"do ")
blake.Update(b"pieca")
result = blake.Final()
print(f"BLAKE-256: {result}")


```

## Testowanie

Aby przetestować implementację należy wygenerować zarówno dla niej, jak i dla referencyjnego kodu w C pliki zawierające hasze, a następnie je porównać.

### Kompilacja testów C
`gcc test_generator.c blake256.c -o test_generator`

### Uruchamianie testów

C: 
`./test_generator`
Python: 
`python3 test_generator.py`

### Porównywanie wyników:
`diff kat_py.txt kat_c.txt`
`diff mct_py.txt mct_c.txt`

Jeśli diff nic nie zwrócił, wyniki Pythona i C są identyczne. 