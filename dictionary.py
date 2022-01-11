from collections import namedtuple

# verbs that conjugate with etre on passé composé, passé antérieur, et futur antérieur
_AUX_ETRE_VERBS = (
    "naître",
    "mourir",
    "sortir",
    "entrer",
    "monter",
    "descendre",
    "passer",
    "rester",
    "aller",
    "retourner",
    "venir",
    "partir",
    "tomber",
    "arriver",
    "devenir",
    "revenir",
)

_VERBS_IRREG = {
    ("être", "présent", "indicatif"):
        ("suis", "es", "est", "sommes", "êtes", "sont"),
    ("être", "passé simple", "indicatif"):
        ("'fus", "fus", "fut", "fûmes", "fûtes", "furent"),
    ("être", "futur", "indicatif"):
        ("serai", "seras", "sera", "serons", "serez", "seront"),
    ("être", "imparfait", "indicatif"):
        ("'étais", "étais", "était", "étions", "étiez", "étaient"),
    ("être", "présent", "participe"): "étant",
    ("être", "passé", "participe"): "été",
    ("avoir", "présent", "indicatif"):
        ("ai", "as", "a", "avons", "avez", "ont"),
    ("avoir", "passé simple", "indicatif"):
        ("'eus", "eus", "eut", "eûmes", "eûtes", "eurent"),
    ("avoir", "futur", "indicatif"):
        ("aurai", "auras", "aura", "aurons", "aurez", "auront"),
    ("avoir", "présent", "participe"): "ayant",
    ("avoir", "passé", "participe"): "eu",

    ("aller", "présent", "indicatif"):
        ("vais", "vas", "va", "allons", "allez", "vont"),
    ("aller", "futur", "indicatif"):
        ("irai", "iras", "ira", "irons", "irez", "iront"),
    ("aller", "présent", "participe"): "allant",
    ("aller", "passé", "participe"): "allé",
    ("appuyer", "présent", "indicatif"):
        ("appuie", "appuies", "appuie", "appuyons", "appuyez", "appuient"),
    ("apercevoir", "présent", "indicatif"):
        ("aperçois", "aperçois", "aperçoit", "apercevons", "apercevez", "aperçoivent"),
    ("apercevoir", "présent", "participe"): "apercevant",
    ("apercevoir", "passé", "participe"): "aperçu",
    ("apprendre", "présent", "indicatif"):
        ("apprends", "apprends", "apprend", "apprenons", "apprenez", "apprennet"),
    ("apprendre", "présent", "participe"): "apprenant",
    ("apprendre", "passé", "participe"): "appris",
    ("asseoir", "présent", "indicatif"):
        ("assieds", "assieds", "assied", "asseyons", "asseyez", "asseyent"),
    ("asseoir", "futur", "indicatif"):
        ("asseyerai", "asseyeras", "asseyera", "asseyerons", "asseyerez", "asseyerent"),
    ("asseoir", "présent", "participe"): "asseyant",
    ("asseoir", "passé", "participe"): "assis",
    ("atteindre", "présent", "indicatif"):
        ("atteins", "atteins", "atteint", "atteignons", "atteignez", "atteignent"),
    ("atteindre", "présent", "participe"): "atteignant",
    ("atteindre", "passé", "participe"): "atteint",
    ("attendre",  "présent", "indicatif"):
        ("attends", "attends", "attend", "attendons", "attendez", "attendent"),
("attendre", "présent", "participe"): "attendant",
    ("attendre", "passé", "participe"): "attendu",
    ("boire", "présent", "indicatif"):
        ("bois", "bois", "boit", "buvons", "buvez", "boivent"),
    ("boire", "présent", "participe"): "buvant",
    ("boire", "passé", "participe"): "bu",
    ("bouillir", "présent", "indicatif"):
        ("bous", "bous", "bout", "bouillons", "bouillez", "bouillent"),
    ("bouillir", "présent", "participe"): "bouillant",
    ("bouillir", "passé", "participe"): "bouilli",
    ("comprendre", "présent", "indicatif"):
        ("comprends", "comprends", "comprend", "comprenons", "comprenez", "comprennent"),
("comprendre", "présent", "participe"): "comprenant",
    ("comprendre", "passé", "participe"): "compris",
    ("conduire", "présent", "indicatif"):
        ("conduis", "conduis", "conduit", "conduisons", "conduisez", "conduisent"),
    ("conduire", "présent", "participe"): "conduisant",
    ("conduire", "passé", "participe"): "conduit",
    ("connaître", "présent", "indicatif"):
        ("connais", "connais", "connait", "connaissons", "connaissez", "connaissent"),
("connaître", "présent", "participe"): "connaissant",
    ("connaître", "passé", "participe"): "connu",
    ("courir", "présent", "indicatif"):
        ("cours", "cours", "court", "courons", "courez", "courent"),
("courir", "présent", "participe"): "courant",
    ("courir", "passé", "participe"): "couru",
    ("couvrir", "présent", "indicatif"):
        ("couvre", "couvres", "couvre", "couvrons", "couvrez", "couvrent"),
    ("couvrir", "présent", "participe"): "couvrant",
    ("couvrir", "passé", "participe"): "couvert",
("croire", "présent", "indicatif"):
        ("crois", "crois", "croit", "croyons", "croyez", "croient"),
    ("croire", "présent", "participe"): "croyant",
    ("croire", "passé", "participe"): "cru",
    ("cueillir", "présent", "indicatif"):
        ("cueille", "cueilles", "cueille", "cueillons", "cueillez", "cueillent"),
    ("cueillir", "présent", "participe"): "cueillant",
    ("cueillir", "passé", "participe"): "cueilli",
    ("cuire", "présent", "indicatif"):
        ("cuis", "cuis", "cuit", "cuisons", "cuisez", "cuisent"),
    ("cuire", "présent", "participe"): "cuisant",
    ("cuire", "passé", "participe"): "cuit",
    ("décevoir", "présent", "indicatif"):
        ("déçois", "déçois", "déçoit", "décevons", "décevez", "déçoivent"),
    ("décevoir", "présent", "participe"): "décevant",
    ("décevoir", "passé", "participe"): "déçu",
    ("découvrir", "présent", "indicatif"):
        ("découvre", "découvres", "découvre", "découvrons", "découvrez", "découvrent"),
    ("découvrir", "présent", "participe"): "découvrant",
    ("découvrir", "passé", "participe"): "découvert",
    ("déduire", "présent", "indicatif"):
        ("déduis", "déduis", "déduit", "déduisons", "déduisez", "déduisent"),
    ("déduire", "présent", "participe"): "déduisant",
    ("déduire", "passé", "participe"): "déduit",
    ("descendre", "présent", "indicatif"):
        ("descends", "descends", "descend", "descendons", "descendez", "descendent"),
    ("descendre", "présent", "participe"): "descendant",
    ("descendre", "passé", "participe"): "descendu",
    ("détendre", "présent", "indicatif"):
        ("détends", "détends", "détend", "détendons", "détendez", "détendent"),
    ("détendre", "présent", "participe"): "détendant",
    ("détendre", "passé", "participe"): "détendu",
    ("devenir", "présent", "indicatif"):
        ("deviens", "deviens", "devient", "devenons", "devenez", "deviennet"),
    ("devenir", "présent", "participe"): "devenant",
    ("devenir", "passé", "participe"): "devenu",
    ("devoir", "présent", "indicatif"):
        ("dois", "dois", "doit", "devons", "devez", "doivent"),
    ("devoir", "présent", "participe"): "devant",
    ("devoir", "passé", "participe"): "dû",
    ("dire", "présent", "indicatif"):
        ("dis", "dis", "dit", "disons", "disez", "disent"),
    ("dire", "présent", "participe"): "disant",
    ("dire", "passé", "participe"): "dit",
    ("disparaître", "présent", "indicatif"):
        ("disparais", "disparais", "disparait", "disparaissons", "disparaissez", "disparaissent"),
    ("disparaître", "présent", "participe"): "disparaissant",
    ("disparaître", "passé", "participe"): "disparu",
    ("dormir", "présent", "indicatif"):
        ("dors", "dors", "dort", "dormons", "dormez", "dorment"),
    ("dormir", "présent", "participe"): "dormant",
    ("dormir", "passé", "participe"): "dormi",
    ("écrire", "présent", "indicatif"):
        ("écris", "écris", "écrit", "écrivons", "écrivez", "écrivent"),
    ("écrire", "présent", "participe"): "écrivant",
    ("écrire", "passé", "participe"): "écrit",
("enduire", "présent", "indicatif"):
        ("enduis", "enduis", "enduit", "enduisons", "enduisez", "enduisent"),
    ("enduire", "présent", "participe"): "enduisant",
    ("enduire", "passé", "participe"): "enduit",
    ("entendre", "présent", "indicatif"):
        ("entends", "entends", "entend", "entendons", "entendez", "entendent"),
    ("entendre", "présent", "participe"): "entendant",
    ("entendre", "passé", "participe"): "entendu",
    ("faire", "présent", "indicatif"):
        ("fais", "fais", "fait", "faisons", "faites", "font"),
    ("faire", "présent", "participe"): "faisant",
    ("faire", "passé", "participe"): "fait",
    ("falloir", "présent", "indicatif"):
        ("", "", "faut", "", "", ""),
    ("falloir", "passé", "participe"): "fallu",
    ("inscrire", "présent", "indicatif"):
        ("inscris", "inscris", "inscrit", "inscrivons", "inscrivez", "inscrivent"),
    ("inscrire", "présent", "participe"): "inscrivant",
    ("inscrire", "passé", "participe"): "inscrit",
    ("joindre", "présent", "indicatif"):
        ("joins", "joins", "joint", "joignons", "joignez", "joignent"),
    ("joindre", "présent", "participe"): "joignant",
    ("joindre", "passé", "participe"): "joint",
    ("lire", "présent", "indicatif"):
        ("lis", "lis", "lit", "lisons", "lisez", "lisent"),
    ("lire", "présent", "participe"): "lisant",
    ("lire", "passé", "participe"): "lu",
    ("mettre", "présent", "indicatif"):
        ("mets", "mets", "met", "mettons", "mettez", "mettent"),
    ("mettre", "présent", "participe"): "mettant",
    ("mettre", "passé", "participe"): "mis",
    ("mourir", "présent", "indicatif"):
        ("meurs", "meurs", "meurt", "mourons", "mourez", "meurent"),
    ("mourir", "présent", "participe"): "mourant",
    ("mourir", "passé", "participe"): "mort",
    ("naître", "présent", "indicatif"):
        ("nais", "nais", "naît", "naissons", "naissez", "naissent"),
    ("naître", "présent", "participe"): "naissant",
    ("naître", "passé", "participe"): "né",
    ("obtenir", "présent", "indicatif"):
        ("obtiens", "obtiens", "obtient", "obtenons", "obtenez", "obtiennent"),
    ("obtenir", "présent", "participe"): "obtenant",
    ("obtenir", "passé", "participe"): "obtenu",
    ("offrir", "présent", "indicatif"):
        ("offre", "offres", "offre", "offrons", "offrez", "offrent"),
    ("offrir", "présent", "participe"): "offrant",
    ("offrir", "passé", "participe"): "offert",
    ("ouvrir", "présent", "indicatif"):
        ("ouvre", "ouvres", "ouvre", "ouvrons", "ouvrez", "ouvrent"),
    ("ouvrir", "présent", "participe"): "ouvrant",
    ("ouvrir", "passé", "participe"): "ouvert",
    ("partir", "présent", "indicatif"):
        ("pars", "pars", "part", "partons", "partez", "partent"),
    ("partir", "présent", "participe"): "partant",
    ("partir", "passé", "participe"): "parti",
    ("peindre", "présent", "indicatif"):
        ("peins", "peins", "peint", "peignons", "peignez", "peignent"),
    ("peindre", "présent", "participe"): "peignant",
    ("peindre", "passé", "participe"): "peint",
    ("pendre", "présent", "indicatif"):
        ("pends", "pends", "pend", "pendons", "pendez", "pendent"),
    ("pendre", "présent", "participe"): "pendant",
    ("pendre", "passé", "participe"): "pendu",
    ("percevoir", "présent", "indicatif"):
        ("perçois", "perçois", "perçoit", "percevons", "percevez", "perçoivent"),
    ("percevoir", "présent", "participe"): "percevant",
    ("percevoir", "passé", "participe"): "perçu",
    ("perdre", "présent", "indicatif"):
        ("perds", "perds", "perd", "perdons", "perdez", "perdent"),
    ("perdre", "présent", "participe"): "perdant",
    ("perdre", "passé", "participe"): "perdu",
    ("permettre", "présent", "indicatif"):
        ("permets", "permets", "permet", "permettons", "permettez", "permettent"),
    ("permettre", "présent", "participe"): "permettant",
    ("permettre", "passé", "participe"): "permis",
    ("pleuvoir", "présent", "indicatif"):
        ("", "", "pleut", "", "", ""),
    ("pleuvoir", "passé", "participe"): "plu",
    ("pourvoir", "présent", "indicatif"):
        ("pourvois", "pourvois", "pourvoit", "pourvoyons", "pourvoyez", "pourvoient"),
    ("pourvoir", "présent", "participe"): "pourvoyant",
    ("pourvoir", "passé", "participe"): "pourvu",
    ("pouvoir", "présent", "indicatif"):
        ("peux", "peux", "peut", "pouvons", "pouvez", "peuvent"),
    ("pouvoir", "présent", "participe"): "pouvant",
    ("pouvoir", "passé", "participe"): "pu",
    ("prendre", "présent", "indicatif"):
        ("prends", "prends", "prend", "prenons", "prenez", "prennet"),
    ("prendre", "présent", "participe"): "prenant",
    ("prendre", "passé", "participe"): "pris",
    ("prescrire", "présent", "indicatif"):
        ("prescris", "prescris", "prescrit", "prescrivons", "prescrivez", "prescrivent"),
    ("prescrire", "présent", "participe"): "prescrivant",
    ("prescrire", "passé", "participe"): "prescrit",
    ("prétendre", "présent", "indicatif"):
        ("prétends", "prétends", "prétend", "prétendons", "prétendez", "prétendent"),
    ("prétendre", "présent", "participe"): "prétendant",
    ("prétendre", "passé", "participe"): "prétendu",
    ("produire", "présent", "indicatif"):
        ("produis", "produis", "produit", "produisons", "produisez", "produisent"),
    ("produire", "présent", "participe"): "produisant",
    ("produire", "passé", "participe"): "produit",
    ("recevoir", "présent", "indicatif"):
        ("reçois", "reçois", "reçoit", "recevons", "recevez", "reçoivent"),
    ("recevoir", "présent", "participe"): "recevant",
    ("recevoir", "passé", "participe"): "reçu",
    ("réduire", "présent", "indicatif"):
        ("réduis", "réduis", "réduit", "réduisons", "réduisez", "réduisent"),
    ("réduire", "présent", "participe"): "réduisant",
    ("réduire", "passé", "participe"): "réduit",
    ("rejoindre", "présent", "indicatif"):
        ("rejoins", "rejoins", "rejoint", "rejoignons", "rejoignez", "rejoignent"),
    ("rejoindre", "présent", "participe"): "rejoignant",
    ("rejoindre", "passé", "participe"): "rejoint",
    ("rendre", "présent", "indicatif"):
        ("rends", "rends", "rend", "rendons", "rendez", "rendent"),
    ("rendre", "présent", "participe"): "rendant",
    ("rendre", "passé", "participe"): "rendu",
    ("résoudre", "présent", "indicatif"):
        ("résous", "résous", "résout", "résolvons", "résolvez", "résolvent"),
    ("résoudre", "présent", "participe"): "résolvant",
    ("résoudre", "passé", "participe"): "résolu",
    ("rire", "présent", "indicatif"):
        ("ris", "ris", "rit", "rions", "riez", "rient"),
    ("rire", "présent", "participe"): "riant",
    ("rire", "passé", "participe"): "ri",
    ("savoir", "présent", "indicatif"):
        ("sais", "sais", "sait", "savons", "savez", "savent"),
    ("savoir", "futur", "indicatif"):
        ("saurai", "sauras", "saura", "saurons", "saurez", "sauront"),
    ("savoir", "présent", "participe"): "sachant",
    ("savoir", "passé", "participe"): "su",
    ("sentir", "présent", "indicatif"):
        ("sens", "sens", "sent", "sentons", "sentez", "sentent"),
    ("sentir", "présent", "participe"): "sentant",
    ("sentir", "passé", "participe"): "senti",
    ("servir", "présent", "indicatif"):
        ("sers", "sers", "sert", "servons", "servez", "servent"),
    ("servir", "présent", "participe"): "servant",
    ("servir", "passé", "participe"): "servi",
    ("sortir", "présent", "indicatif"):
        ("sors", "sors", "sort", "sortons", "sortez", "sortent"),
    ("sortir", "présent", "participe"): "sortant",
    ("sortir", "passé", "participe"): "sorti",
    ("souffrir", "présent", "indicatif"):
        ("souffre", "souffres", "souffre", "souffrons", "souffrez", "souffrent"),
    ("souffrir", "présent", "participe"): "souffrant",
    ("souffrir", "passé", "participe"): "souffert",
    ("suffire", "présent", "indicatif"):
        ("suffis", "suffis", "suffit", "suffisons", "suffisez", "suffisent"),
    ("suffire", "présent", "participe"): "suffisant",
    ("suffire", "passé", "participe"): "suffi",
    ("suivre", "présent", "indicatif"):
        ("suis", "suis", "suit", "suivons", "suivez", "suivent"),
    ("suivre", "présent", "participe"): "suivant",
    ("suivre", "passé", "participe"): "suivi",
    ("tendre", "présent", "indicatif"):
        ("tends", "tends", "tend", "tendons", "tendez", "tendent"),
    ("tendre", "présent", "participe"): "tendant",
    ("tendre", "passé", "participe"): "tendu",
    ("tenir", "présent", "indicatif"):
        ("tiens", "tiens", "tient", "tenons", "tenez", "tiennent"),
    ("tenir", "présent", "participe"): "tenant",
    ("tenir", "passé", "participe"): "tenu",
    ("tondre", "présent", "indicatif"):
        ("tonds", "tonds", "tond", "tondons", "tondez", "tondent"),
    ("tondre", "présent", "participe"): "tondant",
    ("tondre", "passé", "participe"): "tondu",
    ("tordre", "présent", "indicatif"):
        ("tords", "tords", "tord", "tordons", "tordez", "tordent"),
    ("tordre", "présent", "participe"): "tordant",
    ("tordre", "passé", "participe"): "tordu",
    ("traduire", "présent", "indicatif"):
        ("traduis", "traduis", "traduit", "traduisons", "traduisez", "traduisent"),
    ("traduire", "présent", "participe"): "traduisant",
    ("traduire", "passé", "participe"): "traduit",
    ("valoir", "présent", "indicatif"):
        ("vaux", "vaux", "vaut", "valons", "valez", "valent"),
    ("valoir", "présent", "participe"): "valant",
    ("valoir", "passé", "participe"): "valu",
    ("vendre", "présent", "indicatif"):
        ("vends", "vends", "vend", "vendons", "vendez", "vendent"),
    ("vendre", "présent", "participe"): "vendant",
    ("vendre", "passé", "participe"): "vendu",
    ("venir", "présent", "indicatif"):
        ("viens", "viens", "vient", "venons", "venez", "viennent"),
    ("venir", "présent", "participe"): "venant",
    ("venir", "passé", "participe"): "venu",
    ("vivre", "présent", "indicatif"):
        ("vis", "vis", "vit", "vivons", "vivez", "vivent"),
    ("vivre", "présent", "participe"): "vivant",
    ("vivre", "passé", "participe"): "vécu",
    ("voir", "présent", "indicatif"):
        ("vois", "vois", "voit", "voyons", "voyez", "voient"),
    ("voir", "présent", "participe"): "voyant",
    ("voir", "passé", "participe"): "vu",
    ("vouloir", "présent", "indicatif"):
        ("veux", "veux", "veut", "voulons", "voulez", "veulent"),
    ("vouloir", "présent", "participe"): "voulant",
    ("vouloir", "passé", "participe"): "voulu",
}

