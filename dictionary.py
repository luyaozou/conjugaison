#! encoding = utf-8

""" Conjugation rules and irregular verb dictionary """

_VOWELS = ('a', 'â', 'à', 'e', 'é', 'è', 'i', 'o', 'u')
_DOUBLE_CONSONANTS = ('ch', 'gn',)

# tense & moods currently available in the dictionray
AVAILABLE_TENSE_MOODS = (0, 1, 2, 3, 8, 15)

TENSE_MOODS = (
    ("présent", "indicatif"),
    ("passé composé", "indicatif"),
    ("imparfait", "indicatif"),
    ("futur", "indicatif"),
    ("passé simple", "indicatif"),
    ("plus-que-parfait", "indicatif"),
    ("passé antérieur", "indicatif"),
    ("futur antérieur", "indicatif"),
    ("présent", "conditionnel"),
    ("passé", "conditionnel"),
    ("passé - forme alternative", "conditionnel"),
    ("présent", "subjonctif"),
    ("imparfait", "subjonctif"),
    ("plus-que-parfait", "subjonctif"),
    ("passé", "subjonctif"),
    ("présent", "impératif"),
)

# 自反代词
PERSONS_PRONOMINAL = ("me", "te", "se", "se", "nous", "vous", "se", "se")
PERSONS = ("je", "tu", "il", "elle", "nous", "vous", "ils", "elles")
PERSONS_TONIQUE = ("moi", "toi", "", "", "nous", "vous", "", "")

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

