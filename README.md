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
head -9 verbes.dic
```

```
je mange
tu manges
il mange
elle mange
on mange
nous mangeons
vous mangez
ils mangent
elles mangent
```


- Générer un tableau de conjugaison pour un seul verbe:

```bash
python3 conjugue_moi.py manger
```

```
| Présent              | Imparfait            | Futur                | Passé simple         |
| -------------------- | -------------------- | -------------------- | -------------------- |
| je mange             | je mangeais          | je mangerai          | je mangeai           |
| tu manges            | tu mangeais          | tu mangeras          | tu mangeais          |
| il mange             | il mangeait          | il mangera           | il mangea            |
| nous mangeons        | nous mangions        | nous mangerons       | nous mangeâmes       |
| vous mangez          | vous mangiez         | vous mangerez        | vous mangeâtes       |
| ils mangent          | ils mangeaient       | ils mangeront        | ils mangèrent        |
```

| Présent              | Imparfait            | Futur                | Passé simple         |
| -------------------- | -------------------- | -------------------- | -------------------- |
| je mange             | je mangeais          | je mangerai          | je mangeai           |
| tu manges            | tu mangeais          | tu mangeras          | tu mangeais          |
| il mange             | il mangeait          | il mangera           | il mangea            |
| nous mangeons        | nous mangions        | nous mangerons       | nous mangeâmes       |
| vous mangez          | vous mangiez         | vous mangerez        | vous mangeâtes       |
| ils mangent          | ils mangeaient       | ils mangeront        | ils mangèrent        |


## Notes

Le verbe à conjuguer n'a pas besoin d'exister dans le dictionnaire, le programme se basera sur sa
terminaison pour le conjuguer.

Exemple:

```bash
python3 conjugue_moi.py tramontir
```

| Présent              | Imparfait            | Futur                | Passé simple         |
| -------------------- | -------------------- | -------------------- | -------------------- |
| je tramontis         | je tramontissais     | je tramontirai       | je tramontis         |
| tu tramontis         | tu tramontissais     | tu tramontiras       | tu tramontis         |
| il tramontit         | il tramontissait     | il tramontira        | il tramontit         |
| nous tramontissons   | nous tramontissions  | nous tramontirons    | nous tramontîmes     |
| vous tramontissez    | vous tramontissiez   | vous tramontirez     | vous tramontîtes     |
| ils tramontissent    | ils tramontissaient  | ils tramontiront     | ils tramontirent     |
