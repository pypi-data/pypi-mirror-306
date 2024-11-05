# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chronometrage']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chronometrage',
    'version': '0.1.3.1',
    'description': '',
    'long_description': "## Utilisation de l'application\n\nexemple 1: la fonction est executée une fois\\\n```python\nfrom chronometrage import chronometrage\n\n@chronometrage()\ndef ma_fonction_a_chronometrer():\n    # Code à chronométrer\n    pass\n\nma_fonction_a_chronometrer()\n```\nle temps d'execution est affiché dans la console\n\nexemple 2 : la fonction est executée 3 fois\n```python\nfrom chronometrage import chronometrage\n\n@chronometrage(3)\ndef ma_fonction_a_chronometrer():\n    # Code à chronométrer\n    pass\n\nma_fonction_a_chronometrer()\n```\nle temps d'execution moyen est affiché dans la console\n\nexemple 3 : plusieurs fonctions sont chronométrées les résultats sont mémorisés dans une liste.\n\n```python\nfrom chronometrage import *\n\n@chronometrage()\ndef ma_fonction_a_chronometrer_1():\n    # Code à chronométrer\n    pass\n\n@chronometrage()\ndef ma_fonction_a_chronometrer_2():\n    # Code à chronométrer\n    pass\n\n# Initialisation de la liste des temps et démarrage du mode mémorisation\ninit_time_list()\nma_fonction_a_chronometrer_1()\nma_fonction_a_chronometrer_2()\n# Affichage de la liste des temps\nprint(get_time_list())\n```\n\nautres décorateurs possibles:\nchrono_s : Décorateur qui affiche le temps d'exécution d'une fonction en seconde.\nchrono_us : Décorateur qui affiche le temps d'exécution d'une fonction en microseconde.",
    'author': 'Pierre Lemaitre',
    'author_email': 'oultetman@sfr.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