# 1st group verbs that uses è in futur simple
_VERB_EGRAVE = (
    "acheter",
    "celer",
    "ciseler",
    "démanteler",
    "écarteler",
    "fureter",
    "geler",
    "marteler",
    "modeler",
    "peler"
)

# index map of person to conjug tuple index
# the "person" distinguishes masculin / feminin
# the conjug tuple does not
_PERSON_IDX_MAP = {
    0: 0,
    1: 1,
    2: 2,
    3: 2,
    4: 3,
    5: 4,
    6: 5,
    7: 5
}

_VOWELS = ('a', 'â', 'à', 'e', 'é', 'è', 'i', 'o', 'u')
_DOUBLE_CONSONANTS = ('ch', 'gn',)

TENSES = (
    "présent",
    "passé composé",
    "imparfait",
    "futur",
    "passé simple",
    "plus-que-parfait",
    "passé antérieur",
    "futur antérieur"
)

# 自反代词
PERSONS_PRONOMINAL = ("me", "te", "se", "se", "nous", "vous", "se", "se")
PERSONS = ("je", "tu", "il", "elle", "nous", "vous", "ils", "elles")
MOODS = ("indicatif", "conditionnel", "subjonctif", "impératif")

# map composed tenses
_MAP_COMPOSE = {
    "passé composé": "présent",
    "futur antérieur": "futur",
    "passé antérieur": "passé simple",
}


