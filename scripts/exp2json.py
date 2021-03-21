"""
Old iCount data export.

Needs a running instance of old iCount. Generates two json files:
- http://icount.biolab.si/exp2res.json: data on all experiments, mappings, and associated results
- http://icount.biolab.si/prot2exp.json: mapping from protein to list of experiments

Runs in python 2.6.5 and requires ordereddict 1.1: https://pypi.org/project/ordereddict/#files
"""

import gzip
import json

import iCount
import db

from ordereddict import OrderedDict

print_fields_experiment = OrderedDict([
    ('lib_id', 1),
    ('exp_id', 1),
    ('protein', 1),
    ('method', 1),
    ('replicate', 1),
    ('tissue', 1),
    ('condition', 1),
    ('species', 1),
    ('bar5', 1),
    ('bar3', 1),
    ('bar5_rnd', 1),
    ('bar_tail_to_remove', 1),
    ('notes', 1),
    ('fq_filename', 1),
    ('filesize', 1),
    ('status', 0),
    ('published', 0),
    ('archived', 0),
    ('last_update', 0),
    ('collaborator', 0),
    ('timestamp', 0),
    ('_sa_instance_state', 0),
])

print_fields_mapping = OrderedDict([
    ('id', 1),
    ('lib_id', 1),
    ('exp_id', 1),
    ('group_name', 1),
    ('mapped_to', 1),
    ('regions', 1),
    ('annotation_version', 1),
    ('G_min_read_len', 0),
    ('T_min_read_len', 0),
    ('M_short_min_read_len', 0),
    ('M_long_min_read_len', 0),
    ('M_short_max_hits', 0),
    ('M_long_max_hits', 0),
    ('G_mismatches', 0),
    ('T_mismatches', 0),
    ('M_short_mismatches', 0),
    ('M_long_mismatches', 0),
    ('status', 0),
    ('last_update', 1),
    ('published', 0),
    ('archived', 0),
    ('_sa_instance_state', 0),
    ('parameters', 1),
    ('timestamp', 0),
    ('version', 0),
])

print_fields_results = OrderedDict([
    ('mapping_id', 0),
    ('type', 1),
    ('result_filename', 1),
    ('filesize', 1),
    ('status', 0),
    ('last_update', 0),
    ('published', 0),
    ('archived', 0),
    ('mapping', 0),
    ('_sa_instance_state', 0),
    ('analyses', 0),
    ('timestamp', 0),
    ('uploaded', 0),
])

print_fields_analysis = OrderedDict([
    ('creation_date', 1),
    ('creator', 0),
    ('id', 1),
    ('inputs', 1), # of type results
    ('note', 1),
    ('outputs', 1), # of type analysisresult
    ('parameters', 1), # of type analysisparameters
    ('prev_inputs', 1),
    ('_sa_instance_state', 0),
    ('archived', 0),
    ('last_update', 0),
    ('published', 0),
    ('status', 0),
    ('timestamp', 0),
    ('type', 1)
])

print_fields_analysisinput = OrderedDict([
    ('mapping_id', 0),
    ('type', 1),
    ('result_filename', 1),
    ('filesize', 1),
    ('status', 0),
    ('last_update', 0),
    ('published', 0),
    ('archived', 0),
    ('mapping', 0),
    ('_sa_instance_state', 0),
    ('timestamp', 0),
    ('uploaded', 0),
])

print_fields_analysisresult = OrderedDict([
    ('_sa_instance_state', 0),
    ('analysis_id', 0),
    ('type', 1),
    ('filename', 1),
    ('filesize', 1),
    ('next_analyses', 0),
    ('id', 0),
])

print_fields_analysisresultparameters = OrderedDict([
    ('_sa_instance_state', 0),
    ('analysis_id', 0),
    ('name', 1),
    ('value', 1),
    ('timestamp', 0),
])

# check if all fields are registered
exps = db.experiments_get()
e = exps[0]
e_keys = e.__dict__.keys()
if set(e_keys) <> set(print_fields_experiment):
    print "Not all experiment fields registered, missing:", sorted(set(e_keys)-set(print_fields_experiment))
    exit(1)

maps = db.mapping_get_for_lib_id_exp_id(e.lib_id, e.exp_id)
m = maps[0]
m_keys = m.__dict__.keys()
if set(m_keys) <> set(print_fields_mapping):
    print "Not all mapping fields registered, missing:", sorted(set(m_keys)-set(print_fields_mapping))
    exit(1)

res = db.results_get_for_mapid(m.id)
r = res[0]
r_keys = r.__dict__.keys()
if set(r_keys) <> set(print_fields_results):
    print "Not all results fields registered, missing:", sorted(set(r_keys)-set(print_fields_results))
    exit(1)

anas = db.analyses_get('compare')
a = anas[0]
a_keys = a.__dict__.keys()
if set(a_keys) <> set(print_fields_analysis):
    print "Not all analysis fields registered, missing:", sorted(set(a_keys)-set(print_fields_analysis))
    exit(1)

a = db.analysis_get(a.id)
ai_keys = a.inputs[0].__dict__.keys()
if set(ai_keys) <> set(print_fields_analysisinput):
    print set(ai_keys)
    print set(print_fields_analysisinput)
    print "Not all analysis inputs fields registered, missing:", sorted(set(ai_keys)-set(print_fields_analysisinput))
    exit(1)