# suffixes in general
_SUFFIX = {
    ("présent_1", "indicatif"): ("e", "es", "e", "ons", "ez", "ent"),
    ("présent_2", "indicatif"): ("is", "is", "it", "issons", "issez", "issent"),
    ("imparfait", "indicatif"): ("ais", "ais", "ait", "ions", "iez", "aient"),
    ("futur", "indicatif"): ("rai", "ras", "ra", "rons", "rez", "ront"),
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
    ("être", "futur", "indicatif"): "se",
    ("être", "imparfait", "indicatif"): "ét",
    ("être", "présent", "impératif"):
        ("", "sois", "", "soyons", "soyez", ""),
    ("être", "présent", "participe"): "étant",
    ("être", "passé", "participe"): "été",
    ("avoir", "présent", "indicatif"):
        ("ai", "as", "a", "avons", "avez", "ont"),
    ("avoir", "passé simple", "indicatif"):
        ("'eus", "eus", "eut", "eûmes", "eûtes", "eurent"),
    ("avoir", "présent", "impératif"):
        ("", "aie", "", "ayons", "ayez", ""),
    ("avoir", "futur", "indicatif"): "au",
    ("avoir", "présent", "participe"): "ayant",
    ("avoir", "passé", "participe"): "eu",
    ("aller", "présent", "indicatif"):
        ("vais", "vas", "va", "allons", "allez", "vont"),
    ("aller", "futur", "indicatif"): "i",
    ("aller", "présent", "participe"): "allant",
    ("aller", "passé", "participe"): "allé",
    ("appuyer", "présent", "indicatif"):
        ("appuie", "appuies", "appuie", "appuyons", "appuyez", "appuient"),
    ("apercevoir", "présent", "indicatif"):
        ("aperçois", "aperçois", "aperçoit", "apercevons", "apercevez", "aperçoivent"),
    ("apercevoir", "futur", "indicatif"): "apercev",
    ("apercevoir", "présent", "participe"): "apercevant",
    ("apercevoir", "passé", "participe"): "aperçu",
    ("apprendre", "présent", "indicatif"):
        ("apprends", "apprends", "apprend", "apprenons", "apprenez", "apprennent"),
    ("apprendre", "présent", "participe"): "apprenant",
    ("apprendre", "passé", "participe"): "appris",
    ("asseoir", "présent", "indicatif"):
        ("assieds", "assieds", "assied", "asseyons", "asseyez", "asseyent"),
    ("asseoir", "futur", "indicatif"): "asseye",
    ("asseoir", "présent", "participe"): "asseyant",
    ("asseoir", "passé", "participe"): "assis",
    ("atteindre", "présent", "indicatif"):
        ("atteins", "atteins", "atteint", "atteignons", "atteignez", "atteignent"),
    ("atteindre", "présent", "participe"): "atteignant",
    ("atteindre", "passé", "participe"): "atteint",
    ("attendre", "présent", "indicatif"):
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
        ("connais", "connais", "connaît", "connaissons", "connaissez", "connaissent"),
    ("connaître", "présent", "participe"): "connaissant",
    ("connaître", "passé", "participe"): "connu",
    ("courir", "présent", "indicatif"):
        ("cours", "cours", "court", "courons", "courez", "courent"),
    ("courir", "futur", "indicatif"): "cour",
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
    ("cueillir", "futur", "indicatif"): "cueille",
    ("cueillir", "présent", "participe"): "cueillant",
    ("cueillir", "passé", "participe"): "cueilli",
    ("cuire", "présent", "indicatif"):
        ("cuis", "cuis", "cuit", "cuisons", "cuisez", "cuisent"),
    ("cuire", "présent", "participe"): "cuisant",
    ("cuire", "passé", "participe"): "cuit",
    ("décevoir", "présent", "indicatif"):
        ("déçois", "déçois", "déçoit", "décevons", "décevez", "déçoivent"),
    ("décevoir", "futur", "indicatif"): "décev",
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
        ("deviens", "deviens", "devient", "devenons", "devenez", "deviennent"),
    ("devenir", "futur", "indicatif"): "deviend",
    ("devenir", "présent", "participe"): "devenant",
    ("devenir", "passé", "participe"): "devenu",
    ("devoir", "présent", "indicatif"):
        ("dois", "dois", "doit", "devons", "devez", "doivent"),
    ("devoir", "futur", 'indicatif'): "dev",
    ("devoir", "présent", "participe"): "devant",
    ("devoir", "passé", "participe"): "dû",
    ("dire", "présent", "indicatif"):
        ("dis", "dis", "dit", "disons", "dites", "disent"),
    ("dire", "présent", "participe"): "disant",
    ("dire", "passé", "participe"): "dit",
    ("disparaître", "présent", "indicatif"):
        ("disparais", "disparais", "disparaît", "disparaissons", "disparaissez", "disparaissent"),
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
    ("faire", "futur", "indicatif"): "fe",
    ("faire", "présent", "participe"): "faisant",
    ("faire", "passé", "participe"): "fait",
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
    ("mourir", "futur", "indicatif"): "mour",
    ("mourir", "présent", "participe"): "mourant",
    ("mourir", "passé", "participe"): "mort",
    ("naître", "présent", "indicatif"):
        ("nais", "nais", "naît", "naissons", "naissez", "naissent"),
    ("naître", "présent", "participe"): "naissant",
    ("naître", "passé", "participe"): "né",
    ("obtenir", "présent", "indicatif"):
        ("obtiens", "obtiens", "obtient", "obtenons", "obtenez", "obtiennent"),
    ("obtenir", "futur", "indicatif"): "obtiend",
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
    ("percevoir", "futur", "indicatif"): "percev",
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
    ("pourvoir", "présent", "indicatif"):
        ("pourvois", "pourvois", "pourvoit", "pourvoyons", "pourvoyez", "pourvoient"),
    ("pouvoir", "futur", "indicatif"): "pour",
    ("pourvoir", "présent", "participe"): "pourvoyant",
    ("pourvoir", "passé", "participe"): "pourvu",
    ("pouvoir", "présent", "indicatif"):
        ("peux", "peux", "peut", "pouvons", "pouvez", "peuvent"),
    ("pouvoir", "présent", "impératif"): ("", "", "", "", "", ""),
    ("pouvoir", "présent", "participe"): "pouvant",
    ("pouvoir", "passé", "participe"): "pu",
    ("prendre", "présent", "indicatif"):
        ("prends", "prends", "prend", "prenons", "prenez", "prennent"),
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
    ("recevoir", "futur", "indicatif"): "recev",
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
    ("savoir", "futur", "indicatif"): "sau",
    ("savoir", "présent", "impératif"):
        ("", "sache", "", "sachons", "sachez", ""),
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
    ("soutenir", "présent", "indicatif"):
        ("soutiens", "soutiens", "soutient", "soutenons", "soutenez", "soutiennent"),
    ("soutenir", "futur", "indicatif"): "soutiend",
    ("soutenir", "présent", "participe"): "soutenant",
    ("soutenir", "passé", "participe"): "soutenu",
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
    ("tenir", "futur", "indicatif"): "tiend",
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
    ("valoir", "futur", "indicatif"): "vaud",
    ("valoir", "présent", "participe"): "valant",
    ("valoir", "passé", "participe"): "valu",
    ("vendre", "présent", "indicatif"):
        ("vends", "vends", "vend", "vendons", "vendez", "vendent"),
    ("vendre", "présent", "participe"): "vendant",
    ("vendre", "passé", "participe"): "vendu",
    ("venir", "présent", "indicatif"):
        ("viens", "viens", "vient", "venons", "venez", "viennent"),
    ("venir", "futur", "indicatif"): "viend",
    ("venir", "présent", "participe"): "venant",
    ("venir", "passé", "participe"): "venu",
    ("vivre", "présent", "indicatif"):
        ("vis", "vis", "vit", "vivons", "vivez", "vivent"),
    ("vivre", "présent", "participe"): "vivant",
    ("vivre", "passé", "participe"): "vécu",
    ("voir", "présent", "indicatif"):
        ("vois", "vois", "voit", "voyons", "voyez", "voient"),
    ("voir", "futur", "indicatif"): "ver",
    ("voir", "présent", "participe"): "voyant",
    ("voir", "passé", "participe"): "vu",
    ("vouloir", "présent", "indicatif"):
        ("veux", "veux", "veut", "voulons", "voulez", "veulent"),
    ("vouloir", "présent", "impératif"):
        ("", "veuille", "", "veuillons", "veuillez", ""),
    ("vouloir", "futur", "indicatif"): "voud",
    ("vouloir", "présent", "participe"): "voulant",
    ("vouloir", "passé", "participe"): "voulu",
}

