import csv
import string
import re


def root1(name):
    name = name.upper()
    name = name.replace(' ', '')  # remove space
    name = name.replace('.', '')  # remove dot *
    name = re.sub(u"\\(.*?\\)", "", name)  # remove brackets and its content
    name = name.rstrip(string.digits)  # *

    if name.find("-") >= 0:
        if not name[name.find("-") + 1:len(name)].isalpha() or len(name[name.find("-") + 1:len(name)]) < len(
                name[0:name.find("-")]):
            name = name[0:name.find("-")]
        if name.find("-") < 2:
            name = name[name.find("-") + 1:len(name)]
    return name


def root2(name):
    return name.replace("-", "")


def matching_name(truth_name, name):
    if root1(truth_name) == root1(name) or root2(root1(truth_name)) == root2(root1(name)):
        return True
    else:
        return False


def write_plus(outputs, wfile, wlist):
    with open(wfile, 'w', newline='', encoding="utf-8") as newfile:
        filewriter = csv.DictWriter(newfile, fieldnames=wlist)
        filewriter.writeheader()  # 写入列名
        filewriter.writerows(outputs)


def matching(file_truth, file_validation, fig_name1, fig_name2, gene_name1, gene_name2, wfile, wlist):
    match_name = ""
    with open(file_truth, 'r', encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile)
        truth = [row for row in reader]
    with open(file_validation, 'r', encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile)
        outputs = [row for row in reader]
    for row2 in outputs:
        temp_list = list()
        flag = 0
        fig = row2[fig_name2]
        for row1 in truth:
            if row1[fig_name1] == fig:
                temp_list.append(row1[gene_name1])  # in same fig
        for name in temp_list:
            # add IOU in here
            if matching_name(name, row2[gene_name2]):
                match_name = name
                flag = 1  # Successful match
                break
        if flag == 1:
            row2.update({"evaluation": "TP", "match_name": match_name})
        else:
            row2.update({"evaluation": "FP", "match_name": "None"})
    write_plus(outputs, wfile, wlist)

    f1 = "csv/finalized_genes.csv"
    # f2 = "csv/validation model outputs elements.csv"
    # figname1 = "fig_name"
    # figname2 = "fige_name"
    # genename1 = "annotated_gene_name"
    # genename2 = "gene_name"
    # wfile = "plus/validation model outputs elements plus.csv"
    # wlist = ["", "coordinates", "gene_name", "fige_name", "evaluation","match_name"]

