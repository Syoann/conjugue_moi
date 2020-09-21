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
| Présent |
| --- |
| je mange |
| tu manges |
| il mange |
| elle mange |
| on mange |
| nous mangeons |
| vous mangez |
| ils mangent |
| elles mangent |
```

| Présent |
| --- |
| je mange |
| tu manges |
| il mange |
| elle mange |
| on mange |
| nous mangeons |
| vous mangez |
| ils mangent |
| elles mangent |