_VERBS_4GP = {
    ("falloir", "présent", "indicatif"):
        ("", "", "faut", "", "", ""),
    ("falloir", "présent", "impératif"): ("", "", "", "", "", ""),
    ("falloir", "imparfait", "indicatif"): "fall",
    ("falloir", "futur", "indicatif"): "faud",
    ("falloir", "passé", "participe"): "fallu",
    ("frire", "présent", "indicatif"): ("fris", "fris", "frit", "", "", ""),
    ("frire", "imparfait", "indicatif"): "",
    ("frire", "futur", "indicatif"): "fri",
    ("frire", "passé", "participe"): "frit",
    ("pleuvoir", "présent", "indicatif"):
        ("", "", "pleut", "", "", ""),
    ("pleuvoir", "présent", "impératif"): ("", "", "", "", "", ""),
    ("pleuvoir", "imparfait", "indicatif"): "pleuv",
    ("pleuvoir", "futur", "indicatif"): "pleuv",
    ("pleuvoir", "passé", "participe"): "plu",
}


def conjug_all(verb, tense, mood):
    """ Generate the conjugaison for all persons
    :argument
        verb: str           verb infinitive to conjugate
        tense: str          tense in TENSES
        mood: str           mood in MOODS
    :returns
        t_answer: tuple of str
            conjugated verb strings with all persons
    """

    is_gender = _find_gender(verb, tense, mood)
    is_pronominal = _check_pronominal(verb)
    infinitive = _remove_pronominal(verb)
    group = _find_group(infinitive)
    t_answer = []
    if mood == 'impératif':
        # treat impératif alone because it always has only 3 conjugs
        conjug_tuple = _RULES_SANS_AUX[('présent', 'impératif')](infinitive, group)
        for pidx in range(8):
            pers_idx = _PERSON_IDX_MAP[pidx]
            base = conjug_tuple[pers_idx]
            if pers_idx in (1, 3, 4):
                if base and is_pronominal:
                    t_answer.append('-'.join([base, PERSONS_TONIQUE[pidx]]))
                else:
                    t_answer.append(base)
            else:
                t_answer.append("")
    else:
        try:
            conjug_tuple = _RULES_AVEC_AUX[(tense, mood)](verb, group)
        except KeyError:
            if is_pronominal:
                conjug_tuple = _RULES_SANS_AUX[(tense, mood)](infinitive, group)
            else:
                conjug_tuple = _RULES_SANS_AUX[(tense, mood)](verb, group)
        if group == 4:  # special verbs, do not have all conjugaison
            present_tuple = _RULES_SANS_AUX[('présent', 'indicatif')](verb, 4)
            for i, (_p, _c) in enumerate(zip(present_tuple, conjug_tuple)):
                if _c and _p and i < 3:
                    if i == 0 and _check_apostrophe(_c):
                        t_answer.append("j'" + _c)
                    else:
                        t_answer.append(' '.join([PERSONS[i], _c]))
                else:
                    t_answer.append("")
            t_answer.append("")
            t_answer.append("")
        else:
            for pidx in range(8):
                base = conjug_tuple[_PERSON_IDX_MAP[pidx]]
                if not base:  # if this conjugation does not exist and therefore is empty
                    answer = ""
                else:
                    if is_pronominal:
                        if pidx not in (4, 5) and _check_apostrophe(base):
                            answer = PERSONS[pidx] + " " + \
                                     PERSONS_PRONOMINAL[pidx][:-1] + "'" + base
                        else:
                            answer = ' '.join([PERSONS[pidx], PERSONS_PRONOMINAL[pidx],
                                               base])
                    else:
                        if pidx == 0 and _check_apostrophe(base):
                            answer = "'".join(["j", base])
                        else:
                            answer = ' '.join([PERSONS[pidx], base])
                    if is_gender:
                        if pidx in (0, 1):
                            answer += '(e)'
                        elif pidx == 3:
                            answer += 'e'
                        elif pidx in (4, 5):
                            if answer[-1] == 's':  # already ends with "s"
                                answer += '(es)'
                            else:
                                answer += '(e)s'
                        elif pidx == 6 and answer[-1] != 's':
                            answer += 's'
                        elif pidx == 7:
                            answer += 'es'
                        else:
                            pass
                t_answer.append(answer)
    return tuple(t_answer)


