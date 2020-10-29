
CARD_PROPERTIES = []
for color in ['red', 'green', 'purple']:
    for shading in ['open', 'striped', 'solid']:
        for shape in ['diamond', 'oval', 'squiggle']:
            for number in ['one', 'two', 'three']:
                CARD_PROPERTIES.append((color, shading, shape, number))

CARD_ORDER = [3, 5, 6, 8, 10, 12, 34]
NUM_TRIALS = len(CARD_ORDER)

NUM_BINS = 2
RULES = [
    [['red', 'green', 'purple'], ['open', 'striped', 'solid'], ['diamond', 'oval', 'squiggle'], ['one']],
    [['red', 'green', 'purple'], ['open', 'striped', 'solid'], ['diamond', 'oval', 'squiggle'], ['two', 'three']]
]

ANSWER = []
for card in CARD_ORDER:
    bin_res = [1]*NUM_BINS
    for cur_bin in range(NUM_BINS):
        for prop in range(4):
            if not (CARD_PROPERTIES[card][prop] in RULES[cur_bin][prop]):
                bin_res[cur_bin] = 0
                break
    ANSWER.append(bin_res)





