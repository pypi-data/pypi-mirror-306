import time

time_list = []
to_liste = False


def init_time_list():
    global time_list, to_liste
    time_list = []
    to_liste = True

def get_time_list():
    return time_list


def chrono_s(fonction):
    """Décorateur qui affiche le temps d'exécution d'une fonction en seconde."""

    def fonction_decoree(*args, **kwargs):
        debut = time.time()
        resultat = fonction(*args, **kwargs)
        fin = time.time()
        print(f"Temps d'exécution de {fonction.__name__}: {fin - debut:.9f} secondes")
        return resultat

    return fonction_decoree


def chrono_us(fonction):
    """Décorateur qui affiche le temps d'exécution d'une fonction en seconde."""

    def fonction_decoree(*args, **kwargs):
        debut = time.time()
        resultat = fonction(*args, **kwargs)
        fin = time.time()
        print(f"Temps d'exécution de {fonction.__name__}: {(fin - debut) * 1000000:.6f} microsecondes")
        return resultat

    return fonction_decoree


def chronometrage(n=1):
    def decorateur(fonction):
        def fonction_decoree(*args, **kwargs):
            total_time = 0
            for _ in range(n):
                debut = time.time()
                resultat = fonction(*args, **kwargs)
                fin = time.time()
                total_time += (fin - debut)
            moyenne = total_time / n
            if to_liste:
                time_list.append([fonction.__name__, moyenne])
            else:
                if n == 1:
                    print(f"Temps d'exécution de {fonction.__name__}: {moyenne:.6f} secondes")
                else:
                    print(f"Temps d'exécution moyen de {fonction.__name__} sur {n} essais : {moyenne:.6f} secondes")
            return resultat

        return fonction_decoree

    return decorateur