import json

data = json.load(open("../data/exp2res.json"))
for exp_id, exp_data in data.items():
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


data = json.load(open("../data/analysis.json"))
for ana_id, ana_data in data.items():
    # write experiment html file
    code = """
---
title: {ana_id}
linkTitle: {ana_id}
type: "page"
analysis: "{ana_id}"
type: "analysis"
---
""".format(ana_id=ana_id)
    f = open("../content/analysis/%s.html" % ana_id, "wt")
    f.write(code)
    f.close()
