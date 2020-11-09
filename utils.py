from time import strftime

def rules_to_str(rules):
    rule_str = ""
    for bin in range(len(rules)):
        rule_str += "bin:".format(bin)
        for prop_ind, prop_vals in enumerate(rules[bin]):
            rule_str += "prop-{}".format(prop_vals)
    return (rule_str)


def str_to_rules(rule_str):
    bin_strs = rule_str.split("bin:")
    rules = []
    for bin_ind, bin_str in enumerate(bin_strs[1:]):
        prop_strs = bin_str.split("prop-")
        rules.append([])
        for prop_str in prop_strs[1:]:
            tmp_strs = prop_str.replace('[', '').replace(']',
                                                         '').replace("'", '')
            rules[bin_ind].append(tmp_strs.split(', '))
    return rules

def get_user_index(id, time):
    return(str(id) + '---' + strftime("%a, %d %b %Y %H:%M:%S +0000",time))

def from_index(index):
    return None