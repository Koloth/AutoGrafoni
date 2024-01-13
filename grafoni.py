import eng_to_ipa as ipa
import drawsvg as draw
from math import sqrt
from collections import defaultdict

convert_dict = {
    'i': ["uv1","uv1"], # sometimes can be duplicated like "see"
    'ɪ': ["uv1"],
    'ɛ': ["uv2"],
    'e': ["uv2"],
    'æ': ["uv3"],
    'ʊ': ["mv1"],
    'ə': ["mv2"],
    'ɑ': ["mv3"],
    'a': ["mv3"],
    'u': ["lv1"],
    'o': ["lv2"],
    'ɔ': ["lv3"],

    'j': ["uv1"],
    'w': ["lv1"],

    'θ': ["th"],
    'ð': ["dh"],
    'ʃ': ["sh"],
    'ʒ': ["zh"],

    'ʤ': ["d","zh"],
    'ʧ': ["t","sh"],

    'ŋ': ["ng"],

    'ˈ': [],
    'ˌ': [],
    '*': [],
    
    ' ': [" "]
}

vowel_scale = 1.5

letter_forms = {
    " ": [('move',4,0)],

    "uv1": [('quadratic',1*vowel_scale,-1*vowel_scale,2*vowel_scale,0)],
    "uv2": [('quadratic',2*vowel_scale,-2*vowel_scale,4*vowel_scale,0)],
    "uv3": [('quadratic',4*vowel_scale,-4*vowel_scale,8*vowel_scale,0)],
    "mv1": [('line',2*vowel_scale,0)],
    "mv2": [('line',4*vowel_scale,0)],
    "mv3": [('line',8*vowel_scale,0)],
    "lv1": [('quadratic',1*vowel_scale,1*vowel_scale,2*vowel_scale,0)],
    "lv2": [('quadratic',2*vowel_scale,2*vowel_scale,4*vowel_scale,0)],
    "lv3": [('quadratic',4*vowel_scale,4*vowel_scale,8*vowel_scale,0)],

    "r": [('cubic',1,-2,1,-4,0,-4),('cubic',-1,-4,-1,-2,0,0)],
    "l": [('cubic',1,-2,1,-8,0,-8),('cubic',-1,-8,-1,-2,0,0)],
    # "m": [('cubic',1,0,1,2,0,2),('cubic',-1,2,-1,0,0,0)],
    # "m": [('cubic',2,2,-2,2,0,0)],
    # "m": [('cubic',3,0,0,3,0,0)],
    # "m": [('cubic',3,3,0,3,0,0)],
    # "m": [('cubic',0,3,-3,3,0,0)],
    "m": [('cubic',0.5,1,0.5,2,0,2),('cubic',-0.5,2,-0.5,1,0,0)],
    "n": [('cubic',1,2,1,4,0,4),('cubic',-1,4,-1,2,0,0)],
    "ng":[('cubic',1,2,1,8,0,8),('cubic',-1,8,-1,2,0,0)],

    "k": [('cubic',2,-2,0,-2,2,-4),('quadratic',0,-2,2,0)],
    "g": [('cubic',2,-2,0,-4,2,-8),('quadratic',0,-4,2,0)],
    "h": [('cubic',2,2,0,2,2,4),('quadratic',0,2,2,0)],
    "x": [('cubic',2,2,0,4,2,8),('quadratic',0,4,2,0)],

    "t": [('quadratic',2,0,2,-2),('line',2,-4),('line',2,0)],
    "d": [('quadratic',2,0,2,-2),('line',2,-8),('line',2,0)],
    "th": [('line',0,4),('line',0,2),('quadratic',0,0,2,0)],
    "dh": [('line',0,8),('line',0,2),('quadratic',0,0,2,0)],

    "p": [('quadratic',2,-2,0,-4),('cubic',2,-2,0,-2,2,0)],
    "b": [('quadratic',2,-4,0,-8),('cubic',2,-4,0,-2,2,0)],
    "f": [('quadratic',2,2,0,4),('cubic',2,2,0,2,2,0)],
    "v": [('quadratic',2,4,0,8),('cubic',2,4,0,2,2,0)],

    "s": [('quadratic',0,-4,1,-4),('quadratic',2,-4,2,0)],
    "z": [('quadratic',0,-8,1,-8),('quadratic',2,-8,2,0)],
    "sh": [('quadratic',0,4,1,4),('quadratic',2,4,2,0)],
    "zh": [('quadratic',0,8,1,8),('quadratic',2,8,2,0)],

    "Y": [('cubic',1,1,-1,1,0,0)],
    "W": [('cubic',1,-1,-1,-1,0,0)],

    "k-beg": [('move',0,-4),('quadratic',-2,-2,0,0)],
    "g-beg": [('move',0,-8),('quadratic',-2,-4,0,0)],
    "h-beg": [('move',0,4),('quadratic',-2,2,0,0)],
    "x-beg": [('move',0,8),('quadratic',-2,4,0,0)],

    "t-beg": [('move',0,-4),('line',0,0)],
    "d-beg": [('move',0,-8),('line',0,0)],
    "th-beg": [('move',0,4),('line',0,0)],
    "dh-beg": [('move',0,8),('line',0,0)],

    "p-beg": [('move',0,-4),('quadratic',2,-2,0,0)],
    "b-beg": [('move',0,-8),('quadratic',2,-4,0,0)],
    "f-beg": [('move',0,4),('quadratic',2,2,0,0)],
    "v-beg": [('move',0,8),('quadratic',2,4,0,0)],

    "k-end": [('quadratic',-2,-2,0,-4),('move',0,0)],
    "g-end": [('quadratic',-2,-4,0,-8),('move',0,0)],
    "h-end": [('quadratic',-2,2,0,4),('move',0,0)],
    "x-end": [('quadratic',-2,4,0,8),('move',0,0)],

    "t-end": [('line',0,-4),('move',0,0)],
    "d-end": [('line',0,-8),('move',0,0)],
    "th-end": [('line',0,4),('move',0,0)],
    "dh-end": [('line',0,8),('move',0,0)],

    "p-end": [('quadratic',2,-2,0,-4),('move',0,0)],
    "b-end": [('quadratic',2,-4,0,-8),('move',0,0)],
    "f-end": [('quadratic',2,2,0,4),('move',0,0)],
    "v-end": [('quadratic',2,4,0,8),('move',0,0)],

    ".": [('move',2,0),('quadratic',2,0.25,2.125,0.25),('quadratic',2.25,0.25,2.25,0),('quadratic',2.25,-0.25,2.125,-0.25),('quadratic',2,-0.25,2,0),('move',4,0)],
    ",": [('move',2,0),('quadratic',3,1,2,2),('move',4,0)],
    ":": [('move',2,2),('quadratic',2,2.25,2.125,2.25),('quadratic',2.25,2.25,2.25,2),('quadratic',2.25,1.75,2.125,1.75),('quadratic',2,1.75,2,2),('move',2,-2),('quadratic',2,-2.25,2.125,-2.25),('quadratic',2.25,-2.25,2.25,-2),('quadratic',2.25,-1.75,2.125,-1.75),('quadratic',2,-1.75,2,-2),('move',4,0)], 
    ";": [('move',2,2),('quadratic',3,3,2,4),('move',2,-2),('quadratic',2,-2.25,2.125,-2.25),('quadratic',2.25,-2.25,2.25,-2),('quadratic',2.25,-1.75,2.125,-1.75),('quadratic',2,-1.75,2,-2),('move',4,0)],   
    #"-": [('move',2,-1),('line',3,1),('move',5,0)], #from the 1910 edition
    "-": [('move',2,-1),('line',4,-1),('move',2,1),('line',4,1),('move',6,0)], #from the 1913 edition
    "(": [('move',3,6),('quadratic',0,0,3,-6),('move',5,0)],
    ")": [('move',2,6),('quadratic',5,0,2,-6),('move',5,0)],

    #from the 1917 book on just the numerals, not from the 1913 text
    "1": [('move',0,-8),('line',0,0),('move',3,0)],
    "2": [('move',0,-8),('quadratic',2,-8,0,-4),('quadratic',-1,-2,0,0),('move',3,0)],
    "3": [('move',0,-8),('quadratic',2,-6,0,-4),('quadratic',2,-2,0,0),('move',3,0)],
    "4": [('move',0,-8),('quadratic',2,-4,0,0),('line',2,-2),('move',3,0)],
    "5": [('move',0,-8),('quadratic',-2,-6,0,-4),('quadratic',2,-2,0,0),('move',3,0)],
    "6": [('move',1,-8),('quadratic',-1,0,1,0),('quadratic',2,0,3,-1),('move',4,0)],
    "7": [('move',-1,-6),('quadratic',0,-7,0,-8),('line',0,0),('move',3,0)],
    "8": [('move',0,-8),('line',0,-4),('quadratic',0,0,-1,0),('quadratic',-2,0,0,-4),('move',3,0)],
    "9": [('move',0,-8),('quadratic',2,-4,0,0),('move',3,0)],
    "0": [('move',0,-4),('quadratic',1,-5,2,-4),('move',3,0)],
}

