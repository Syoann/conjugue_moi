#! /usr/bin/env python3

import re


class Tense:
    """Classe générique d'un temps"""
    terminations = []
    pronouns = ["je", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles"]


    @classmethod
    def conjugate(self, verb, interrogative=False):
        """
        Conjugue n'importe quel verbe dans ce temps.
        """

        # On trie les terminaisons par ordre décroissant de taille afin de matcher le plus
        # précisement possible
        for suffix in sorted(self.terminations.keys(), key=lambda k: len(k), reverse=True):
            if verb.endswith(suffix):
                radical = verb[:-len(suffix)]
                terms = self.terminations[suffix]
                extended_terminations = terms[0:2] + [terms[2]] * 3 + terms[3:] + [terms[5]]
                pronouns = list(self.pronouns)

                # Forme interrogative
                if interrogative:
                    # On remplace .....e-je par .....é-je (exemple: demande-je devient demandé-je)
                    if extended_terminations[0] is not None and extended_terminations[0].endswith("e"):
                        extended_terminations[0] = extended_terminations[0][:-1]+ "é"

                    # Ajout de '-t-' si voyelle en fin de verbe
                    if extended_terminations[2].endswith(tuple("aeiou")):
                        pronouns[2:5] = ["t-il", "t-elle", "t-on"]

                    # Remplacement des terminaisons "è.é-je" par "e.é-je"
                    # exemple: "pèlé-je" devient "pelé-je"
                    base_verbale = [f"{radical}{term}" if term is not None else None for term in extended_terminations]
                    if base_verbale[0]:
                        base_verbale[0] = re.sub(r'è(.)é$', 'e\g<1>é', base_verbale[0])

                    return([f"{verb}-{pronoun} ?" for pronoun, verb in zip(pronouns, base_verbale) if base_verbale is not None])
                # Forme classique
                else:
                    pronouns = [pronoun + " " for pronoun in pronouns]
                    # "j'" si le verbe commence par une voyelle
                    if terms[0] is not None and (radical + terms[0]).startswith(tuple("aeéèêiou")):
                        pronouns[0] = "j'"

                    return [f"{pronoun}{radical}{term}" for pronoun, term in zip(pronouns, extended_terminations) if term is not None]
        return [None]



class IndicatifPresent(Tense):
    """Règles de conjugaison pour le présent de l'indicatif"""

    def generate_eacute_terms():
        result = {}
        # Terminaisons où "é" devient "è" pour les 3 premières personnes du singulier et la 3ème
        # du pluriel
        for term in ["ébrer", "écer", "écher", "écrer", "éder", "égler", "égner", "égrer", "éguer",
                     "éler", "émer", "éner", "équer", "érer", "éser", "éter", "étrer", "évrer",
                     "éyer"]:
            result[term] = ["è" + term[1:-2] + t for t in ["e", "es", "e"]] + \
                           [      term[0:-2] + t for t in ["ons", "ez"]] + \
                           ["è" + term[1:-2] + t for t in ["ent"]]
        return result

    def generate_exceptions():
        result = {}

        for term in ["celer", "ciseler", "démanteler", "écarteler", "encasteler", "geler",
                     "marteler", "modeler", "peler", "acheter", "bégueter", "corseter", "crocheter",
                     "fileter", "fureter", "haleter"]:
            rad = term[:-4]
            result[term] = [rad + "è" + term[-3] + t for t in ["e", "es", "e"]] + \
                           [rad + "e" + term[-3] + t for t in ["ons", "ez"]] + \
                           [rad + "è" + term[-3] + t for t in ["ent"]]

        return result


    terminations_group1 = {"appeler": ["appelle", "appelles", "appelle", "appelons", "appelez", "appellent"],
                           "dire": ["dis", "dis", "dit", "disons", "dites", "disent"],
                           "evrer": ["èvre", "èvres", "èvre", "evrons", "evrez", "èvrent"],
                           "emer": ["ème", "èmes", "ème", "emons", "emez", "èment"],
                           "eper": ["èpe", "èpes", "èpes", "epons", "epez", "èpent"],
                           "erer": ["ère", "ères", "ère", "erons", "erez", "èrent"],
                           "eser": ["èse", "èses", "èse", "esons", "esez", "èsent"],
                           "ever": ["ève", "èves", "ève", "evons", "evez", "èvent"],
                           "oyer": ["oie", "oies", "oie", "oyons", "oyez", "oient"],
                           "uyer": ["uie", "uies", "uie", "uyons", "uyez", "uient"],
                           "ecer": ["èce", "èces", "èce", "eçons", "ecez", "ècent"],
                           "eler": ["elle", "elles", "elle", "elons", "elez", "ellent"],
                           "eter": ["ette", "ettes", "ette", "etons", "etez", "ettent"],
                           "cer": ["ce", "ces", "ce", "çons", "cez", "cent"],
                           "ger": ["ge", "ges", "ge", "geons", "gez", "gent"],
                           "er": ["e", "es", "e", "ons", "ez", "ent"]}

    terminations_group2 = {"ir": ["is", "is", "it", "issons", "issez", "issent"],
                           "ïr": ["is", "is", "ït", "ïssons", "ïssez", "ïssent"]}

    terminations_group3 = {"aillir": ["aux", "aux", "aut", "aillons", "aillez", "aillent"],
                           "aindre": ["ains", "ains", "aint", "aignons", "aignez", "aignent"],
                           "aller": ["vais", "vas", "va", "allons", "allez", "vont"],
                           "asseoir": ["assieds", "assieds", "assied", "asseyons", "asseyez", "asseyent"],
                           "astreindre": ["astreins", "astreins", "astreint", "astreignons", "astreignez", "astraignent"],
                           "avoir": ["ai", "as", "a", "avons", "avez", "ont"],
                           "battre": ["bats", "bats", "bat", "battons", "battez", "battent"],
                           "boire": ["bois", "bois", "boit", "buvons", "buvez", "boivent"],
                           "bouillir": ["bous", "bous", "bout", "bouillons", "bouillez", "bouillent"],
                           "cevoir": ["çois", "çois", "çoit", "cevons", "cevez", "çoivent"],
                           "choir": ["chois", "chois", "choit", "choyons", "choyez", "choient"],
                           "circoncire": ["circoncis", "circoncis", "circoncit", "circoncisons", "circoncisez", "circoncisent"],
                           "clore": ["clos", "clos", "clôt", None, None, "closent"],
                           "clure": ["clus", "clus", "clut", "cluons", "cluez", "cluent"],
                           "confire": ["confis", "confis", "confit", "confisons", "confisez", "confisent"],
                           "coudre": ["couds", "couds", "coud", "cousons", "cousez", "cousent"],
                           "courir": ["cours", "cours", "court", "courons", "courez", "courent"],
                           "croire": ["crois", "crois", "croit", "croyons", "croyez", "croient"],
                           "croître": ["croîs", "croîs", "croît", "croissons", "croissez", "croissent"],
                           "cueillir": ["cueille", "cueilles", "cueille", "cueillons", "cueillez", "cueillent"],
                           "descendre": ["descends", "descends", "descend", "descendons", "descendez", "descendent"],
                           "devoir": ["dois", "dois", "doit", "devons", "devez", "doivent"],
                           "dormir": ["dors", "dors", "dort", "dormons", "dormez", "dorment"],
                           "écrire": ["écris", "écris", "écrit", "écrivons", "écrivez", "écrivent"],
                           "eindre": ["eins", "eins", "eint", "eignons", "eignez", "eignent"],
                           "épandre": ["épands","épands", "épand", "épandons", "épandez", "épandent"],
                           "être": ["suis", "es", "est", "sommes", "êtes", "sont"],
                           "faire": ["fais", "fais", "fait", "faisons", "faites", "font"],
                           "falloir": [None, None, "faut", None, None, None],
                           "fendre": ["fends", "fends", "fend", "fendons", "fendez", "fendent"],
                           "fondre": ["fonds", "fonds", "fond", "fondons", "fondez", "fondent"],
                           "foutre": ["fous", "fous", "fout", "foutons", "foutez", "foutent"],
                           "frire": ["fris", "fris", "frit", None, None, None],
                           "fuir": ["fuis", "fuis", "fuit", "fuyons", "fuyez", "fuient"],
                           "gésir": ["gis", "gis", "gît", "gisons", "gisez", "gisent"],
                           "joindre": ["joins", "joins", "joint", "joignons", "joignez", "joignent"],
                           "lire": ["lis", "lis", "lit", "lisons", "lisez", "lisent"],
                           "mentir": ["mens", "mens", "ment", "mentons", "mentez", "mentent"],
                           "mettre": ["mets", "mets", "met", "mettons", "mettez", "mettent"],
                           "mordre": ["mords", "mords", "mord", "mordons", "mordez", "mordent"],
                           "moudre": ["mouds", "mouds", "moud", "moulons", "moulez", "moulent"],
                           "mourir": ["meurs", "meurs", "meurt", "mourons", "mourez", "meurent"],
                           "mouvoir": ["meus", "meus", "meut", "mouvons", "mouvez", "meuvent"],
                           "naître": ["nais", "nais", "naît", "naissons", "naissez", "naissent"],
                           "offrir": ["offre", "offres", "offre", "offrons", "offrez", "offrent"],
                           "oindre": ["oins", "oins", "oint", "oignons", "oignez", "oignent"],
                           "ouïr": ["ois", "ois", "oit", "oyons", "oyez", "oient"],
                           "ouvrir": ["ouvre", "ouvres", "ouvre", "ouvrons", "ouvrez", "ouvrent"],
                           "paître": ["pais", "pais", "paît", "paissons", "paissez", "paissent"],
                           "paraître": ["parais", "parais", "paraît", "paraissons", "paraissez", "paraissent"],
                           "partir": ["pars", "pars", "part", "partons", "partez", "partent"],
                           "pendre": ["pends", "pends", "pend", "pendons", "pendez", "pendent"],
                           "perdre": ["perds", "perds", "perd", "perdons", "perdez", "perdent"],
                           "plaire": ["plais", "plais", "plaît", "plaisons", "plaisez", "plaisent"],
                           "pleuvoir": [None, None, "pleut", None, None, "pleuvent"],
                           "poindre": [None, None, "point", None, None, "poignent"],
                           "pondre": ["ponds", "ponds", "pond", "pondons", "pondez", "pondent"],
                           "pouvoir": ["peux", "peux", "peut", "pouvons", "pouvez", "peuvent"],
                           "prendre": ["prends", "prends", "prend", "prenons", "prenez", "prennent"],
                           "prévoir": ["prévois", "prévois", "prévoit", "prévoyons", "prévoyez", "prévoient"],
                           "quérir": ["quiers", "quiers", "quiert", "quérons", "quérez", "quièrent"],
                           "raire": ["rais", "rais", "rait", "rayons", "rayez", "raient"],
                           "rendre": ["rends", "rends", "rend", "rendons", "rendez", "rendent"],
                           "repentir": ["repens", "repens", "repent", "repentons", "repentez", "repentent"],
                           "rire": ["ris", "ris", "rit", "rions", "riez", "rient"],
                           "rompre": ["romps", "romps", "rompt", "rompons", "rompez", "rompent"],
                           "saillir": ["saille", "sailles", "saille", "saillons", "saillez", "saillent"],
                           "savoir": ["sais", "sais", "sait", "savons", "savez", "savent"],
                           "scrire": ["scris", "scris", "scrit", "scrivons", "scrivez", "scrivent"],
                           "sentir": ["sens", "sens", "sent", "sentons", "sentez", "sentent"],
                           "servir": ["sers", "sers", "sert", "servons", "servez", "servent"],
                           "seoir": [None, None, "sied", None, None, "siéent"],
                           "suivre": ["suis", "suis", "suit", "suivons", "suivez", "suivent"],
                           "sortir": ["sors", "sors", "sort", "sortons", "sortez", "sortent"],
                           "soudre": ["sous", "sous", "sout", "solvons", "solvez", "solvent"],
                           "souffre": ["souffre", "souffres", "souffre", "souffrons", "souffrez", "souffrent"],
                           "suffire": ["suffis", "suffis", "suffit", "suffisons", "suffisez", "suffisent"],
                           "surseoir": ["sursois", "sursois", "sursoit", "sursoyons", "sursoyez", "sursoient"],
                           "taire": ["tais", "tais", "tait", "taisons", "taisez", "taisent"],
                           "tendre": ["tends", "tends", "tend", "tendons", "tendez", "tendent"],
                           "tenir": ["tiens", "tiens", "tient", "tenons", "tenez", "tiennent"],
                           "tondre": ["tonds", "tonds", "tond", "tondons", "tondez", "tondent"],
                           "tordre": ["tords", "tords", "tord", "tordons", "tordez", "tordent"],
                           "uire": ["uis", "uis", "uit", "uisons", "uisez", "uisent"],
                           "vaincre": ["vaincs", "vaincs", "vainc", "vainquons", "vainquez", "vainquent"],
                           "valoir": ["vaux", "vaux", "vaut", "valons", "valez", "valent"],
                           "vendre": ["vends", "vends", "vend", "vendons", "vendez", "vendent"],
                           "venir": ["viens", "viens", "vient", "venons", "venez", "viennent"],
                           "vêtir": ["vêts", "vêts", "vêt", "vêtons", "vêtez", "vêtent"],
                           "vivre": ["vis", "vis", "vit", "vivons", "vivez", "vivent"],
                           "voir": ["vois", "vois", "voit", "voyons", "voyez", "voient"],
                           "vouloir": ["veux", "veux", "veut", "voulons", "voulez", "veulent"]}


    terminations_group1.update(generate_eacute_terms())
    terminations_group1.update(generate_exceptions())

    terminations = {**terminations_group1, **terminations_group2, **terminations_group3}


class IndicatifFutur(Tense):
    """
    Futur de l'indicatif
    """
    def generate_exceptions():
        result = {}

        for term in ["celer", "ciseler", "démanteler", "écarteler", "encasteler", "geler",
                     "marteler", "modeler", "peler", "acheter", "bégueter", "corseter", "crocheter",
                     "fileter", "fureter", "haleter"]:
            rad = term[:-4]
            result[term] = [rad + "è" + term[-3] + t for t in ["erai", "eras", "era", "erons", "erez", "eront"]]
        return result


    terminations_group1 = {"yer": ["ierai", "ieras", "iera", "yerons", "yerez", "ieront"],
                           "er": ["erai", "eras", "era", "erons", "erez", "eront"],
                           "appeler": ["appellerai", "appelleras", "appellera", "appellerons", "appellerez", "appelleront"],
                           "eler": ["ellerai", "elleras", "ellera", "elleront", "ellerez", "elleront"],
                           "eter": ["etterai", "etteras", "ettera", "etteront", "etterez", "etteront"]}

    terminations_group1.update(generate_exceptions())

    terminations_group2 = {"ir": ["irai", "iras", "ira", "irons", "irez", "iront"],
                           "ïr": ["ïrai", "ïras", "ïra", "ïrons", "ïrez", "ïront"]}
    terminations_group3 = {"e": ["ai", "as", "a", "ons", "ez", "ont"],
                           "": ["ai", "as", "a", "ons", "ez", "ont"],
                           "aller": ["irai", "iras", "ira", "irons", "irez", "iront"],
                           "avoir": ["aurai", "auras", "aura", "auront", "aurez", "auront"],
                           "être": ["serai", "seras", "sera", "serons", "serez", "seront"],
                           "asseoir": ["assoirai", "assoiras", "assoira", "assoirons", "assoirez", "assoiront"],
                           "cevoir": ["cevrai", "cevras", "cevra", "cevrons", "cevrez", "cevront"],
                           "courir": ["courrai", "courras", "courra", "courrons", "courrez", "courront"],
                           "cueillir": ["cueillerai", "cueilleras", "cueillera", "cueillerons", "cueillerez", "cueilleront"],
                           "devoir": ["devrai", "devras", "devra", "devrons", "devrez", "devront"],
                           "faire": ["ferais", "feras", "fera", "ferons", "ferez", "feront"],
                           "falloir": [None, None, "faudra", None, None, None],
                           "gésir": [None, None, None, None, None, None],
                           "mourir": ["mourrai", "mourras", "mourra", "mourrons", "mourrez", "mourront"],
                           "mouvoir": ["mouvrai", "mouvras", "mouvra", "mouvrons", "mouvrez", "mouvront"],
                           "pleuvoir": [None, None, "pleuvra", None, None, "pleuvront"],
                           "poindre": [None, None, "poindra", None, None, "poindront"],
                           "pouvoir": ["pourrai", "pourras", "pourra", "pourrons", "pourrez", "pourront"],
                           "savoir": ["saurai", "sauras", "saura", "saurons", "saurez", "sauront"],
                           "seoir": [None, None, "siéra", None, None, "siéront"],
                           "tenir": ["tiendrai", "tiendras", "tiendra", "tiendrons", "tiendrez", "tiendront"],
                           "vaincre": ["vaincrai", "vaincras", "vaincra", "vaincrons", "vaincrez", "vaincront"],
                           "valoir": ["vaudrai", "vaudras", "vaudra", "vaudrons", "vaudrez", "vaudront"],
                           "venir": ["viendrai", "viendras", "viendra", "viendrons", "viendrez", "viendront"],
                           "voir": ["verrai", "verras", "verra", "verrons", "verrez", "verront"],
                           "vouloir": ["voudrai", "voudras", "voudra", "voudrons", "voudrez", "voudront"]}


    terminations = {**terminations_group1, **terminations_group2, **terminations_group3}


class IndicatifImparfait(Tense):
    """
    Imparfait de l'indicatif
    """

    terminations_group1 = {"er": ["ais", "ais", "ait", "ions", "iez", "aient"],
                           "ger": ["geais", "geais", "geait", "gions", "giez", "geaient"]}
    terminations_group2 = {"ir": ["issais", "issais", "issait", "issions", "issiez", "issaient"],
                           "ïr": ["ïssais", "ïssais", "ïssait", "ïssions", "ïssiez", "ïssaient"]}
    terminations_group3 = {"avoir": ["avais", "avais", "avait", "avions", "aviez", "avaient"],
                           "être": ["étais", "étais", "était", "étions", "étiez", "étaient"]}

    terminations = {**terminations_group1, **terminations_group2, **terminations_group3}


class IndicatifPasseSimple(Tense):
    """
    Passé simple
    """

    terminations_group1 = {"er": ["ai", "ais", "a", "âmes", "âtes", "èrent"],
                           "ger": ["geai", "geais", "gea", "geâmes", "geâtes", "gèrent"]}
    terminations_group2 = {"ir": ["is", "is", "it", "îmes", "îtes", "irent"],
                           "ïr": ["ïs", "ïs", "ït", "ïmes", "ïtes", "ïrent"]}
    terminations_group3 = {"avoir": ["eus", "eus", "eut", "eûmes", "eûtes", "eurent"],
                           "être": ["fus", "fus", "fut", "fûmes", "fûtes", "furent"]}

    terminations = {**terminations_group1, **terminations_group2, **terminations_group3}


class ConditionnelPresent(Tense):
    terminations_group1 = {"er": ["erais", "erais", "erait", "erions", "eriez", "eraient"]}
    terminations_group2 = {"ir": ["irais", "irais", "irait", "irions", "iriez", "iraient"],
                           "ïr": ["ïrais", "ïrais", "ïrait", "ïrions", "ïriez", "ïraient"]}
    terminations_group3 = {"avoir": ["aurais", "aurais", "aurait", "aurions", "auriez", "auraient"],
                           "être": ["serais", "serais", "serait", "serions", "seriez", "seraient"]}

    terminations = {**terminations_group1, **terminations_group2, **terminations_group3}


def conjugate(verb, tense, interrogative=False):
    """
    Conjugue un verbe au temps demandé. Possibilité d'avoir la forme interrogative.

    Parameters
    ----------
    verb : string
        verbe à conjuguer
    tense : string
        temps à utiliser
    interrogative : bool
        utiliser la forme interrogative ? False par défaut
    """
    return tense.conjugate(verb, interrogative)




if __name__ == "__main__":
    import os
    import sys

    arg1 = sys.argv[1]

    tenses = {"Présent": IndicatifPresent,
              "Imparfait": IndicatifImparfait,
              "Futur": IndicatifFutur,
              "Passé simple": IndicatifPasseSimple,
              "Conditionnel": ConditionnelPresent}


    # Fichier en entrée, dictionnaire en sortie
    if os.path.isfile(arg1):
        with open(arg1) as fh:
            for line in fh:
                verb = line[:-1].lower()

                for tense in tenses:
                    [print(result) for result in conjugate(verb, tenses[tense]) if result is not None]
                    [print(result) for result in conjugate(verb, tenses[tense], interrogative=True) if result is not None]
    # Verbe en entrée, tableau de conjugaison en sortie
    else:
        verb = arg1
        header = "|"
        delim = "| --- " * len(tenses) + "|"
        output = ["|"] * 6

        for tense in tenses:
            header += f" {tense} |"
            conjug = [result for result in conjugate(verb, tenses[tense])]

            for i, index in enumerate([0, 1, 2, 5, 6, 7]):
                output[i] += f" {conjug[index]} |"

        print(header)
        print(delim)

        for line in output:
            print(line)

