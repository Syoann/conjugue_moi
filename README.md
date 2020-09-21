# conjugue_moi

Conjugaison des verbes français en ligne de commande.
Utilisé pour le moment pour générer un dictionnaire de verbes conjugués.
Possibilité d'avoir la forme interrogative.


## Installation

```
git clone https://github.com/Syoann/conjugue_moi.git
```

## Utilisation

- Générer un dictionnaire de verbes conjugués :

```
python3 conjugue_moi.py verbes.list > verbes.dic
```

```
head -6 verbes.dic
```

```
je mange
tu manges
il mange
nous mangeons
vous mangez
ils mangent
```


- Générer un tableau de conjugaison pour un seul verbe:

```
python3 conjugue_moi.py manger
```
```
| Présent | Imparfait | Futur | Passé simple | Conditionnel |
| --- | --- | --- | --- | --- |
| je mange | je mangeais | je mangerai | je mangeai | je mangerais |
| tu manges | tu mangeais | tu mangeras | tu mangeais | tu mangerais |
| il mange | il mangeait | il mangera | il mangea | il mangerait |
| nous mangeons | nous mangions | nous mangerons | nous mangeâmes | nous mangerions |
| vous mangez | vous mangiez | vous mangerez | vous mangeâtes | vous mangeriez |
| ils mangent | ils mangeaient | ils mangeront | ils mangèrent | ils mangeraient |
```
| Présent | Imparfait | Futur | Passé simple | Conditionnel |
| --- | --- | --- | --- | --- |
| je mange | je mangeais | je mangerai | je mangeai | je mangerais |
| tu manges | tu mangeais | tu mangeras | tu mangeais | tu mangerais |
| il mange | il mangeait | il mangera | il mangea | il mangerait |
| nous mangeons | nous mangions | nous mangerons | nous mangeâmes | nous mangerions |
| vous mangez | vous mangiez | vous mangerez | vous mangeâtes | vous mangeriez |
| ils mangent | ils mangeaient | ils mangeront | ils mangèrent | ils mangeraient |


## A faire

- terminer la conjugaison des verbes du 3ème groupe
- gérer les verbes pronominaux
- ajouter l'impératif