def conjug(verb, tense, mood, pers_idx):
    """ Generate the conjugaison
    :argument
        verb: str           verb infinitive to conjugate
        tense: str          tense in TENSES
        mood: str           mood in MOODS
        pers_idx: int       person index 0-7, correspond to PERSONS
    :returns
        answer: str         conjugated verb string with person
    """

    is_gender = _find_gender(verb, tense, mood)
    is_pronominal = _check_pronominal(verb)
    infinitive = _remove_pronominal(verb)
    group = _find_group(infinitive)
    if mood == 'impératif':
        answer = _RULES_SANS_AUX[('présent', 'impératif')](infinitive, group, _PERSON_IDX_MAP[pers_idx])
        if bool(answer) and is_pronominal:
            answer += '-' + PERSONS_TONIQUE[pers_idx]
    elif group == 4:  # special verbs, do not have all conjugaison
        if pers_idx < 3:
            if _RULES_SANS_AUX[('présent', 'indicatif')](verb, 4, pers_idx):
                try:
                    base = _RULES_AVEC_AUX[(tense, mood)](verb, 4, pers_idx)
                except KeyError:
                    base = _RULES_SANS_AUX[(tense, mood)](verb, 4, pers_idx)
                if base:
                    if pers_idx == 0 and _check_apostrophe(base):
                        answer = "'".join(["j", base])
                    else:
                        answer = ' '.join([PERSONS[pers_idx], base])
                else:
                    answer = ""
            else:
                answer = ""
        else:
            answer = ""
    else:
        try:
            base = _RULES_AVEC_AUX[(tense, mood)](verb, group, _PERSON_IDX_MAP[pers_idx])
        except KeyError:
            if is_pronominal:
                base = _RULES_SANS_AUX[(tense, mood)](infinitive, group, _PERSON_IDX_MAP[pers_idx])
            else:
                base = _RULES_SANS_AUX[(tense, mood)](verb, group, _PERSON_IDX_MAP[pers_idx])
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
    elif (infinitive, 'présent', 'indicatif') in _VERBS_4GP:
        return 4
    elif infinitive.endswith('er'):
        return 1
    elif infinitive.endswith('ir'):
        return 2
    else:
        err_str = 'Verb "{:s}" seems to be irregular but it is not in the dictionary'.format(infinitive)
        raise KeyError(err_str)


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


