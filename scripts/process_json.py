import json

data = json.load(open("../data/prot2exp.json"))
for protein, exps in data.items():
    exps_processed = []
    for exp_id in exps:
        exp_id = exp_id.replace("(", "[").replace(")", "]").replace("'", "\"")
        exp_id = json.loads(str(exp_id))
        exps_processed.append("%s_%s" % (exp_id[0].lower(), exp_id[1]))
    data[protein] = exps_processed
json.dump(data, open("../data/prot2exp_processed.json", "wt"), indent=4, sort_keys=True)


data = json.load(open("../data/exp2res.json"))
data_processed = {}
for exp_id, exp_data in data.items():
    exp_id = exp_id.replace("(", "[").replace(")", "]").replace("'", "\"")
    exp_id = json.loads(str(exp_id))
    exp_id = "%s_%s" % (exp_id[0].lower(), exp_id[1])
    data_processed[exp_id] = exp_data

    # write experiment html file
    code = """
---
title: {exp_id}
linkTitle: {exp_id}
type: "page"
experiment: "{exp_id}"
type: "experiment"
---
""".format(exp_id=exp_id)
    f = open("../content/experiments/%s.html" % exp_id, "wt")
    f.write(code)
    f.close()

json.dump(data_processed, open("../data/exp2res_processed.json", "wt"), indent=4)