def conjug(verb, tense, mood, pers_idx):
    """ Generate the conjugason """

    is_gender = _find_gender(verb, tense, mood)
    is_pronominal = _check_pronominal(verb)
    try:
        conjug_tuple = _RULES_AVEC_AUX[(tense, mood)](verb)
    except KeyError:
        if is_pronominal:
            conjug_tuple = _RULES_SANS_AUX[(tense, mood)](_remove_pronominal(verb))
        else:
            conjug_tuple = _RULES_SANS_AUX[(tense, mood)](verb)
    base = conjug_tuple[_PERSON_IDX_MAP[pers_idx]]
    if is_pronominal:
        if pers_idx not in (4, 5) and _check_apostrophe(base):
            answer = PERSONS[pers_idx] + " " + \
                     PERSONS_PRONOMINAL[pers_idx][:-1] + "'" + base
        else:
            answer = ' '.join([PERSONS[pers_idx], PERSONS_PRONOMINAL[pers_idx],
                               base])
    else:
        if pers_idx == 0 and _check_apostrophe(base):
            answer = "'".join(["j", base])
        else:
            answer = ' '.join([PERSONS[pers_idx], base])
    if is_gender:
        if pers_idx in (0, 1):
            answer += '(e)'
        elif pers_idx == 3:
            answer += 'e'
        elif pers_idx in (4, 5):
            if answer[-1] == 's':  # already ends with "s"
                answer += '(es)'
            else:
                answer += '(e)s'
        elif pers_idx == 6 and answer[-1] != 's':
            answer += 's'
        elif pers_idx == 7:
            answer += 'es'
        else:
            pass
    return answer