# this dictionary will hold kerning instructions for pairs of letters, it says how much to kern the left letter on the right and the right letter on the left
kerning = defaultdict(lambda: (-1,-1))
kerning[("t-beg","r")] = (-1,2)
kerning[("t-beg","l")] = (-1,2)
kerning[("d-beg","r")] = (-1,2)
kerning[("d-beg","l")] = (-1,2)
kerning[("t","r")] = (-1,2)
kerning[("t","l")] = (-1,2)
kerning[("d","r")] = (-1,2)
kerning[("d","l")] = (-1,2)
kerning[("t","s")] = (-1,2)
kerning[("t","z")] = (-1,2)
kerning[("d","s")] = (-1,2)
kerning[("d","z")] = (-1,2)
kerning[("g-beg","r")] = (1,1)
kerning[("g-beg","l")] = (1,1)
kerning[("k-beg","r")] = (1,1)
kerning[("k-beg","l")] = (1,1)
kerning[("g","r")] = (1,1)
kerning[("g","l")] = (1,1)
kerning[("k","r")] = (1,1)
kerning[("k","l")] = (1,1)
kerning[("r","p")] = (1,0.5)
kerning[("r","b")] = (1,0.5)
kerning[("l","p")] = (1,0.5)
kerning[("l","b")] = (1,0.5)
kerning[("p-beg","r")] = (-1,2.5)
kerning[("p-beg","l")] = (-1,2.5)
kerning[("b-beg","r")] = (-1,2.5)
kerning[("b-beg","l")] = (-1,2.5)
kerning[("p","r")] = (0.5,1)
kerning[("p","l")] = (0.5,1)
kerning[("b","r")] = (0.5,0.5)
kerning[("b","l")] = (0.5,0.5)
kerning[("r","l")] = (1,1)
kerning[("r","k")] = (0.5,0.5)
kerning[("r","g")] = (0.5,0.5)
kerning[("r","s")] = (1.5,0.5)
kerning[("r","z")] = (1.5,0.5)
kerning[("l","r")] = (1,1)
kerning[("l","k")] = (0.5,0.5)
kerning[("l","g")] = (0.5,0.5)
kerning[("l","s")] = (1.5,0.5)
kerning[("l","z")] = (1.5,0.5)
kerning[("s","t-end")] = (-1,1)
kerning[("s","d-end")] = (-1,1)
kerning[("z","t-end")] = (-1,1)
kerning[("z","d-end")] = (-1,1)
kerning[("r","t-end")] = (2,-1)
kerning[("r","d-end")] = (2,-1)
kerning[("l","t-end")] = (2,-1)
kerning[("l","d-end")] = (2,-1)
kerning[("k","t-end")] = (2,-1)
kerning[("k","d-end")] = (2,-1)
kerning[("g","t-end")] = (2,-1)
kerning[("g","d-end")] = (2,-1)
kerning[("s","p")] = (-1,1)
kerning[("s","b")] = (-1,1)
kerning[("z","p")] = (-1,1)
kerning[("z","b")] = (-1,1)
kerning[("s","k")] = (-1,0.5)
kerning[("s","g")] = (-1,0.5)
kerning[("z","k")] = (-1,0.5)
kerning[("z","g")] = (-1,0.5)
kerning[("s","r")] = (-1,2)
kerning[("s","l")] = (-1,2)
kerning[("z","r")] = (-1,2)
kerning[("z","l")] = (-1,2)
kerning[("k","s")] = (1,-1)
kerning[("k","z")] = (1,-1)
kerning[("g","s")] = (1,-1)
kerning[("g","z")] = (1,-1)
kerning[("s","k-end")] = (2,-1)
kerning[("s","g-end")] = (2,-1)
kerning[("z","k-end")] = (2,-1)
kerning[("z","g-end")] = (2,-1)
kerning[("k-beg","s")] = (1,-1)
kerning[("k-beg","z")] = (1,-1)
kerning[("g-beg","s")] = (1,-1)
kerning[("g-beg","z")] = (1,-1)
kerning[("t","r")] = (-1,2)
kerning[("t","l")] = (-1,2)
kerning[("d","r")] = (-1,2)
kerning[("d","l")] = (-1,2)
kerning[("t","k")] = (-1,2)
kerning[("t","g")] = (-1,2)
kerning[("d","k")] = (-1,2)
kerning[("d","g")] = (-1,2)
kerning[("t","p")] = (-1,2)
kerning[("t","b")] = (-1,2)
kerning[("d","p")] = (-1,2)
kerning[("d","b")] = (-1,2)
kerning[("r","mv1")] = (1,-1)
kerning[("r","mv2")] = (1,-1)
kerning[("r","mv3")] = (1,-1)
kerning[("l","mv1")] = (1,-1)
kerning[("l","mv2")] = (1,-1)
kerning[("l","mv3")] = (1,-1)
kerning[("mv1","r")] = (-1,1)
kerning[("mv2","r")] = (-1,1)
kerning[("mv3","r")] = (-1,1)
kerning[("mv1","l")] = (-1,1)
kerning[("mv2","l")] = (-1,1)
kerning[("mv3","l")] = (-1,1)
kerning[("n","mv1")] = (1,-1)
kerning[("n","mv2")] = (1,-1)
kerning[("n","mv3")] = (1,-1)
kerning[("ng","mv1")] = (1,-1)
kerning[("ng","mv2")] = (1,-1)
kerning[("ng","mv3")] = (1,-1)
kerning[("mv1","n")] = (-1,1)
kerning[("mv2","n")] = (-1,1)
kerning[("mv3","n")] = (-1,1)
kerning[("mv1","ng")] = (-1,1)
kerning[("mv2","ng")] = (-1,1)
kerning[("mv3","ng")] = (-1,1)
kerning[("n","sh")] = (2,-1)
kerning[("n","zh")] = (2,-1)
kerning[("ng","sh")] = (2,-1)
kerning[("ng","zh")] = (2,-1)
kerning[("m","r")] = (-1,1)
kerning[("m","l")] = (-1,1)
kerning[("n","r")] = (0.5,0.5)
kerning[("n","l")] = (0.5,0.5)
kerning[("ng","r")] = (0.5,0.5)
kerning[("ng","l")] = (0.5,0.5)
kerning[("r","m")] = (1,-1)
kerning[("r","n")] = (0.5,0.5)
kerning[("r","ng")] = (0.5,0.5)
kerning[("l","m")] = (1,-1)
kerning[("l","n")] = (0.5,0.5)
kerning[("l","ng")] = (0.5,0.5)
kerning[("n","h")] = (0.5,0.5)
kerning[("n","x")] = (0.5,0.5)
kerning[("ng","h")] = (0.5,0.5)
kerning[("ng","x")] = (0.5,0.5)
kerning[("r","k")] = (0.5,0.5)
kerning[("l","k")] = (0.5,0.5)
kerning[("r","g")] = (0.5,0.5)
kerning[("l","g")] = (0.5,0.5)
kerning[("r","k-end")] = (2.5,-1)
kerning[("l","k-end")] = (2.5,-1)
kerning[("r","g-end")] = (2.5,-1)
kerning[("l","g-end")] = (2.5,-1)
kerning[("p","t-end")] = (1,-1)
kerning[("p","d-end")] = (1,-1)
kerning[("b","t-end")] = (1,-1)
kerning[("b","d-end")] = (1,-1)
kerning[("n","f")] = (1,1)
kerning[("n","v")] = (1,1)
kerning[("m","n")] = (-1,1.5)
kerning[("m","ng")] = (-1,1.5)
kerning[("n","m")] = (1.5,-1)
kerning[("ng","m")] = (1.5,-1)
kerning[("r","p-end")] = (2,-1)
kerning[("l","p-end")] = (2,-1)
kerning[("r","b-end")] = (2,-1)
kerning[("l","b-end")] = (2,-1)
kerning[("m","th")] = (2,-1)
kerning[("m","dh")] = (2,-1)
kerning[("n","th")] = (2,-1)
kerning[("n","dh")] = (2,-1)
kerning[("ng","th")] = (2,-1)
kerning[("ng","dh")] = (2,-1)
kerning[("r","r")] = (1,1)
kerning[("l","l")] = (1,1)
kerning[("m","m")] = (0.5,0.5)
kerning[("n","n")] = (1,1)
kerning[("ng","ng")] = (1,1)
kerning[("m","th-end")] = (2,-1)
kerning[("m","dh-end")] = (2,-1)
kerning[("n","th-end")] = (2,-1)
kerning[("n","dh-end")] = (2,-1)
kerning[("ng","th-end")] = (2,-1)
kerning[("ng","dh-end")] = (2,-1)
kerning[("sh","m")] = (-1,1)
kerning[("zh","m")] = (-1,1)
kerning[("m","sh")] = (1,-1)
kerning[("m","zh")] = (1,-1)

