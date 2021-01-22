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
    ('status', 1),
    ('published', 1),
    ('archived', 1),
    ('last_update', 1),
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
    ('G_min_read_len', 1),
    ('T_min_read_len', 1),
    ('M_short_min_read_len', 1),
    ('M_long_min_read_len', 1),
    ('M_short_max_hits', 1),
    ('M_long_max_hits', 1),
    ('G_mismatches', 1),
    ('T_mismatches', 1),
    ('M_short_mismatches', 1),
    ('M_long_mismatches', 1),
    ('status', 1),
    ('last_update', 1),
    ('published', 1),
    ('archived', 1),
    ('_sa_instance_state', 0),
    ('parameters', 0),
    ('timestamp', 0),
    ('version', 0),
])

print_fields_results = OrderedDict([
    ('mapping_id', 0),
    ('type', 1),
    ('result_filename', 1),
    ('filesize', 1),
    ('status', 1),
    ('last_update', 0),
    ('published', 0),
    ('archived', 0),
    ('mapping', 0),
    ('_sa_instance_state', 0),
    ('analyses', 0),
    ('timestamp', 0),
    ('uploaded', 0),
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


def add_server_URL(d, f):
    if f.endswith('_filename'):
        return "http://icount.biolab.si/" + d[f]
    return str(d[f])


# mapping from protein to experiment
protein2exp = {}

def process_all():
    # libraries_get, library_get(lib_id)
    # experiments_get, experiment_get(lib_id, exp_id)
    # mapping_get_for_lib_id_exp_id(lib_id, exp_id)
    # results_get_for_mapid(map_id)
    # analyses_get, analysis_get(aid)
    ret_json = OrderedDict()
    exps = db.experiments_get()
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
                    rec_annot[f] = add_server_URL(m.__dict__, f)
            exp_maps[str(m.id)]['Annotation'] = rec_annot

            rec_ress = []
            for r in db.results_get_for_mapid(m.id):
                if not r.published:
                    continue
                rec_res = OrderedDict()
                for f, v in print_fields_results.items():
                    if v:
                        rec_res[f] = add_server_URL(r.__dict__, f)
                rec_ress.append(rec_res)
            if not rec_ress:
                continue
            exp_maps[str(m.id)]['Results'] = rec_ress
        if not exp_maps:
            continue
        exp_data['Mappings'] = exp_maps
        k = str(e.lib_id) + "_" + str(e.exp_id)
        ret_json[k] = exp_data
        protein2exp.setdefault(e.protein, []).append(k)

    fout = open('exp2res.json', 'wt')
    fout.write(json.dumps(ret_json, indent=4))
    fout.close()

    fout = open('prot2exp.json', 'wt')
    fout.write(json.dumps(protein2exp, indent=4, sort_keys=True))
    fout.close()


if __name__ == "__main__":
    process_all()