def _find_gender(infinitive, tense, mood):
    """ Determine if gender & number needs to be considerer in the participle """

    if tense == 'passé composé' and mood == 'indicatif':
        return infinitive in _AUX_ETRE_VERBS or _check_pronominal(infinitive)
    else:
        return False


def _find_group(infinitive):
    """ Find the conjugation group of the infinitive
    Our assumption is all irregular verbs will be in our dictionary.
    """
    if (infinitive, 'présent', 'indicatif') in _VERBS_IRREG:
        return 3
    elif infinitive.endswith('er'):
        return 1
    elif infinitive.endswith('ir'):
        return 2
    else:
        raise KeyError('Verb seems to be irregular but it is not in the dictionary')


def _check_pronominal(infinitive):
    """ check if the infinitive is pronominal verb """
    return infinitive.split()[0] == 'se' or infinitive.split("'")[0] == "s"


def _remove_pronominal(verb):
    """ Remove the pronominal prefix in a verb """
    if verb.split()[0] == 'se':
        infinitive = verb.split()[1]
    elif verb.split("'")[0] == "s":
        infinitive = verb.split("'")[1]
    else:
        infinitive = verb
    return infinitive


def _check_apostrophe(verb):
    """ Check if the verb starts with a vowel and therefore needs apostrophe """
    return verb[0] in _VOWELS or (verb[0] == 'h' and verb[1] in _VOWELS)