ligatures = {
    "n_t": [('cubic',1,2,1,4,0,4),('cubic',-1,4,-1,2,0,0),('quadratic',1,-2,1,-4),('line',1,0)],
    "n_d": [('cubic',1,2,1,4,0,4),('cubic',-1,4,-1,2,0,0),('quadratic',1,-2,1,-4),('line',1,-8),('line',1,0)],
    "ng_t": [('cubic', 1, 2, 1, 8, 0, 8), ('cubic', -1, 8, -1, 2, 0, 0), ('quadratic',1,-2,1,-4),('line',1,0)],
    "ng_d": [('cubic', 1, 2, 1, 8, 0, 8), ('cubic', -1, 8, -1, 2, 0, 0), ('quadratic',1,-2,1,-4),('line',1,-8),('line',1,0)],
    
    "r_th": [('cubic',1,-2,1,-4,0,-4),('cubic',-1,-4,-1,-2,0,0),('quadratic',1,2,1,4),('line',1,0)],
    "r_dh": [('cubic',1,-2,1,-4,0,-4),('cubic',-1,-4,-1,-2,0,0),('quadratic',1,2,1,4),('line',1,8),('line',1,0)],
    "l_th": [('cubic', 1, -2, 1, -8, 0, -8), ('cubic', -1, -8, -1, -2, 0, 0), ('quadratic',1,2,1,4),('line',1,0)],
    "l_dh": [('cubic', 1, -2, 1, -8, 0, -8), ('cubic', -1, -8, -1, -2, 0, 0), ('quadratic',1,2,1,4),('line',1,8),('line',1,0)],

    "m_t-end": [('cubic',1,1,1,2,0.5,2),('cubic',0,2,0,1,0,0),('line',0,-4),('move',0,0)],
    "m_d-end": [('cubic',1,1,1,2,0.5,2),('cubic',0,2,0,1,0,0),('line',0,-8),('move',0,0)],
    "n_t-end": [('cubic',2,2,2,4,1,4),('cubic',0,4,0,2,0,0),('line',0,-4),('move',0,0)],
    "n_d-end": [('cubic',2,2,2,4,1,4),('cubic',0,4,0,2,0,0),('line',0,-8),('move',0,0)],
    "ng_t-end": [('cubic',2,2,2,8,1,8),('cubic',0,8,0,2,0,0),('line',0,-4),('move',0,0)],
    "ng_d-end": [('cubic',2,2,2,8,1,8),('cubic',0,8,0,2,0,0),('line',0,-8),('move',0,0)],
    "th-beg_r": [('move',0,4),('line',0,0),('cubic',0,-2,0,-4,-1,-4),('cubic',-2,-4,-2,-2,0,0)],
    "th-beg_l": [('move',0,4),('line',0,0),('cubic',0,-2,0,-8,-1,-8),('cubic',-2,-8,-2,-2,0,0)],
    "dh-beg_r": [('move',0,8),('line',0,0),('cubic',0,-2,0,-4,-1,-4),('cubic',-2,-4,-2,-2,0,0)],
    "dh-beg_l": [('move',0,8),('line',0,0),('cubic',0,-2,0,-8,-1,-8),('cubic',-2,-8,-2,-2,0,0)],

    "r_th-end": [('cubic',2,-2,2,-4,1,-4),('cubic',0,-4,0,-2,0,0),('line',0,4),('move',0,0)],
    "r_dh-end": [('cubic',2,-2,2,-4,1,-4),('cubic',0,-4,0,-2,0,0),('line',0,8),('move',0,0)],
    "l_th-end": [('cubic',2,-2,2,-8,1,-8),('cubic',0,-8,0,-2,0,0),('line',0,4),('move',0,0)],
    "l_dh-end": [('cubic',2,-2,2,-8,1,-8),('cubic',0,-8,0,-2,0,0),('line',0,8),('move',0,0)],
    
    "n_s": [('cubic',2,2,2,4,1,4),('cubic',0,4,0,2,0,0), ('quadratic', 0, -4, 1, -4), ('quadratic', 2, -4, 2, 0)],
    "n_z": [('cubic',2,2,2,4,1,4),('cubic',0,4,0,2,0,0), ('quadratic', 0, -8, 1, -8), ('quadratic', 2, -8, 2, 0)],
    "ng_s": [('cubic',2,2,2,8,1,8),('cubic',0,8,0,2,0,0), ('quadratic', 0, -4, 1, -4), ('quadratic', 2, -4, 2, 0)],
    "ng_z": [('cubic',2,2,2,8,1,8),('cubic',0,8,0,2,0,0), ('quadratic', 0, -8, 1, -8), ('quadratic', 2, -8, 2, 0)],
    "r_sh": [('cubic',2,-2,2,-4,1,-4),('cubic',0,-4,0,-2,0,0), ('quadratic', 0, 4, 1, 4), ('quadratic', 2, 4, 2, 0)],
    "r_zh": [('cubic',2,-2,2,-4,1,-4),('cubic',0,-4,0,-2,0,0), ('quadratic', 0, 8, 1, 8), ('quadratic', 2, 8, 2, 0)],
    "l_sh": [('cubic',2,-2,2,-8,1,-8),('cubic',0,-8,0,-2,0,0), ('quadratic', 0, 4, 1, 4), ('quadratic', 2, 4, 2, 0)],
    "l_zh": [('cubic',2,-2,2,-8,1,-8),('cubic',0,-8,0,-2,0,0), ('quadratic', 0, 8, 1, 8), ('quadratic', 2, 8, 2, 0)],
    "s_n": [('quadratic', 0, -4, 1, -4), ('quadratic', 2, -4, 2, 0), ('cubic', 2, 2, 2, 4, 1, 4), ('cubic', 0, 4, 0, 2, 2, 0)],
    "z_n": [('quadratic', 0, -8, 1, -8), ('quadratic', 2, -8, 2, 0), ('cubic', 2, 2, 2, 4, 1, 4), ('cubic', 0, 4, 0, 2, 2, 0)],
    "s_ng": [('quadratic', 0, -4, 1, -4), ('quadratic', 2, -4, 2, 0), ('cubic', 2, 2, 2, 8, 1, 8), ('cubic', 0, 8, 0, 2, 2, 0)],
    "z_ng": [('quadratic', 0, -8, 1, -8), ('quadratic', 2, -8, 2, 0), ('cubic', 2, 2, 2, 8, 1, 8), ('cubic', 0, 8, 0, 2, 2, 0)],
    "sh_r": [('quadratic', 0, 4, 1, 4), ('quadratic', 2, 4, 2, 0), ('cubic', 2, -2, 2, -4, 1, -4), ('cubic', 0, -4, 0, -2, 2, 0)],
    "zh_r": [('quadratic', 0, 8, 1, 8), ('quadratic', 2, 8, 2, 0), ('cubic', 2, -2, 2, -4, 1, -4), ('cubic', 0, -4, 0, -2, 2, 0)],
    "sh_l": [('quadratic', 0, 4, 1, 4), ('quadratic', 2, 4, 2, 0), ('cubic', 2, -2, 2, -8, 1, -8), ('cubic', 0, -8, 0, -2, 2, 0)],
    "zh_l": [('quadratic', 0, 8, 1, 8), ('quadratic', 2, 8, 2, 0), ('cubic', 2, -2, 2, -8, 1, -8), ('cubic', 0, -8, 0, -2, 2, 0)],      

    "th_uv1": [('line',0,4),('line',0,2),('cubic',0,0,1*vowel_scale,-1*vowel_scale,2*vowel_scale,0)],
    "th_uv2": [('line',0,4),('line',0,2),('cubic',0,0,2*vowel_scale,-2*vowel_scale,4*vowel_scale,0)],
    "th_uv3": [('line',0,4),('line',0,2),('cubic',0,0,4*vowel_scale,-4*vowel_scale,8*vowel_scale,0)],
    "dh_uv1": [('line',0,8),('line',0,2),('cubic',0,0,1*vowel_scale,-1*vowel_scale,2*vowel_scale,0)],
    "dh_uv2": [('line',0,8),('line',0,2),('cubic',0,0,2*vowel_scale,-2*vowel_scale,4*vowel_scale,0)],
    "dh_uv3": [('line',0,8),('line',0,2),('cubic',0,0,4*vowel_scale,-4*vowel_scale,8*vowel_scale,0)],
    "lv1_t": [('cubic',1*vowel_scale,1*vowel_scale,2*vowel_scale,0,2*vowel_scale,-2),('line',2*vowel_scale,-4),('line',2*vowel_scale,0)],
    "lv2_t": [('cubic',2*vowel_scale,2*vowel_scale,4*vowel_scale,0,4*vowel_scale,-2),('line',4*vowel_scale,-4),('line',4*vowel_scale,0)],
    "lv3_t": [('cubic',4*vowel_scale,4*vowel_scale,8*vowel_scale,0,8*vowel_scale,-2),('line',8*vowel_scale,-4),('line',8*vowel_scale,0)],
    "lv1_d": [('cubic',1*vowel_scale,1*vowel_scale,2*vowel_scale,0,2*vowel_scale,-2),('line',2*vowel_scale,-8),('line',2*vowel_scale,0)],
    "lv2_d": [('cubic',2*vowel_scale,2*vowel_scale,4*vowel_scale,0,4*vowel_scale,-2),('line',4*vowel_scale,-8),('line',4*vowel_scale,0)],
    "lv3_d": [('cubic',4*vowel_scale,4*vowel_scale,8*vowel_scale,0,8*vowel_scale,-2),('line',8*vowel_scale,-8),('line',8*vowel_scale,0)],

    "s_f": [('quadratic', 0, -4, 1, -4), ('quadratic', 2, -4, 2, 0), ('quadratic', 2, 4, 1, 4), ('cubic', 2, 4, 2, 0, 3, 0)],
    "z_f": [('quadratic', 0, -8, 1, -8), ('quadratic', 2, -8, 2, 0), ('quadratic', 2, 4, 1, 4), ('cubic', 2, 4, 2, 0, 3, 0)],
    "s_v": [('quadratic', 0, -4, 1, -4), ('quadratic', 2, -4, 2, 0), ('quadratic', 2, 8, 1, 8), ('cubic', 2, 8, 2, 0, 3, 0)],
    "z_v": [('quadratic', 0, -8, 1, -8), ('quadratic', 2, -8, 2, 0), ('quadratic', 2, 8, 1, 8), ('cubic', 2, 8, 2, 0, 3, 0)],
    "h_s": [('cubic', 1, 0, 1, 4, 2, 4), ('quadratic', 1, 4, 1, 0), ('quadratic', 1, -4, 2, -4), ('quadratic', 3, -4, 3, 0)],
    "h_z": [('cubic', 1, 0, 1, 4, 2, 4), ('quadratic', 1, 4, 1, 0), ('quadratic', 1, -8, 2, -8), ('quadratic', 3, -8, 3, 0)],
    "x_s": [('cubic', 1, 0, 1, 8, 2, 8), ('quadratic', 1, 8, 1, 0), ('quadratic', 1, -4, 2, -4), ('quadratic', 3, -4, 3, 0)],
    "x_z": [('cubic', 1, 0, 1, 8, 2, 8), ('quadratic', 1, 8, 1, 0), ('quadratic', 1, -8, 2, -8), ('quadratic', 3, -8, 3, 0)],
    "sh_p": [('quadratic', 0, 4, 1, 4), ('quadratic', 2, 4, 2, 0), ('quadratic', 2, -4, 1, -4), ('cubic', 2, -4, 2, 0, 3, 0)],
    "zh_p": [('quadratic', 0, 8, 1, 8), ('quadratic', 2, 8, 2, 0), ('quadratic', 2, -4, 1, -4), ('cubic', 2, -4, 2, 0, 3, 0)],
    "sh_b": [('quadratic', 0, 4, 1, 4), ('quadratic', 2, 4, 2, 0), ('quadratic', 2, -8, 1, -8), ('cubic', 2, -8, 2, 0, 3, 0)],
    "zh_b": [('quadratic', 0, 8, 1, 8), ('quadratic', 2, 8, 2, 0), ('quadratic', 2, -8, 1, -8), ('cubic', 2, -8, 2, 0, 3, 0)],
    "k_sh": [('cubic', 1, 0, 1, -4, 2, -4), ('quadratic', 1, -4, 1, 0), ('quadratic', 1, 4, 2, 4), ('quadratic', 3, 4, 3, 0)],
    "k_zh": [('cubic', 1, 0, 1, -4, 2, -4), ('quadratic', 1, -4, 1, 0), ('quadratic', 1, 8, 2, 8), ('quadratic', 3, 8, 3, 0)],
    "g_sh": [('cubic', 1, 0, 1, -8, 2, -8), ('quadratic', 1, -8, 1, 0), ('quadratic', 1, 4, 2, 4), ('quadratic', 3, 4, 3, 0)],
    "g_zh": [('cubic', 1, 0, 1, -8, 2, -8), ('quadratic', 1, -8, 1, 0), ('quadratic', 1, 8, 2, 8), ('quadratic', 3, 8, 3, 0)],
        
    "v_r": [('quadratic', 2, 4, 0, 8), ('cubic', 2, 4, 0, 2, 1, 0), ('cubic', 2, -2, 2, -4, 1, -4), ('cubic', 0, -4, 0, -2, 1, 0)],
    "v_l": [('quadratic', 2, 4, 0, 8), ('cubic', 2, 4, 0, 2, 1, 0), ('cubic', 2, -4, 2, -8, 1, -8), ('cubic', 0, -8, 0, -4, 1, 0)],
    "f_r": [('quadratic', 2, 2, 0, 4), ('cubic', 2, 2, 0, 1, 1, 0), ('cubic', 2, -2, 2, -4, 1, -4), ('cubic', 0, -4, 0, -2, 1, 0)],
    "f_l": [('quadratic', 2, 2, 0, 4), ('cubic', 2, 2, 0, 1, 1, 0), ('cubic', 2, -4, 2, -8, 1, -8), ('cubic', 0, -8, 0, -4, 1, 0)],
    "n_k": [('cubic', 1, 2, 1, 4, 0, 4), ('cubic', -1, 4, -1, 2, 0, 0), ('cubic', 1, -1, -1, -2, 1, -4), ('quadratic', -1, -2, 1, 0)],
    "n_g": [('cubic', 1, 2, 1, 4, 0, 4), ('cubic', -1, 4, -1, 2, 0, 0), ('cubic', 1, -2, -1, -4, 1, -8), ('quadratic', -1, -4, 1, 0)],
    "ng_k": [('cubic', 1, 2, 1, 8, 0, 8), ('cubic', -1, 8, -1, 2, 0, 0), ('cubic', 1, -1, -1, -2, 1, -4), ('quadratic', -1, -2, 1, 0)],
    "ng_g": [('cubic', 1, 2, 1, 8, 0, 8), ('cubic', -1, 8, -1, 2, 0, 0), ('cubic', 1, -2, -1, -4, 1, -8), ('quadratic', -1, -4, 1, 0)],
    
    "f-beg_r": [('move', 0, 4), ('quadratic', 2, 3, 2, 0), ('cubic', 2, -2, 2, -4, 1, -4), ('cubic', 0, -4, 0, -2, 2, 0)],
    "f-beg_l": [('move', 0, 4), ('quadratic', 2, 3, 2, 0), ('cubic', 2, -4, 2, -8, 1, -8), ('cubic', 0, -8, 0, -4, 2, 0)],
    "n_k-end": [('cubic', 2, 2, 2, 4, 1, 4), ('cubic', 0, 4, 0, 2, 0, 0), ('quadratic', 0, -3, 2, -4), ('move', 2, 0)],
    "ng_k-end": [('cubic', 2, 4, 2, 8, 1, 8), ('cubic', 0, 8, 0, 4, 0, 0), ('quadratic', 0, -3, 2, -4), ('move', 2, 0)],

    "f_s": [('quadratic', 2, 2, 0, 4), ('cubic', 1, 3, 1.5, 2,1.5,0), ('quadratic', 1.5, -4, 2.5, -4), ('quadratic', 3.5, -4, 3.5, 0)],
    "f_z": [('quadratic', 2, 2, 0, 4), ('cubic', 1, 3, 1.5, 2,1.5,0), ('quadratic', 1.5, -8, 2.5, -8), ('quadratic', 3.5, -8, 3.5, 0)],   
    "v_s": [('quadratic', 2, 4, 0, 8), ('cubic', 1, 6, 1.5, 4,1.5,0), ('quadratic', 1.5, -4, 2.5, -4), ('quadratic', 3.5, -4, 3.5, 0)],
    "v_z": [('quadratic', 2, 4, 0, 8), ('cubic', 1, 6, 1.5, 4,1.5,0), ('quadratic', 1.5, -8, 2.5, -8), ('quadratic', 3.5, -8, 3.5, 0)],

    "f_t-end": [('quadratic', 2, 2, 0, 4), ('cubic', 1, 3, 1.5, 2,1.5,0), ('line', 1.5, -4), ('move', 1.5, 0)],
    "f_d-end": [('quadratic', 2, 2, 0, 4), ('cubic', 1, 3, 1.5, 2,1.5,0), ('line', 1.5, -8), ('move', 1.5, 0)],
    "v_t-end": [('quadratic', 2, 4, 0, 8), ('cubic', 1, 6, 1.5, 4,1.5,0), ('line', 1.5, -4), ('move', 1.5, 0)],
    "v_d-end": [('quadratic', 2, 4, 0, 8), ('cubic', 1, 6, 1.5, 4,1.5,0), ('line', 1.5, -8), ('move', 1.5, 0)],

    "f_t": [('quadratic', 2, 2, 0, 4), ('cubic', 2, 2, 0, 2, 2, 0), ('quadratic', 3, -1, 3, -2), ('line', 3, -4), ('line', 3, 0)],
    "f_d": [('quadratic', 2, 2, 0, 4), ('cubic', 2, 2, 0, 2, 2, 0), ('quadratic', 3, -1, 3, -2), ('line', 3, -8), ('line', 3, 0)],
    "v_t": [('quadratic', 2, 4, 0, 8), ('cubic', 2, 4, 0, 4, 2, 0), ('quadratic', 3, -2, 3, -3), ('line', 3, -4), ('line', 3, 0)],
    "v_d": [('quadratic', 2, 4, 0, 8), ('cubic', 2, 4, 0, 4, 2, 0), ('quadratic', 3, -2, 3, -3), ('line', 3, -8), ('line', 3, 0)],

    "m_s": [('cubic',1,1,1,2,0.5,2),('cubic',0,2,0,1,0,0), ('quadratic', 0, -4, 1, -4), ('quadratic', 2, -4, 2, 0)],
    "m_z": [('cubic',1,1,1,2,0.5,2),('cubic',0,2,0,1,0,0), ('quadratic', 0, -8, 1, -8), ('quadratic', 2, -8, 2, 0)],

    "s_m": [('quadratic', 0, -4, 1, -4), ('quadratic', 2, -4, 2, 0), ('cubic', 2, 1, 2, 2, 1.5, 2), ('cubic', 1, 2, 1, 1, 2, 0)],
    "z_m": [('quadratic', 0, -8, 1, -8), ('quadratic', 2, -8, 2, 0), ('cubic', 2, 1, 2, 2, 1.5, 2), ('cubic', 1, 2, 1, 1, 2, 0)]
}

