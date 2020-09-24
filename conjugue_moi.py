#! /usr/bin/env python3

import re


class Tense:
    """Classe générique d'un temps"""
    terminations = {}

    PRONOUNS = {"1ps": ["je"],
                "2ps": ["tu"],
                "3ps": ["il", "elle", "on"],
                "1pp": ["nous"],
                "2pp": ["vous"],
                "3pp": ["ils", "elles"]}

    @classmethod
    def conjugate(cls, verb, interrogative=True):
        """
        Conjugue n'importe quel verbe dans ce temps.
        Retourne un dicitonnaire avec seulement le verbe conjugué
        """

        # Initialisation du résultat sous forme de dictionnaire de dictionnaire
        # Le résultat est de type {"1ps": {"je": "je mange"}, "2ps": {"tu": "tu manges"}, ...}
        result = dict()
        for person, pronouns in cls.PRONOUNS.items():
            result[person] = {}
            for pronoun in pronouns:
                result[person][pronoun] = None

        # On trie les terminaisons par ordre décroissant de taille afin de matcher le plus
        # précisement possible
        for suffix in sorted(cls.terminations.keys(), key=lambda k: len(k), reverse=True):
            if verb.endswith(suffix):
                radical = verb[:-len(suffix)]

                for person, term in zip(cls.PRONOUNS.keys(), cls.terminations[suffix]):
                    if term is not None:
                        for pronoun in cls.PRONOUNS[person]:
                            if interrogative:
                                result[person][pronoun] = cls._get_interrogative_form(radical + term, pronoun, person)
                            else:
                                result[person][pronoun] = cls._get_simple_form(radical + term, pronoun, person)

                break

        return result

    @classmethod
    def _get_interrogative_form(cls, verb, pronoun, person):
        if person == "1ps":
            # On remplace .....e-je par .....é-je (exemple: demande-je devient demandé-je)
            if verb.endswith("e"):
                verb = verb[:-1] + "é"

            # Remplacement des terminaisons "è.é-je" par "e.é-je"
            # exemple: "pèlé-je" devient "pelé-je"
            verb = re.sub(r'è(.)é$', r'e\g<1>é', verb)

        # Ajout de '-t-' avec il/elle et ils/elles si voyelle en fin de verbe
        if person in ["3ps", "3pp"] and verb.endswith("aeiou"):
            verb = verb + "-t"

        return f"{verb}-{pronoun} ?"

    @classmethod
    def _get_simple_form(cls, verb, pronoun, person):
        # "j'" si le verbe commence par une voyelle
        if pronoun == "je" and verb.startswith(tuple("aeéèêiou")):
            return f"j'{verb}"
        return f"{pronoun} {verb}"


class IndicatifPresent(Tense):
    """Règles de conjugaison pour le présent de l'indicatif"""

    @staticmethod
    def generate_eacute_terms():
        """Générer les terminaisons pour les verbes avec un accent aigu"""
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

    @staticmethod
    def generate_exceptions_group1():
        """Génerer les terminaisons pour les exceptions du 1er groupe"""
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
                           "avoir": ["ai", "as", "a", "avons", "avez", "ont"],
                           "battre": ["bats", "bats", "bat", "battons", "battez", "battent"],
                           "boire": ["bois", "bois", "boit", "buvons", "buvez", "boivent"],
                           "bouillir": ["bous", "bous", "bout", "bouillons", "bouillez", "bouillent"],
                           "cevoir": ["çois", "çois", "çoit", "cevons", "cevez", "çoivent"],
                           "choir": ["chois", "chois", "choit", "choyons", "choyez", "choient"],
                           "concire": ["concis", "concis", "concit", "concisons", "concisez", "concisent"],
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
                           "épandre": ["épands", "épands", "épand", "épandons", "épandez", "épandent"],
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

    terminations_group1.update(generate_eacute_terms.__func__())
    terminations_group1.update(generate_exceptions_group1.__func__())

    terminations = {**terminations_group1, **terminations_group2, **terminations_group3}