def _rule_present_indicatif(infinitive):
    """ Conjugation rule for present, indicatif """
    group = _find_group(infinitive)
    if group == 1:
        conjug_tuple = _rule_present_indicatif_1st(infinitive)
    elif group == 2:
        conjug_tuple = _rule_present_indicatif_2nd(infinitive)
    else:
        conjug_tuple = _VERBS_IRREG[(infinitive, 'présent', 'indicatif')]
    return conjug_tuple


def _rule_present_indicatif_1st(infinitive):
    """ Conjugation rule of 1st group regular verb, present, indicatif """
    root = infinitive[:-2]
    # check if the root has ending e + consonnant
    if root[-2] in ('é', 'e') or \
            (root[-3] in ('é', 'e') and root[-3:] in _DOUBLE_CONSONANTS):
        n_cons = 1 if root[-2] in ('é', 'e') else 2
        if n_cons == 1 and root[-1] in ('l', 't') and infinitive not in _VERB_EGRAVE:  # double ll or tt
            new_root = root + root[-1]
        else:  # use è
            new_root = ''.join([root[:-1 - n_cons], 'è', root[-n_cons:]])
        p1 = new_root + 'e'
        p2 = new_root + 'es'
        p3 = new_root + 'e'
        # check if the word ends with "ger"
        if root[-1] != 'g':
            p4 = root + 'ons'
        else:
            p4 = root + 'eons'
        p5 = root + 'ez'
        p6 = new_root + 'ent'
    else:
        p1 = root + 'e'
        p2 = root + 'es'
        p3 = root + 'e'
        # check if the word ends with "ger"
        if root[-1] != 'g':
            p4 = root + 'ons'
        else:
            p4 = root + 'eons'
        p5 = root + 'ez'
        p6 = root + 'ent'
    return p1, p2, p3, p4, p5, p6


