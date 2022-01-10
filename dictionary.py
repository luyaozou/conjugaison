from collections import namedtuple

_Conjug = namedtuple("Conjug", "tense, mood, je, tu, il, nous, vous, ils")

# verbs that conjugate with etre on passé composé, passé antérieur, et futur antérieur
_PASSE_COMPOSE_ETRE_VERBS = (
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

# index map of person to conjug tuple index
# the "person" distinguishes masculin / feminin
# the conjug tuple does not
_PERSON_IDX_MAP = {
    0:0,
    1:1,
    2:2,
    3:2,
    4:3,
    5:4,
    6:5,
    7:5
}

_VOWELS = ('a', 'â', 'à', 'e', 'é', 'è', 'i', 'o', 'u')
_DOUBLE_CONSONANTS = ('ch', 'gn', )

TENSES = (
    "présent",
    # "passé simple",
    "passé composé",
    # "imparfait",
    # "futur",
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
            if answer[-1] == 's':   # already ends with "s"
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
        return infinitive in _PASSE_COMPOSE_ETRE_VERBS or _check_pronominal(infinitive)
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
        new_root = ''.join([root[:-1-n_cons], 'è', root[-n_cons:]])
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
    if infinitive in _PASSE_COMPOSE_ETRE_VERBS or _check_pronominal(verb):
        aux = _VERBS_IRREG[('être', 'présent', 'indicatif')]
    else:
        aux = _VERBS_IRREG[('avoir', 'présent', 'indicatif')]
    group = _find_group(infinitive)
    if group == 1:
        part = infinitive[:-2] + 'é'
    elif group == 2:
        part = infinitive[:-1]
    else:
        part = _VERBS_IRREG[(infinitive, 'passé', 'participe')]
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
            if infinitive.endswith('re'):   # drop e and add suffix
                p1 = infinitive[:-1] + 'ai'
                p2 = infinitive[:-1] + 'as'
                p3 = infinitive[:-1] + 'a'
                p4 = infinitive[:-1] + 'ons'
                p5 = infinitive[:-1] + 'ez'
                p6 = infinitive[:-1] + 'ont'
            elif infinitive.endswith('ir'): # drop i and add suffix with double r
                p1 = infinitive[:-1] + 'rai'
                p2 = infinitive[:-1] + 'ras'
                p3 = infinitive[:-1] + 'ra'
                p4 = infinitive[:-1] + 'rons'
                p5 = infinitive[:-1] + 'rez'
                p6 = infinitive[:-1] + 'ront'
            else:
                raise KeyError
    else:
        if group == 1:
            # treat exceptions
            if infinitive.endswith('yer'):
                root = base[:-3] + 'ie'
            elif infinitive.endswith('eter') or infinitive.endswith('eler'):
                if infinitive in _VERB_FUTUR_EGRAVE:        # uses è
                    root = base[:-4] + 'è' + base[-3] + 'e'
                else:       # double t or l
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


_VERBS_IRREG = {
    ("aller", "présent", "indicatif"):
        ("vais", "vas", "va", "allons", "allez", "vont"),
    ("appuyer", "présent", "indicatif"):
        ("appuie", "appuies", "appuie", "appuyons", "appuyez", "appuient"),
    ("asseoir", "présent", "indicatif"):
        ("assieds", "assieds", "assied", "asseyons", "asseyez", "asseyent"),
    ("asseoir", "futur", "indicatif"):
        ("asseyerai", "asseyeras", "asseyera", "asseyerons", "asseyerez", "asseyerent"),
    ("asseoir", "présent", "participe"): "asseyant",
    ("asseoir", "passé", "participe"): "assis",
    ("avoir", "présent", "indicatif"):
        ("ai", "as", "a", "avons", "avez", "ont"),
    ("avoir", "passé simple", "indicatif"):
        ("'eus", "eus", "eut", "eûmes", "eûtes", "eurent"),
    ("avoir", "futur", "indicatif"):
        ("aurai", "auras", "aura", "aurons", "aurez", "auront"),
    ("avoir", "imparfait", "indicatif"):
        ("'avais", "avais", "avait", "avions", "aviez", "avaient"),
    ("avoir", "présent", "participe"): "ayant",
    ("avoir", "passé", "participe"): "eu",
    ("cueillir", "présent", "indicatif"):
        ("cueille", "cueilles", "cueille", "cueillons", "cueillez", "cueillent"),
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
    ("boire", "présent", "indicatif"):
        ("bois", "bois", "boit", "buvons", "buvez", "boivent"),
    ("boire", "présent", "participe"): "buvant",
    ("boire", "passé", "participe"): "bu",
    ("conduire", "présent", "indicatif"):
        ("conduis", "conduis", "conduit", "conduisons", "conduisez", "conduisent"),
    ("conduire", "présent", "participe"): "conduisant",
    ("conduire", "passé", "participe"): "conduit",
    ("crier", "présent", "indicatif"):
        ("crie", "cries", "crie", "crions", "criyez", "crient"),
    ("crier", "présent", "participe"): "criant",
    ("crier", "passé", "participe"): "crié",
    ("croire", "présent", "indicatif"):
        ("crois", "crois", "croit", "croyons", "croyez", "croient"),
    ("croire", "présent", "participe"): "croyant",
    ("croire", "passé", "participe"): "cru",
    ("cuire", "présent", "indicatif"):
        ("cuis", "cuis", "cuit", "cuisons", "cuisez", "cuisent"),
    ("cuire", "présent", "participe"): "cuisant",
    ("cuire", "passé", "participe"): "cuit",
    ("devenir", "présent", "indicatif"):
        ("deviens", "deviens", "devient", "devenons", "devenez", "deviennet"),
    ("devenir", "présent", "participe"): "devenant",
    ("devenir", "passé", "participe"): "devenu",
    ("devoir", "présent", "indicatif"):
        ("dois", "dois", "doit", "devons", "devez", "doivent"),
    ("devoir", "présent", "participe"): "devant",
    ("devoir", "passé", "participe"): "dû",
    ("dormir", "présent", "indicatif"):
        ("dors", "dors", "dort", "dormons", "dormez", "dorment"),
    ("dormir", "présent", "participe"): "dormant",
    ("dormir", "passé", "participe"): "dormi",
    ("écrire", "présent", "indicatif"):
        ("écris", "écris", "écrit", "écrivons", "écrivez", "écrivent"),
    ("écrire", "présent", "participe"): "écrivant",
    ("écrire", "passé", "participe"): "écrit",
    ("falloir", "présent", "indicatif"):
        ("", "", "faut", "", "", ""),
    ("falloir", "passé", "participe"): "fallu",
    ("faire", "présent", "indicatif"):
        ("fais", "fais", "fait", "faisons", "faites", "font"),
    ("faire", "présent", "participe"): "faisant",
    ("faire", "passé", "participe"): "fait",
    ("mourir", "présent", "indicatif"):
        ("meurs", "meurs", "meurt", "mourons", "mourez", "meurent"),
    ("mourir", "présent", "participe"): "mourant",
    ("mourir", "passé", "participe"): "mort",
    ("naître", "présent", "indicatif"):
        ("nais", "nais", "naît", "naissons", "naissez", "naissent"),
    ("naître", "présent", "participe"): "naissant",
    ("naître", "passé", "participe"): "né",
    ("pleuvoir", "présent", "indicatif"):
        ("", "", "pleut", "", "", ""),
    ("pleuvoir", "passé", "participe"): "plu",
    ("réduire", "présent", "indicatif"):
        ("réduis", "réduis", "réduit", "réduisons", "réduisez", "réduisent"),
    ("réduire", "présent", "participe"): "réduisant",
    ("réduire", "passé", "participe"): "réduit",
    ("résoudre", "présent", "indicatif"):
        ("résous", "résous", "résout", "résolvons", "résolvez", "résolvent"),
    ("résoudre", "présent", "participe"): "résolvant",
    ("résoudre", "passé", "participe"): "résolu",
    ("rire", "présent", "indicatif"):
        ("ris", "ris", "rit", "rions", "riez", "rient"),
    ("rire", "présent", "participe"): "riant",
    ("rire", "passé", "participe"): "ri",
    ("servir", "présent", "indicatif"):
        ("sers", "sers", "sert", "servons", "servez", "servent"),
    ("servir", "présent", "participe"): "servant",
    ("servir", "passé", "participe"): "servi",
    ("souffrir", "présent", "indicatif"):
        ("souffre", "souffres", "souffre", "souffrons", "souffrez", "souffrent"),
    ("souffrir", "présent", "participe"): "souffrant",
    ("souffrir", "passé", "participe"): "souffert",
    ("sortir", "présent", "indicatif"):
        ("sors", "sors", "sort", "sortons", "sortez", "sortent"),
    ("sortir", "présent", "participe"): "sortant",
    ("sortir", "passé", "participe"): "sorti",
    ("tenir", "présent", "indicatif"):
        ("tiens", "tiens", "tient", "tenons", "tenez", "tiennent"),
    ("tenir", "présent", "participe"): "tenant",
    ("tenir", "passé", "participe"): "tenu",
    ("tordre", "présent", "indicatif"):
        ("tords", "tords", "tord", "tordons", "tordez", "tordent"),
    ("tordre", "présent", "participe"): "tordant",
    ("tordre", "passé", "participe"): "tordu",
    ("valoir", "présent", "indicatif"):
        ("vaux", "vaux", "vaut", "valons", "valez", "valent"),
    ("valoir", "présent", "participe"): "valant",
    ("valoir", "passé", "participe"): "valu",
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
_VERB_FUTUR_EGRAVE = (
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