class IndicatifFutur(Tense):
    """
    Futur de l'indicatif
    """

    @staticmethod
    def generate_exceptions_group1():
        result = {}

        for term in ["celer", "ciseler", "démanteler", "écarteler", "encasteler", "geler",
                     "marteler", "modeler", "peler", "acheter", "bégueter", "corseter", "crocheter",
                     "fileter", "fureter", "haleter"]:
            rad = term[:-4]
            result[term] = [rad + "è" + term[-3] + t for t in ["erai", "eras", "era", "erons", "erez", "eront"]]
        return result

    terminations_group1 = {"yer": ["ierai", "ieras", "iera", "yerons", "yerez", "ieront"],
                           "er": ["erai", "eras", "era", "erons", "erez", "eront"],
                           "appeler": ["appellerai", "appelleras", "appellera",
                                       "appellerons", "appellerez", "appelleront"],
                           "eler": ["ellerai", "elleras", "ellera", "elleront", "ellerez", "elleront"],
                           "eter": ["etterai", "etteras", "ettera", "etteront", "etterez", "etteront"]}

    terminations_group1.update(generate_exceptions_group1.__func__())

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
                           "cueillir": ["cueillerai", "cueilleras", "cueillera",
                                        "cueillerons", "cueillerez", "cueilleront"],
                           "devoir": ["devrai", "devras", "devra", "devrons", "devrez", "devront"],
                           "faire": ["ferais", "feras", "fera", "ferons", "ferez", "feront"],
                           "falloir": [None, None, "faudra", None, None, None],
                           "gésir": [None, None, None, None, None, None],
                           "mourir": ["mourrai", "mourras", "mourra", "mourrons", "mourrez", "mourront"],
                           "mouvoir": ["mouvrai", "mouvras", "mouvra", "mouvrons", "mouvrez", "mouvront"],
                           "oindre": ["oindrai", "oindras", "oindra", "oindrons", "oindrez", "oindront"],
                           "pleuvoir": [None, None, "pleuvra", None, None, "pleuvront"],
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

    @staticmethod
    def generate_terminations_group3():
        """
        Génère automatiquement les terminaisons de l'imparfait des verbes du 3ème groupe à partir
        de la conjugaison au présent pour la première personne du pluriel.
        """
        terminations_imparfait = {}

        # Récupération des terminaisons du présent de l'indicatif
        for term, conjug in IndicatifPresent.terminations_group3.items():
            if conjug[3] is None:
                continue

            # Suppression de '-ons' à la première personne du pluriel pour former le radical
            radical = conjug[3][:-3]

            # Génération des terminaisons
            terminations_imparfait[term] = [radical + t for t in ["ais", "ais", "ait", "ions", "iez", "aient"]]

        return terminations_imparfait

    terminations_group1 = {"er": ["ais", "ais", "ait", "ions", "iez", "aient"],
                           "ger": ["geais", "geais", "geait", "gions", "giez", "geaient"]}
    terminations_group2 = {"ir": ["issais", "issais", "issait", "issions", "issiez", "issaient"],
                           "ïr": ["ïssais", "ïssais", "ïssait", "ïssions", "ïssiez", "ïssaient"]}

    terminations_group3 = generate_terminations_group3.__func__()
    terminations_group3.update({"être": ["étais", "étais", "était", "étions", "étiez", "étaient"],
                                "falloir": [None, None, "fallait", None, None, None],
                                "frire": [None, None, None, None, None, None],
                                "pleuvoir": [None, None, "pleuvait", None, None, "pleuvaient"],
                                "seoir": [None, None, "seyait", None, None, "seyaient"]})

    terminations = {**terminations_group1, **terminations_group2, **terminations_group3}