ar_keys = a.outputs[0].__dict__.keys()
if set(ar_keys) <> set(print_fields_analysisresult):
    print "Not all analysis results fields registered, missing:", sorted(set(ar_keys)-set(print_fields_analysisresult))
    exit(1)

ap_keys = a.parameters[0].__dict__.keys()
if set(ap_keys) <> set(print_fields_analysisresultparameters):
    print "Not all analysis parameters fields registered, missing:", sorted(set(ap_keys)-set(print_fields_analysisresultparameters))
    exit(1)


def add_server_URL(d, f):
    if f == 'filename' or f.endswith('_filename'):
        return "http://icount.biolab.si/" + d[f]
    return str(d[f])


def comp2dict(lst):
    ret_d = OrderedDict()
    for k, v in lst:
        ret_d.setdefault(k, []).append(v)
    return ret_d


def process_all():
    # libraries_get, library_get(lib_id)
    # experiments_get, experiment_get(lib_id, exp_id)
    # mapping_get_for_lib_id_exp_id(lib_id, exp_id)
    # results_get_for_mapid(map_id)
    # analyses_get, analysis_get(aid)


    # mapping from protein to experiment
    protein2exp = {}

    # mapping from experiment to annotation, mappings (annotation, results, analyses)
    ret_json = OrderedDict()

    # mapping from analysis id to analysis details

    exps = db.experiments_get()
    anas = set()
    print(len(exps))
    for e in exps:
        if not e.published:
            continue
        exp_data = OrderedDict({'Annotation': {}, 'Mappings': []})
        rec = OrderedDict()
        for f, v in print_fields_experiment.items():
            if v:
                rec[f] = add_server_URL(e.__dict__, f)
        exp_data['Annotation'] = rec

        exp_maps = {}
        for m in db.mapping_get_for_lib_id_exp_id(e.lib_id, e.exp_id):
            if not m.published:
                continue
            exp_maps[str(m.id)] = OrderedDict()
            rec_annot = OrderedDict()
            for f, v in print_fields_mapping.items():
                if v:
                    if f == 'parameters':
                        rec_annot[f] = eval(m.__dict__[f])
                    else:
                        rec_annot[f] = add_server_URL(m.__dict__, f)
            exp_maps[str(m.id)]['Annotation'] = rec_annot

            ana_ids = set()
            rec_ress = []
            for r in db.results_get_for_mapid(m.id):
                if not r.published:
                    continue
                rec_res = OrderedDict()
                for f, v in print_fields_results.items():
                    if v:
                        rec_res[f] = add_server_URL(r.__dict__, f)
                rec_anas = sorted([(a.type, str(a.id)) for a in r.analyses])
                rec_res['analyses'] = comp2dict(rec_anas)
                ana_ids.update(set(rec_anas))
                anas.update(set(aid for (atype, aid) in rec_anas))

                rec_ress.append(rec_res)

            if not rec_ress:
                continue
            exp_maps[str(m.id)]['Results'] = rec_ress
            exp_maps[str(m.id)]['Analyses'] = comp2dict(sorted(ana_ids))
        if not exp_maps:
            continue
        exp_data['Mappings'] = exp_maps
        k = str(e.lib_id) + "_" + str(e.exp_id)
        ret_json[k] = exp_data
        protein2exp.setdefault(e.protein, []).append(k)

    # get all details on analysis
    ret_ana = OrderedDict()
    for aid in sorted(anas):
        rec_ana = OrderedDict()
        a = db.analysis_get(aid)
        for f, v in print_fields_analysis.items():
            if v:
                if f == 'inputs':
                    rec_lst = []
                    for aa in a.inputs:
                        rec_rec_ana = OrderedDict()
                        for f2, v2 in print_fields_analysisinput.items():
                            if v2:
                                rec_rec_ana[f2] = add_server_URL(aa.__dict__, f2)
                        rec_lst.append(rec_rec_ana)
                    rec_ana[f] = rec_lst
                elif f == 'outputs':
                    rec_lst = []
                    for aa in a.outputs:
                        rec_rec_ana = OrderedDict()
                        for f2, v2 in print_fields_analysisresult.items():
                            if v2:
                                rec_rec_ana[f2] = add_server_URL(aa.__dict__, f2)
                        rec_lst.append(rec_rec_ana)
                    rec_ana[f] = rec_lst
                elif f == 'parameters':
                    rec_lst = []
                    for aa in a.parameters:
                        rec_rec_ana = OrderedDict()
                        for f2, v2 in print_fields_analysisresultparameters.items():
                            if v2:
                                rec_rec_ana[f2] = add_server_URL(aa.__dict__, f2)
                        rec_lst.append(rec_rec_ana)
                    rec_ana[f] = rec_lst
                else:
                    rec_ana[f] = add_server_URL(a.__dict__, f)
        ret_ana[aid] = rec_ana


    fout = open('exp2res.json', 'wt')
    fout.write(json.dumps(ret_json, indent=4, sort_keys=False))
    fout.close()

    fout = open('prot2exp.json', 'wt')
    fout.write(json.dumps(protein2exp, indent=4, sort_keys=True))
    fout.close()

    fout = open('analysis.json', 'wt')
    fout.write(json.dumps(ret_ana, indent=4, sort_keys=False))
    fout.close()

if __name__ == "__main__":
    process_all()
