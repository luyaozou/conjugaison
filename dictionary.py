from collections import namedtuple

_Conjug = namedtuple("Conjug", "tense, mood, je, tu, il, nous, vous, ils")

# verbs that conjugate with etre on passé composé, passé antérieur, et futur antérieur
_ETRE_VERBS = (
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
    "arriver"
)

TENSES = (
    "présent",
    # "passé simple",
    "passé composé",
    # "imparfait",
    # "futur",
)

PERSONS = ("je", "tu", "il/elle/on", "nous", "vous", "ils/elles")
MOODS = ("indicatif", ) #"conditionnel", "subjonctif", "impératif")

# map composed tenses
_MAP_COMPOSE = {
    "passé composé": "présent",
    "futur antérieur": "futur",
    "passé antérieur": "passé simple",
}


def conjug(verb, tense, mood, pers_idx):
    """ Generate the conjugason """

    if isinstance(pers_idx, type(None)):
        # return conjugasons of all persons
        conjug_list = []
        if tense in _MAP_COMPOSE.keys():
            if verb in _ETRE_VERBS:
                assist_tuple = find_conjug_tuple("être", _MAP_COMPOSE[tense], mood)
            else:
                assist_tuple = find_conjug_tuple("avoir", _MAP_COMPOSE[tense], mood)
            conjug_tuple = find_conjug_tuple(verb, _MAP_COMPOSE[tense], mood)
            for pers_idx in range(6):
                assist_base = assist_tuple[pers_idx + 2]
                conjug_base = conjug_tuple[pers_idx + 2]
                if conjug_base:
                    # make sure there is conjugaison for this person
                    if pers_idx == 0 and assist_base.startswith("'"):
                        answer = "j{:s} {:s}(e)".format(assist_base, _participe(verb, 1))
                    elif pers_idx < 3:
                        answer = "{:s} {:s} {:s}(e)".format(PERSONS[pers_idx], assist_base,
                                                            _participe(verb, 1))
                    else:
                        answer = "{:s} {:s} {:s}(e)s".format(PERSONS[pers_idx], assist_base,
                                                             _participe(verb, 1))
                else:
                    answer = ' -- '
                conjug_list.append(answer)
        else:
            conjug_tuple = find_conjug_tuple(verb, tense, mood)
            for pers_idx in range(6):
                conjug_base = conjug_tuple[pers_idx + 2]
                if conjug_base:
                    if pers_idx == 0 and conjug_base.startswith("'"):
                        answer = "j" + conjug_base
                    else:
                        answer = PERSONS[pers_idx] + ' ' + conjug_base
                else:
                    answer = " -- "
                conjug_list.append(answer)
        return '\n'.join(conjug_list)
    else:
        if tense in _MAP_COMPOSE.keys():
            if verb in _ETRE_VERBS:
                assist_base = conjug("être", _MAP_COMPOSE[tense], mood, pers_idx)
            else:
                assist_base = conjug("avoir", _MAP_COMPOSE[tense], mood, pers_idx)
            conjug_tuple = find_conjug_tuple(verb, _MAP_COMPOSE[tense], mood)
            conjug_base = conjug_tuple[pers_idx + 2]
            if conjug_base:
                if pers_idx < 3:
                    answer = ' '.join([assist_base, _participe(verb, 1) + '(e)'])
                else:
                    answer = ' '.join([assist_base, _participe(verb, 1) + '(e)s'])
            else:
                answer = ''
        else:
            conjug_tuple = find_conjug_tuple(verb, tense, mood)
            conjug_base = conjug_tuple[pers_idx + 2]
            if conjug_base:
                if pers_idx == 0 and conjug_base.startswith("'"):
                    answer = "j" + conjug_base
                else:
                    answer = PERSONS[pers_idx] + ' ' + conjug_base
            else:
                answer = ''
    return answer


def find_conjug_tuple(verb, tense, mood):
    for conjug_tulpe in VERB_DICT[verb]:
        if conjug_tulpe.tense == tense and conjug_tulpe.mood == mood:
            return conjug_tulpe