class IndicatifPasseSimple(Tense):
    """
    Passé simple
    """

    @staticmethod
    def generate_terminations_group3(radical, terms):
        return [radical + term for term in terms]

    terminations_group1 = {"er": ["ai", "as", "a", "âmes", "âtes", "èrent"],
                           "ger": ["geai", "geais", "gea", "geâmes", "geâtes", "gèrent"]}
    terminations_group2 = {"ir": ["is", "is", "it", "îmes", "îtes", "irent"],
                           "ïr": ["ïs", "ïs", "ït", "ïmes", "ïtes", "ïrent"]}

    _TERMS_A = ["ai", "as", "a", "âmes", "âtes", "èrent"]
    _TERMS_U = ["us", "us", "ut", "ûmes", "ûtes", "urent"]
    _TERMS_I = ["is", "is", "it", "îmes", "îtes", "irent"]
    _TERMS_IN = ["ins", "ins", "int", "înmes", "întes", "inrent"]

    terminations_group3 = {"avoir": ["eus", "eus", "eut", "eûmes", "eûtes", "eurent"],
                           "être": ["fus", "fus", "fut", "fûmes", "fûtes", "furent"],
                           "aller": generate_terminations_group3.__func__("all", _TERMS_A),
                           "asseoir": generate_terminations_group3.__func__("ass", _TERMS_I),
                           "battre": generate_terminations_group3.__func__("batt", _TERMS_I),
                           "boire": generate_terminations_group3.__func__("b", _TERMS_U),
                           "cevoir": generate_terminations_group3.__func__("ç", _TERMS_U),
                           "choir": generate_terminations_group3.__func__("ch", _TERMS_U),
                           "concire": generate_terminations_group3.__func__("conc", _TERMS_I),
                           "clore": [None, None, None, None, None, None],
                           "clure": generate_terminations_group3.__func__("cl", _TERMS_U),
                           "confire": generate_terminations_group3.__func__("conf", _TERMS_I),
                           "coudre": generate_terminations_group3.__func__("cous", _TERMS_I),
                           "courir": generate_terminations_group3.__func__("cour", _TERMS_U),
                           "croire": generate_terminations_group3.__func__("cr", _TERMS_U),
                           "croître": ["crûs", "crûs", "crût", "crûmes", "crûtes", "crûrent"],
                           "devoir": generate_terminations_group3.__func__("d", _TERMS_U),
                           "dre": generate_terminations_group3.__func__("d", _TERMS_I),
                           "écrire": generate_terminations_group3.__func__("écriv", _TERMS_I),
                           "faire": generate_terminations_group3.__func__("f", _TERMS_I),
                           "falloir": [None, None, "fallut", None, None, None],
                           "foutre": generate_terminations_group3.__func__("fout", _TERMS_I),
                           "frire": ["fris", "fris", "frit", None, None, None],
                           "gésir": [None, None, None, None, None, None],
                           "indre": generate_terminations_group3.__func__("ign", _TERMS_I),
                           "lire": generate_terminations_group3.__func__("l", _TERMS_U),
                           "mettre": generate_terminations_group3.__func__("m", _TERMS_I),
                           "moudre": generate_terminations_group3.__func__("moul", _TERMS_U),
                           "mouvoir": generate_terminations_group3.__func__("m", _TERMS_U),
                           "naître": generate_terminations_group3.__func__("naqu", _TERMS_I),
                           "oindre": generate_terminations_group3.__func__("oign", _TERMS_I),
                           "ouïr": [None, None, None, None, None, None],
                           "paître": [None, None, None, None, None, None],
                           "paraître": generate_terminations_group3.__func__("par", _TERMS_U),
                           "plaire": generate_terminations_group3.__func__("pl", _TERMS_U),
                           "pleuvoir": [None, None, "plut", None, None, None],
                           "pouvoir": generate_terminations_group3.__func__("p", _TERMS_U),
                           "prendre": generate_terminations_group3.__func__("pr", _TERMS_I),
                           "prévoir": generate_terminations_group3.__func__("prév", _TERMS_I),
                           "raire": [None, None, None, None, None, None],
                           "rire": generate_terminations_group3.__func__("r", _TERMS_I),
                           "rompre": generate_terminations_group3.__func__("romp", _TERMS_I),
                           "savoir": generate_terminations_group3.__func__("s", _TERMS_U),
                           "scrire": generate_terminations_group3.__func__("scriv", _TERMS_I),
                           "seoir": [None, None, None, None, None, None],
                           "suivre": generate_terminations_group3.__func__("suiv", _TERMS_I),
                           "soudre": generate_terminations_group3.__func__("sol", _TERMS_U),
                           "souffre": generate_terminations_group3.__func__("souffr", _TERMS_I),
                           "suffire": generate_terminations_group3.__func__("suff", _TERMS_I),
                           "surseoir": generate_terminations_group3.__func__("surs", _TERMS_I),
                           "taire": generate_terminations_group3.__func__("t", _TERMS_U),
                           "tenir": generate_terminations_group3.__func__("t", _TERMS_IN),
                           "uire": generate_terminations_group3.__func__("uis", _TERMS_I),
                           "vaincre": generate_terminations_group3.__func__("vainqu", _TERMS_I),
                           "valoir": generate_terminations_group3.__func__("val", _TERMS_U),
                           "venir": generate_terminations_group3.__func__("v", _TERMS_IN),
                           "vêtir": generate_terminations_group3.__func__("vêt", _TERMS_I),
                           "vivre": generate_terminations_group3.__func__("véc", _TERMS_U),
                           "voir": generate_terminations_group3.__func__("v", _TERMS_I),
                           "vouloir": generate_terminations_group3.__func__("voul", _TERMS_U)}

    terminations = {**terminations_group1, **terminations_group2, **terminations_group3}