def _rule_present_indicatif_2nd(infinitive):
    """ Conjugation rule of 2nd group regular verb, present, indicatif """
    root = _remove_pronominal(infinitive[:-2])
    p1 = root + 'is'
    p2 = root + 'is'
    p3 = root + 'it'
    p4 = root + 'issons'
    p5 = root + 'issez'
    p6 = root + 'issent'
    return p1, p2, p3, p4, p5, p6


def _rule_passe_compose(verb):
    """ Conjugation rule of 1st group regular verb, passé composé, indicatif """
    infinitive = _remove_pronominal(verb)
    if infinitive in _AUX_ETRE_VERBS or _check_pronominal(verb):
        aux = _VERBS_IRREG[('être', 'présent', 'indicatif')]
    else:
        aux = _VERBS_IRREG[('avoir', 'présent', 'indicatif')]
    part = _participe(infinitive, "passé")
    return tuple(' '.join([x, part]) for x in aux)


def _rule_imparfait_indicatif(infinitive):
    """ Conjugation rule for imparfait, indicatif
    Rule:
        1. take conjug of present, indicatif, nous
        2. remove "ons"
        3. add suffixes
    """
    root = _rule_present_indicatif(infinitive)[3]
    p1 = root[:-3] + 'ais'
    p2 = root[:-3] + 'ais'
    p3 = root[:-3] + 'ait'
    if root[-5:-3] == 'ge':  # treat "geons" case
        p4 = root[:-4] + 'ions'
        p5 = root[:-4] + 'iez'
    else:
        p4 = root[:-3] + 'ions'
        p5 = root[:-3] + 'iez'
    p6 = root[:-3] + 'aient'
    return p1, p2, p3, p4, p5, p6


