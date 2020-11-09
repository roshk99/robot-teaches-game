DEBUG_MODE = True

CARD_PROPERTIES = []
for color in ['red', 'green', 'purple']:
    for shading in ['open', 'striped', 'solid']:
        for shape in ['diamond', 'oval', 'squiggle']:
            for number in ['one', 'two', 'three']:
                CARD_PROPERTIES.append((color, shading, shape, number))

NUM_BINS = 2
RULES = [
            [
                [['red', 'green', 'purple'], ['open', 'striped', 'solid'], ['oval', 'squiggle'], ['one']]
            ],
            [
                [['red', 'green', 'purple'], ['open', 'striped', 'solid'], ['diamond', 'oval', 'squiggle'], ['two', 'three']],
                [['red', 'green', 'purple'], ['open', 'striped', 'solid'], ['diamond'], ['one']]
            ]
        ]

CARD_ORDER = [3, 5, 6, 8, 10, 12, 34]
NUM_TRIALS = len(CARD_ORDER)
ANSWER = []
for card in CARD_ORDER:
    bin_res = [0] * NUM_BINS
    for cur_bin_num, cur_bin in enumerate(RULES):
        for rule in cur_bin:
            if bin_res[cur_bin_num] == 0:
                res = 1
                for prop_num, prop in enumerate(rule):
                    if not (CARD_PROPERTIES[card][prop_num] in prop):
                        res = 0
                if res == 1:
                    bin_res[cur_bin_num] = 1
    ANSWER.append(bin_res)

CARD_ORDER_DEMO = [10, 12, 34]
NUM_DEMOS = len(CARD_ORDER_DEMO)
ANSWER_DEMO = []
for card in CARD_ORDER_DEMO:
    bin_res = [0] * NUM_BINS
    for cur_bin_num, cur_bin in enumerate(RULES):
        for rule in cur_bin:
            if bin_res[cur_bin_num] == 0:
                res = 1
                for prop_num, prop in enumerate(rule):
                    if not (CARD_PROPERTIES[card][prop_num] in prop):
                        res = 0
                if res == 1:
                    bin_res[cur_bin_num] = 1
    ANSWER_DEMO.append(bin_res)