class ConditionnelPresent(Tense):
    """
    Conditionnel présent
    """

    @staticmethod
    def generate_terminations():
        """
        Génère automatiquement les terminaisons du conditionnel à partir de la conjugaison au futur
        de la première personne du pluriel.
        """
        terminations_conditionnel = {}

        # Récupération des terminaisons du présent de l'indicatif
        for term, conjug in IndicatifFutur.terminations.items():
            if conjug[3] is None:
                continue

            # Suppression de '-ons' à la première personne du pluriel pour former le radical
            radical = conjug[3][:-3]

            # Génération des terminaisons
            terminations_conditionnel[term] = [radical + t for t in ["ais", "ais", "ait", "ions", "iez", "aient"]]

        return terminations_conditionnel

    terminations = generate_terminations.__func__()


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

    # Fichier en entrée liste en sortie
    if os.path.isfile(arg1):
        with open(arg1) as fh:
            for line in fh:
                verb = line[:-1].lower()

                for tense in tenses:
                    conjug = conjugate(verb, tenses[tense])
                    for person in conjug:
                        for pronoun in conjug[person]:
                            if conjug[person][pronoun] is not None:
                                print(conjug[person][pronoun])

                    conjug = conjugate(verb, tenses[tense], interrogative=True)
                    for person in conjug:
                        for pronoun in conjug[person]:
                            if conjug[person][pronoun] is not None:
                                print(conjug[person][pronoun])

    # Verbe en entrée, tableau de conjugaison en sortie
    else:
        verb = arg1
        header = "|"
        output = ["|"] * 6

        for tense_name, tense in tenses.items():
            header += f" {tense_name:20} |"
            conjug = conjugate(verb, tense)

            for i, person in enumerate(conjug):
                for result in conjug[person].values():
                    if result:
                        output[i] += f" {result:20} |"
                    else:
                        output[i] += " " * 20 + "  |"
                    break

        print(header)
        print(("| " + "-" * 20 + " ") * len(tenses) + "|")

        for line in output:
            print(line)