def keep_some_y_w(in_string):
    return in_string.replace('wu','uWu').replace('ji','ɪYɪ').replace('iɪŋ','ɪɪYɪŋ').replace('iiŋ','ɪYɪŋ')

def grafoni_spell(string):
    ipa_string = ipa.convert(string)
    ipa_string = keep_some_y_w(ipa_string)
    out = []
    for letter in ipa_string:
        if letter in convert_dict:
            out += convert_dict[letter]
        else:
            out += [letter]
    return out

def process_ends(in_grafoni):
    in_grafoni = [" "] + in_grafoni + [" "]
    out_grafoni = []
    for i in range(len(in_grafoni)-2):
        # beginning
        l, m, r = in_grafoni[i:i+3]
        if l in [" ",",",".","-",";",":"] and (m in ["k","g","t","d","p","b","h","x"]):
            m += "-beg"
        if l in [" ",",",".","-",";",":"] and m in ["th","dh"] and not r in ["uv1","uv2","uv3","mv1","mv2","mv3"]:
            m += "-beg"
        if l in [" ",",",".","-",";",":"] and m in ["f","v"] and not r in ["uv1","uv2","uv3"]:
            m += "-beg"
        # ending
        if r in [" ",",",".","-",";",":"] and m in ["p","b","h","x","th","dh","f","v"]:
            m += "-end"
        if r in [" ",",",".","-",";",":"] and m in ["t","d"] and not l in ["lv1","lv2","lv3","mv1","mv2","mv3"]:
            m += "-end"
        if r in [" ",",",".","-",";",":"] and m in ["k","g"] and not l in ["lv1","lv2","lv3"]:
            m += "-end"
        out_grafoni.append(m)
    return out_grafoni