def _rule_present_indicatif(infinitive, group, pidx=-1):
    """ Conjugation rule for present, indicatif
    :returns
        str or tuple of str
    """
    if group == 1:  # 1st group verb
        ans = _rule_present_indicatif_1st(infinitive, pidx)
    elif group == 2:  # 2nd group verb
        root = _remove_pronominal(infinitive[:-2])
        if pidx < 0:
            ans = tuple(root + suffix for suffix in _SUFFIX[("présent_2", "indicatif")])
        else:
            ans = root + _SUFFIX[("présent_2", "indicatif")][pidx]
    elif group == 3:  # irregular verb
        if pidx < 0:
            ans = _VERBS_IRREG[(infinitive, 'présent', 'indicatif')]
        else:
            ans = _VERBS_IRREG[(infinitive, 'présent', 'indicatif')][pidx]
    else:
        if pidx < 0:
            ans = _VERBS_4GP[(infinitive, 'présent', 'indicatif')]
        else:
            ans = _VERBS_4GP[(infinitive, 'présent', 'indicatif')][pidx]
    return ans


def _rule_present_indicatif_1st(infinitive, pidx=-1):
    """ Conjugation rule of 1st group regular verb, present, indicatif
    General rule: remove "er"
    Special treatement on
        ~ger: extra "e" in nous ~geons
        e?er: e -> è for persons 1,2,3,6

    :argument
        infinitive: str         verb infinitive
        pidx: int               -1~5 personal index
            if pidx < 0, return all 6 conjugs
            if pidx > 0, return only 1 conjug of that person
    :returns
        str or tuple of str
    """
    root = infinitive[:-2]
    # check if the root has ending e + consonnant
    if root[-2] in ('é', 'e') or \
            (root[-3] in ('é', 'e') and root[-3:] in _DOUBLE_CONSONANTS):
        n_cons = 1 if root[-2] in ('é', 'e') else 2
        if n_cons == 1 and root[-1] in ('l', 't') and infinitive not in _VERB_EGRAVE:
            # double ll or tt
            new_root = root + root[-1]
        else:  # use è
            new_root = ''.join([root[:-1 - n_cons], 'è', root[-n_cons:]])
        if pidx < 0:  # return all persons
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
            return p1, p2, p3, p4, p5, p6
        else:
            if pidx == 3:
                if root[-1] == 'g':
                    return root + 'eons'
                else:
                    return root + 'ons'
            elif pidx == 4:
                return root + 'ez'
            else:
                return new_root + _SUFFIX[("présent_1", "indicatif")][pidx]
    else:
        if pidx < 0:  # return all persons
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
        else:
            if pidx == 3 and root[-1] == 'g':
                return root + 'eons'
            else:
                return root + _SUFFIX[("présent_1", "indicatif")][pidx]


