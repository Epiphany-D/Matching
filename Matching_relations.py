import csv
from Matching_elements import matching_name, write_plus


def matching(file_truth, file_2, wfile, wlist):
    TP_num, FP_num = 0, 0
    match_name_s, match_name_r = "", ""
    with open(file_truth, 'r', encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile)
        truth = [row for row in reader]
    with open(file_2, 'r', encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile)
        outputs = [row for row in reader]
    for row2 in outputs:
        startor_list, receptor_list, category_id_list = list(), list(), list()
        flag_s, flag_r, flag_c = False, False, False
        fig = row2["file_name"]
        for row1 in truth:
            if row1["fig_name"] == fig:
                startor_list.append(row1["activator"])  # in same fig
                receptor_list.append(row1["receptor"])
                category_id_list.append(row1["relation_type"])
        for name in startor_list:
            if matching_name(name, row2["startor"]):
                match_name_s = name
                flag_s = True  # Successful match s
                break
        for name in receptor_list:
            if matching_name(name, row2["receptor"]):
                match_name_r = name
                flag_r = True
                break
        for category_id in category_id_list:
            if row2["category_id"] == category_id:
                flag_c = True
        row2.update({"evaluation": "FP"})
        FP_num += 1
        if flag_s:
            row2.update({"match_name_startor": match_name_s})
        else:
            row2.update({"match_name_startor": "None"})
        if flag_r:
            row2.update({"match_name_receptor": match_name_r})
        else:
            row2.update({"match_name_receptor": "None"})
        if flag_r and flag_s and flag_c:
            row2.update({"evaluation": "TP"})
            FP_num -= 1
            TP_num += 1
    write_plus(outputs, wfile, wlist)
    return TP_num, FP_num


f1 = "csv/finalized_relations.csv"
f2 = "csv/validation model outputs relation.csv"
wfile = "plus/validation model outputs relation plus.csv"
wlist = ["category_id", "bbox", "startor", "receptor", "file_name", "evaluation", "match_name_startor",
         "match_name_receptor"
         ]

tp, fp = matching(f1, f2, wfile, wlist)

fn = 193 - tp

PRECISION = tp / (tp + fp)
RECALL = tp / (tp + fn)
print("TP = {}, FN = {}, FP = {}".format(tp, fn, fp))
print("PRECISION = {0:.4f}".format(PRECISION))
print("RECALL = {0:.4f}".format(RECALL))