# change last curve to be a little longer, and flat.  do nothing with negatives, but do something with non-negatives, including zero
def r_extend(strokes,length=1):
    strokes = strokes.copy()
    if length < 0:
        return strokes
    s = strokes[-1]
    if s[0] == 'move':
        strokes[-1] = ('move',s[1]+length,s[2])
    if s[0] == 'line':
        strokes[-1] = ('quadratic',s[1],s[2],s[1]+length,s[2])
    if s[0] == 'quadratic':
        strokes[-1] = ('cubic',s[1],s[2],s[3],s[4],s[3]+length,s[4])
    if s[0] == 'cubic':
        strokes[-1] = ('cubic',s[1],s[2],s[3],s[6],s[5]+length,s[6]) #note I kinda just flatten the end
    return strokes

# change first curve to be a little longer and flat, translate the rest
# assumes you start at 0,0 (as all should)
def l_extend(strokes,length = 1):
    strokes = strokes.copy()
    if length < 0:
        return strokes
    s = strokes[0]
    if s[0] == 'move':
        strokes[0] = ('move',s[1]+length,s[2])
    if s[0] == 'line':
        strokes[0] = ('quadratic',length,0,s[1]+length,s[2])
    if s[0] == 'quadratic':
        strokes[0] = ('cubic',length,0,s[1]+length,s[2],s[3]+length,s[4])
    if s[0] == 'cubic':
        strokes[0] = ('cubic',s[1]+length,0,s[3]+length,s[4],s[5]+length,s[6]) #note I kinda just flatten the end
    return [strokes[0]] + translate(strokes[1:],length,0)