def _participe(verb, tense_i):
    if verb in _PARTICIPE_IRREGULIER.keys():
        return _PARTICIPE_IRREGULIER[verb][tense_i]
    else:
        if verb.endswith('er'):
            if tense_i == 0:    # present
                return verb[:-2] + 'ant'
            else:
                return verb[:-2] + 'é'
        elif verb.endswith('ir'):
            if tense_i == 0:    # present
                return verb[:-2] + 'issant'
            else:
                return verb[:-2] + 'i'


VERB_DICT = {
    "aller": (
        _Conjug("présent", "indicatif",
                "vais", "vas", "va", "allons", "allez", "vont"),
    ),
    "appuyer": (
        _Conjug("présent", "indicatif",
                "'appuie", "appuies", "appuie", "appuyons", "appuyez", "appuient"),
    ),
    "asseoir": (
        _Conjug("présent", "indicatif",
                "'assieds", "assieds", "assied", "asseyons", "asseyez", "asseyent"),
    ),
    "avoir": (
        _Conjug("présent", "indicatif",
                "'ai", "as", "a", "avons", "avez", "ont"),
        _Conjug("passé simple", "indicatif",
                "'eus", "eus", "eut", "eûmes", "eûtes", "eurent"),
        _Conjug("futur", "indicatif",
                "aurai", "auras", "aura", "aurons", "aurez", "auront"),
        _Conjug("imparfait", "indicatif",
                "'avais", "avais", "avait", "avions", "aviez", "avaient"),
    ),
    "cueillir": (
        _Conjug("présent", "indicatif",
                "cueille", "cueilles", "cueille", "cueillons", "cueillez", "cueillent"),
    ),
    "être": (
        _Conjug("présent", "indicatif",
                "suis", "es", "est", "sommes", "êtes", "sont"),
        _Conjug("passé simple", "indicatif",
                "'fus", "fus", "fut", "fûmes", "fûtes", "furent"),
        _Conjug("futur", "indicatif",
                "serai", "seras", "sera", "serons", "serez", "seront"),
        _Conjug("imparfait", "indicatif",
                "'étais", "étais", "était", "étions", "étiez", "étaient"),
    ),
    "boire": (
        _Conjug("présent", "indicatif",
                "bois", "bois", "boit", "buvons", "buvez", "boivent"),
    ),
    "choisir": (
        _Conjug("présent", "indicatif",
                "choisis", "choisis", "choisit", "choisissons", "choisissez", "choisissent"),
    ),
    "conduire": (
        _Conjug("présent", "indicatif",
                "conduis", "conduis", "conduit", "conduisons", "conduisez", "conduisent"),
    ),
    "crier": (
        _Conjug("présent", "indicatif",
                "crie", "cries", "crie", "crions", "criyez", "crient"),
    ),
    "croire": (
        _Conjug("présent", "indicatif",
                "crois", "crois", "croit", "croyons", "croyez", "croient"),
    ),
    "cuire": (
        _Conjug("présent", "indicatif",
                "cuis", "cuis", "cuit", "cuisons", "cuisez", "cuisent"),
    ),
    "devenir": (
        _Conjug("présent", "indicatif",
                "deviens", "deviens", "devient", "devenons", "devenez", "deviennet"),
    ),
    "devoir": (
        _Conjug("présent", "indicatif",
                "dois", "dois", "doit", "devons", "devez", "doivent"),
    ),
    "dormir": (
        _Conjug("présent", "indicatif",
                "dors", "dors", "dort", "dormons", "dormez", "dorment"),
    ),
    "écrire": (
        _Conjug("présent", "indicatif",
                "'écris", "écris", "écrit", "écrivons", "écrivez", "écrivent"),
    ),
    "falloir": (
        _Conjug("présent", "indicatif",
                "", "", "faut", "", "", ""),
    ),
    "faire": (
        _Conjug("présent", "indicatif",
                "fais", "fais", "fait", "faisons", "faites", "font"),
    ),
    "finir": (
        _Conjug("présent", "indicatif",
                "finis", "finis", "finit", "finissons", "finissez", "finissent"),
    ),
    "louer": (
        _Conjug("présent", "indicatif",
                "loue", "loues", "loue", "louons", "louez", "louent"),
    ),
    "mourir": (
        _Conjug("présent", "indicatif",
                "meurs", "meurs", "meurt", "mourons", "mourez", "meurent"),
    ),
    "naître": (
        _Conjug("présent", "indicatif",
                "nais", "nais", "naît", "naissons", "naissez", "naissent"),
    ),
    "partager": (
        _Conjug("présent", "indicatif",
                "partage", "partages", "partage", "partageons", "partagez", "partagent"),
    ),
    "pleuvoir": (
        _Conjug("présent", "indicatif",
                "", "", "pleut", "", "", ""),
    ),
    "réduire": (
        _Conjug("présent", "indicatif",
                "réduis", "réduis", "réduit", "réduisons", "réduisez", "réduisent"),
    ),
    "résoudre": (
        _Conjug("présent", "indicatif",
                "résous", "résous", "résout", "résolvons", "résolvez", "résolvent"),
    ),
    "réunir": (
        _Conjug("présent", "indicatif",
                "réunis", "réunis", "réunit", "réunissons", "réunissez", "réunissent"),
    ),
    "rire": (
        _Conjug("présent", "indicatif",
                "ris", "ris", "rit", "rions", "riez", "rient"),
    ),
    "sertir": (
        _Conjug("présent", "indicatif",
                "sertis", "sertis", "sertit", "sertissons", "sertissez", "sertissent"),
    ),
    "servir": (
        _Conjug("présent", "indicatif",
                "sers", "sers", "sert", "servons", "servez", "servent"),
    ),
    "souffrir": (
        _Conjug("présent", "indicatif",
                "souffre", "souffres", "souffre", "souffrons", "souffrez", "souffrent"),
    ),
    "sortir": (
        _Conjug("présent", "indicatif",
                "sors", "sors", "sort", "sortons", "sortez", "sortent"),
    ),
    "tenir": (
        _Conjug("présent", "indicatif",
                "tiens", "tiens", "tient", "tenons", "tenez", "tiennent"),
    ),
    "tordre": (
        _Conjug("présent", "indicatif",
                "tords", "tords", "tord", "tordons", "tordez", "tordent"),
    ),
    "valoir": (
        _Conjug("présent", "indicatif",
                "vaux", "vaux", "vaut", "valons", "valez", "valent"),
    ),
    "venir": (
        _Conjug("présent", "indicatif",
                "viens", "viens", "vient", "venons", "venez", "viennent"),
    ),
    "vivre": (
        _Conjug("présent", "indicatif",
                "vis", "vis", "vit", "vivons", "vivez", "vivent"),
    ),
    "voir": (
        _Conjug("présent", "indicatif",
                "vois", "vois", "voit", "voyons", "voyez", "voient"),
    ),
    "vouloir": (
        _Conjug("présent", "indicatif",
                "veux", "veux", "veut", "voulons", "voulez", "veulent"),
    ),

}