def _rule_passe_compose(verb, group, pidx=-1):
    """ Conjugation rule of passé composé, indicatif
    :argument
        infinitive: str         verb infinitive
        pidx: int               -1~5 personal index
            if pidx < 0, return all 6 conjugs
            if pidx > 0, return only 1 conjug of that person
    :returns
        conjug: str or tuple of 6 str
    """
    infinitive = _remove_pronominal(verb)
    if infinitive in _AUX_ETRE_VERBS or _check_pronominal(verb):
        aux = _VERBS_IRREG[('être', 'présent', 'indicatif')]
    else:
        aux = _VERBS_IRREG[('avoir', 'présent', 'indicatif')]
    part = _participe(infinitive, group, "passé")
    if pidx < 0:
        return tuple(' '.join([x, part]) for x in aux)
    else:
        return ' '.join([aux[pidx], part])


def _rule_imparfait_indicatif(infinitive, group, pidx=-1):
    """ Conjugation rule for imparfait, indicatif
    :argument
        infinitive: str         verb infinitive
        pidx: int               -1~5 personal index
            if pidx < 0, return all 6 conjugs
            if pidx > 0, return only 1 conjug of that person
    :returns
        conjug: str or tuple of 6 str
    """
    root = _root_imparfait_indicatif(infinitive, group)
    if group == 1 and root[-2:] == 'ge':  # remove extra "e" in "gions" "giez case
        new_root = (root, root, root, root[:-1], root[:-1], root)
        if pidx < 0:
            return tuple(_r + _s for _r, _s in zip(new_root, _SUFFIX[("imparfait", "indicatif")]))
        else:
            return new_root[pidx] + _SUFFIX[("imparfait", "indicatif")][pidx]
    elif group == 4:
        if pidx < 0:
            if root:
                return tuple(root + _s for _s in _SUFFIX[("imparfait", "indicatif")])
            else:
                return ("",) * 6
        else:
            return root + _SUFFIX[("imparfait", "indicatif")][pidx] if root else ""
    else:
        if pidx < 0:
            return tuple(root + _s for _s in _SUFFIX[("imparfait", "indicatif")])
        else:
            return root + _SUFFIX[("imparfait", "indicatif")][pidx]


def _root_imparfait_indicatif(infinitive, group):
    """ Find root of imparfait, indicatif:
        present conjug. nous, chop ~ons
    """
    try:
        if group == 4:
            root = _VERBS_4GP[(infinitive, 'imparfait', 'indicatif')]
        else:
            root = _VERBS_IRREG[(infinitive, 'imparfait', 'indicatif')]
    except KeyError:
        # present conjug nous, chop ~ons
        root = _rule_present_indicatif(infinitive, group)[3][:-3]
    return root


def _rule_futur_indicatif(infinitive, group, pidx=-1):
    """ Conjugation rule for imparfait, indicatif
    :argument
        infinitive: str         verb infinitive
        pidx: int               -1~5 personal index
            if pidx < 0, return all 6 conjugs
            if pidx > 0, return only 1 conjug of that person
    :returns
        conjug: str or tuple of 6 str
    """
    root = _root_futur_indicatif(infinitive, group)
    if pidx < 0:
        return tuple(root + _s for _s in _SUFFIX[("futur", "indicatif")])
    else:
        return root + _SUFFIX[("futur", "indicatif")][pidx]


def _root_futur_indicatif(infinitive, group):
    """ Find root for futur, indicatif
    Rule for regular:
        1. take conjug of present, indicatif, vous
        2. remove "ez" or "issez"
        3. add suffixes -rai, -ras, -ra, -rons, -rez, -ront
    """
    try:
        if group == 4:
            root = _VERBS_4GP[(infinitive, 'futur', 'indicatif')]
        else:
            root = _VERBS_IRREG[(infinitive, 'futur', 'indicatif')]
    except KeyError:
        base = _rule_present_indicatif(infinitive, group, pidx=4)
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
        elif infinitive.endswith('re'):  # drop e and add suffix
            root = infinitive[:-2]
        elif infinitive.endswith('ir'):
            root = infinitive[:-1]
        else:
            root = base[:-4]
    return root