def make_ligatures(in_list):
    out = []
    last = "None"
    for c in in_list:
        potential = last + "_" + c
        if potential in ligatures:
            out.append(potential) 
            last = "None"
        else:
            if last != "None":
                out.append(last)
            last = c
    if last != "None":
        out.append(last)
    return out

def first(string):
    parts = string.split("_")
    if len(parts) == 0:
        return " "
    else:
        return parts[0]

def last(string):
    parts = string.split("_")
    if len(parts) == 0:
        return " "
    else:
        return parts[-1]

def v_nudge(paths,nudge_size = 0.1):
    if nudge_size < 0:
        return paths
    paths = paths.copy()
    last = paths[-1]
    paths+=[('quadratic',last[-2]+nudge_size,last[-1],last[-2]+nudge_size,last[-1]+nudge_size),('line',last[-2]+nudge_size,last[-1])]
    return paths

nudge_kern = defaultdict(lambda:-1)
nudge_kern[('mv1','mv1')] = 1
nudge_kern[('mv2','mv1')] = 1
nudge_kern[('mv3','mv1')] = 1
nudge_kern[('mv1','mv2')] = 1
nudge_kern[('mv2','mv2')] = 1
nudge_kern[('mv3','mv2')] = 1
nudge_kern[('mv1','mv3')] = 1
nudge_kern[('mv2','mv3')] = 1
nudge_kern[('mv3','mv3')] = 1

