## Utilisation de l'application

exemple 1: la fonction est executée une fois\
```python
from chronometrage import chronometrage

@chronometrage()
def ma_fonction_a_chronometrer():
    # Code à chronométrer
    pass

ma_fonction_a_chronometrer()
```
le temps d'execution est affiché dans la console

exemple 2 : la fonction est executée 3 fois
```python
from chronometrage import chronometrage

@chronometrage(3)
def ma_fonction_a_chronometrer():
    # Code à chronométrer
    pass

ma_fonction_a_chronometrer()
```
le temps d'execution moyen est affiché dans la console

exemple 3 : plusieurs fonctions sont chronométrées les résultats sont mémorisés dans une liste.

```python
from chronometrage import *

@chronometrage()
def ma_fonction_a_chronometrer_1():
    # Code à chronométrer
    pass

@chronometrage()
def ma_fonction_a_chronometrer_2():
    # Code à chronométrer
    pass

# Initialisation de la liste des temps et démarrage du mode mémorisation
init_time_list()
ma_fonction_a_chronometrer_1()
ma_fonction_a_chronometrer_2()
# Affichage de la liste des temps
print(get_time_list())
```

autres décorateurs possibles:
chrono_s : Décorateur qui affiche le temps d'exécution d'une fonction en seconde.
chrono_us : Décorateur qui affiche le temps d'exécution d'une fonction en microseconde.