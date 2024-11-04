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