def to_list(in_string):
    return make_ligatures(process_ends(grafoni_spell(in_string)))

def to_svg(in_string,wrap = 100,shear_val=-1/sqrt(3),line_space=20,v_scale=0.5):
    chars = in_string
    if isinstance(chars, str):
        chars = to_list(in_string)
    #print(" ".join(chars))
    out = [('move',0,0)]
    last_char = " "
    for l in chars:
        if l in letter_forms:
            l_kern,r_kern = kerning[(last(last_char),first(l))]
            n_val = nudge_kern[(last(last_char),first(l))]
            last_char = l
            out = concat(v_nudge(r_extend(out,l_kern),n_val),l_extend(letter_forms[l],r_kern))
        elif l in ligatures:
            l_kern,r_kern = kerning[(last(last_char),first(l))]
            n_val = nudge_kern[(last(last_char),first(l))]
            last_char = l
            out = concat(v_nudge(r_extend(out,l_kern),n_val),l_extend(ligatures[l],r_kern))
        else:
            print("Unsupported Character: " + l)
        if last_char == " "  and out[-1][-2] + shear_val*v_scale*out[-1][-1] > wrap:
            out.append(('move',-shear_val*v_scale*(out[-1][-1]+line_space),out[-1][-1]+line_space))
    return display(svgStrokes(shear(scale(out,1,v_scale),by=shear_val)))

