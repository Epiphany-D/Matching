import csv
from Matching_elements import matching_name


def write_relations(outputs):
    with open('validation model outputs relation plus.csv', 'w', newline='', encoding="utf-8") as newfile:
        filewriter = csv.DictWriter(newfile, fieldnames=["", "category_id", "bbox", "startor", "receptor", "file_name",
                                                         "evaluation", "match_name_startor", "match_name_receptor"])
        filewriter.writeheader()  # 写入列名
        filewriter.writerows(outputs)


def matching(file_truth, file_validation):
    match_name_s, match_name_r = "", ""
    with open(file_truth, 'r', encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile)
        truth = [row for row in reader]
    with open(file_validation, 'r', encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile)
        outputs = [row for row in reader]
    for row2 in outputs:
        startor_list, receptor_list = list(), list()
        flag_s, flag_r = 0, 0
        fig = row2["file_name"]
        for row1 in truth:
            if row1["fig_name"] == fig:
                startor_list.append(row1["activator"])  # in same fig
                receptor_list.append(row1["receptor"])
        for name in startor_list:
            if matching_name(name, row2["startor"]):
                match_name_s = name
                flag_s = 1  # Successful match s
                break
        for name in receptor_list:
            if matching_name(name, row2["receptor"]):
                match_name_r = name
                flag_r = 1
                break
        if flag_s:
            row2.update({"match_name_startor": match_name_s})
        else:
            row2.update({"evaluation": "FP", "match_name_startor": "None"})
        if flag_r:
            row2.update({"match_name_receptor": match_name_r})
        else:
            row2.update({"evaluation": "FP", "match_name_receptor": "None"})
        if flag_r and flag_s:
            row2.update({"evaluation": "TP"})
    write_relations(outputs)


f1 = "finalized_relations.csv"
f2 = "validation model outputs relation.csv"

matching(f1, f2)