def _rule_futur_indicatif(infinitive):
    """ Conjugation rule for imparfait, indicatif
    Rule:
        1. take conjug of present, indicatif, vous
        2. remove "ez" or "issez"
        3. add suffixes -rai, -ras, -ra, -rons, -rez, -ront
    """
    base = _rule_present_indicatif(infinitive)[4]
    group = _find_group(infinitive)
    if group == 3:
        try:
            p1, p2, p3, p4, p5, p6 = _VERBS_IRREG[(infinitive, 'futur', 'indicatif')]
        except KeyError:
            if infinitive.endswith('re'):  # drop e and add suffix
                p1 = infinitive[:-1] + 'ai'
                p2 = infinitive[:-1] + 'as'
                p3 = infinitive[:-1] + 'a'
                p4 = infinitive[:-1] + 'ons'
                p5 = infinitive[:-1] + 'ez'
                p6 = infinitive[:-1] + 'ont'
            elif infinitive.endswith('ir'):  # drop i and add suffix with double r
                p1 = infinitive[:-1] + 'rai'
                p2 = infinitive[:-1] + 'ras'
                p3 = infinitive[:-1] + 'ra'
                p4 = infinitive[:-1] + 'rons'
                p5 = infinitive[:-1] + 'rez'
                p6 = infinitive[:-1] + 'ront'
            else:
                raise KeyError('Verb seems to be irregular but it is not in the dictionary')
    else:
        if group == 1:
            # treat exceptions
            if infinitive.endswith('yer'):
                root = base[:-3] + 'ie'
            elif infinitive.endswith('eter') or infinitive.endswith('eler'):
                if infinitive in _VERB_EGRAVE:  # uses è
                    root = base[:-4] + 'è' + base[-3] + 'e'
                else:  # double t or l
                    root = base[:-2] + base[-3] + 'e'
            else:
                root = base[:-1]
        else:
            root = base[:-4]
        p1 = root + 'rai'
        p2 = root + 'ras'
        p3 = root + 'ra'
        p4 = root + 'rons'
        p5 = root + 'rez'
        p6 = root + 'ront'
    return p1, p2, p3, p4, p5, p6


def _participe(infinitive, tense):
    try:
        part = _VERBS_IRREG[(infinitive, tense, 'participe')]
    except KeyError:
        if infinitive.endswith('er'):
            if tense == 'passé':
                part = infinitive[:-2] + 'é'
            elif tense == 'présent':
                part = infinitive[:-2] + 'ant'
            else:
                raise ValueError('Invalid tense')
        elif infinitive.endswith('ir'):
            if tense == 'passé':
                part = infinitive[:-1]
            elif tense == 'présent':
                part = infinitive[:-1] + 'ssant'
            else:
                raise ValueError('Invalid tense')
        else:
            raise KeyError('Verb seems to be irregular but it is not in the dictionary')
    return part


# map verb conjugaison rules, rules without aux verb
_RULES_SANS_AUX = {
    ('présent', 'indicatif'): _rule_present_indicatif,
    ('imparfait', 'indicatif'): _rule_imparfait_indicatif,
    ('futur', 'indicatif'): _rule_futur_indicatif,
}

# map verb conjugaison rules, rules with aux verb
_RULES_AVEC_AUX = {
    ('passé composé', 'indicatif'): _rule_passe_compose,
}