def _rule_present_conditionnel(infinitive, group, pidx=-1):
    """ Conjugation rule for présent, conditionnel
    The rule: take the root of futur, indicatif,
              and concat with the suffix of imparfait, indicatif
    :argument
        infinitive: str         verb infinitive
        pidx: int               -1~5 personal index
            if pidx < 0, return all 6 conjugs
            if pidx > 0, return only 1 conjug of that person
    :returns
        conjug: str or tuple of 6 str
    """

    # note that in my root of futur, I dont put the ending 'r'
    # so we need to add it back here
    root = _root_futur_indicatif(infinitive, group) + 'r'
    if pidx < 0:
        return tuple(root + _s for _s in _SUFFIX[("imparfait", "indicatif")])
    else:
        return root + _SUFFIX[("imparfait", "indicatif")][pidx]


def _rule_present_imperatif(infinitive, group, pidx=-1):
    """ Conjugation rule for présent, conditionnel
    The rules:
        1. take tu, nous, vous, remove the person
        2. if 1st group, remove ending 's' in tu
        3. if pronominal verb, add -toi, -nous, -vous after the verb
        4. special case: être, avoir, savoir, vouloir
    :argument
        infinitive: str         verb infinitive
        pidx: int               -1~5 personal index
            if pidx < 0, return all 6 conjugs
            if pidx > 0, return only 1 conjug of that person
    :returns
        conjug: str or tuple of 6 str
    """
    if pidx < 0:
        if group == 3:
            try:
                conjug_tuple = _VERBS_IRREG[(infinitive, "présent", "impératif")]
            except KeyError:
                conjug_tuple = _rule_present_indicatif(infinitive, group, pidx)
        elif group == 4:
            try:
                conjug_tuple = _VERBS_4GP[(infinitive, "présent", "impératif")]
            except KeyError:
                conjug_tuple = _rule_present_indicatif(infinitive, group, pidx)
        else:
            conjug_tuple = _rule_present_indicatif(infinitive, group, pidx)
        if conjug_tuple[1].endswith('es') or conjug_tuple[1].endswith('as'):
            return "", conjug_tuple[1][:-1], "", conjug_tuple[3], conjug_tuple[4], ""
        else:
            return "", conjug_tuple[1], "", conjug_tuple[3], conjug_tuple[4], ""
    else:
        if (infinitive, "présent", "impératif") in _VERBS_IRREG:
            answer = _VERBS_IRREG[(infinitive, "présent", "impératif")][pidx]
        elif (infinitive, "présent", "impératif") in _VERBS_4GP:
            answer = _VERBS_4GP[(infinitive, "présent", "impératif")][pidx]
        else:
            if pidx in (1, 3, 4):
                answer = _rule_present_indicatif(infinitive, group, pidx)
                if pidx == 1 and (answer.endswith('es') or answer.endswith('as')):
                    answer = answer[:-1]
            else:
                answer = ""
        return answer


def _participe(infinitive, group, tense):
    try:
        if group == 4:
            part = _VERBS_4GP[(infinitive, tense, 'participe')]
        else:
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
            err_str = 'Verb "{:s}" seems to be irregular but it is not in the dictionary'.format(infinitive)
            raise KeyError(err_str)
    return part


# map verb conjugaison rules, rules without aux verb
_RULES_SANS_AUX = {
    ('présent', 'indicatif'): _rule_present_indicatif,
    ('imparfait', 'indicatif'): _rule_imparfait_indicatif,
    ('futur', 'indicatif'): _rule_futur_indicatif,
    ('présent', 'conditionnel'): _rule_present_conditionnel,
    ('présent', 'impératif'): _rule_present_imperatif,
}

# map verb conjugaison rules, rules with aux verb
_RULES_AVEC_AUX = {
    ('passé composé', 'indicatif'): _rule_passe_compose,
}