def bounding_box(strokes):
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0
    for stroke in strokes:
        if stroke[0] == 'move':
            min_x = min(min_x,stroke[1])
            min_y = min(min_y,stroke[2])
            max_x = max(max_x,stroke[1])
            max_y = max(max_y,stroke[2])
        if stroke[0] == 'line':
            min_x = min(min_x,stroke[1])
            min_y = min(min_y,stroke[2])
            max_x = max(max_x,stroke[1])
            max_y = max(max_y,stroke[2])
        if stroke[0] == 'quadratic':
            min_x = min(min_x,stroke[1],stroke[3])
            min_y = min(min_y,stroke[2],stroke[4])
            max_x = max(max_x,stroke[1],stroke[3])
            max_y = max(max_y,stroke[2],stroke[4])
        if stroke[0] == 'cubic':
            min_x = min(min_x,stroke[1],stroke[3],stroke[5])
            min_y = min(min_y,stroke[2],stroke[4],stroke[6])
            max_x = max(max_x,stroke[1],stroke[3],stroke[5])
            max_y = max(max_y,stroke[2],stroke[4],stroke[6])
    return min_x, min_y, max_x, max_y

def svgStrokes(strokes, scale = 4,padding = 1, stroke_width = 1.0/3):
    path = draw.Path(stroke='black', fill='none', stroke_width = stroke_width*scale, stroke_linecap='round', stroke_linejoin='round')
    min_x,min_y,max_x,max_y = bounding_box(strokes)
    for stroke in strokes:
        if stroke[0] == 'move':
            path.M(scale*(stroke[1]-min_x)+scale*padding,scale*(stroke[2]-min_y)+scale*padding)
        if stroke[0] == 'line':
            path.L(scale*(stroke[1]-min_x)+scale*padding,scale*(stroke[2]-min_y)+scale*padding)
        if stroke[0] == 'quadratic':
            path.Q(scale*(stroke[1]-min_x)+scale*padding,scale*(stroke[2]-min_y)+scale*padding,scale*(stroke[3]-min_x)+scale*padding,scale*(stroke[4]-min_y)+scale*padding)
        if stroke[0] == 'cubic':
            path.C(scale*(stroke[1]-min_x)+scale*padding,scale*(stroke[2]-min_y)+scale*padding,scale*(stroke[3]-min_x)+scale*padding,scale*(stroke[4]-min_y)+scale*padding,scale*(stroke[5]-min_x)+scale*padding,scale*(stroke[6]-min_y)+scale*padding)
    
    d = draw.Drawing(scale*(max_x-min_x)+2*scale*padding,scale*(max_y-min_y)+2*scale*padding)
    d.append(draw.Use(path,0,0))
    return d

def translate(strokes,dx,dy):
    out = []
    for s in strokes:
        if s[0] == 'move':
            out.append(('move',s[1]+dx,s[2]+dy))
        if s[0] == 'line':
            out.append(('line',s[1]+dx,s[2]+dy))
        if s[0] == 'quadratic':
            out.append(('quadratic',s[1]+dx,s[2]+dy,s[3]+dx,s[4]+dy))
        if s[0] == 'cubic':
            out.append(('cubic',s[1]+dx,s[2]+dy,s[3]+dx,s[4]+dy,s[5]+dx,s[6]+dy))
    return out

def scale(strokes,dx,dy):
    out = []
    for s in strokes:
        if s[0] == 'move':
            out.append(('move',s[1]*dx,s[2]*dy))
        if s[0] == 'line':
            out.append(('line',s[1]*dx,s[2]*dy))
        if s[0] == 'quadratic':
            out.append(('quadratic',s[1]*dx,s[2]*dy,s[3]*dx,s[4]*dy))
        if s[0] == 'cubic':
            out.append(('cubic',s[1]*dx,s[2]*dy,s[3]*dx,s[4]*dy,s[5]*dx,s[6]*dy))
    return out

def concat(strokes, new):
    last_x, last_y = strokes[-1][-2:]
    return strokes + translate(new,last_x,last_y)

def shear(strokes,by=-1):
    out = []
    for s in strokes:
        if s[0] == 'move':
            out.append(('move',s[1]+by*s[2],s[2]))
        if s[0] == 'line':
            out.append(('line',s[1]+by*s[2],s[2]))
        if s[0] == 'quadratic':
            out.append(('quadratic',s[1]+by*s[2],s[2],s[3]+by*s[4],s[4]))
        if s[0] == 'cubic':
            out.append(('cubic',s[1]+by*s[2],s[2],s[3]+by*s[4],s[4],s[5]+by*s[6],s[6]))
    return out