_PARTICIPE_IRREGULIER = {
    "asseoir": ("asseyant", "assis"),
    "avoir": ("ayant", "eu"),
    "cueillir": ("cueillant", "cueilli"),
    "être": ("étant", "été"),
    "boire": ("buvant", "bu"),
    "conduire": ("conduisant", "conduit"),
    "crier": ("criant", "crié"),
    "croire": ("croyant", "cru"),
    "cuire": ("cuisant", "cuit"),
    "devenir": ("devenant", "devenu"),
    "devoir": ("devant", "dû"),
    "dormir": ("dormant", "dormi"),
    "écrire": ("écrivant", "écrit"),
    "falloir": ("", "fallu"),
    "faire": ("faisant", "fait"),
    "mourir": ("mourant", "mort"),
    "naître": ("naissant", "né"),
    "partager": ("partageant", "partagé"),
    "pleuvoir": ("pleuvant", "plu"),
    "réduire": ("réduisant", "réduit"),
    "résoudre": ("résolvant", "résolu"),
    "réunir": ("réunissant", "réuni"),
    "rire": ("riant", "ri"),
    "servir": ("servant", "servi"),
    "souffrir": ("souffrant", "souffert"),
    "sortir": ("sortant", "sorti"),
    "tenir": ("tenant", "tenu"),
    "tordre": ("tordant", "tordu"),
    "valoir": ("valant", "valu"),
    "venir": ("venant", "venu"),
    "vivre": ("vivant", "vécu"),
    "voir": ("voyant", "vu"),
    "vouloir": ("voulant", "voulu"),
}
