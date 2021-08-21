import csv
import re
import string


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def root1(name):
    name = name.upper()
    name = name.replace(' ', '')  # remove space
    name = name.replace('.', '')  # remove dot *
    name = re.sub(u"\\(.*?\\)", "", name)  # remove brackets and its content
    name = name.replace('(', "").replace(')', "")
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
    rt_truth_name = root1(truth_name)
    rt_match_name = root1(name)
    if len(name.strip()) <= 1 or len(name.strip()) > 7:  # delete single letter and too long name
        return "None"
    if is_number(root2(name)):  # delete name only has numbers
        return "None"
    if rt_match_name == rt_truth_name or root2(rt_match_name) == root2(rt_truth_name):
        return "OK"
    else:
        return "WRONG"


def write_plus(outputs, wfile, wlist):
    with open(wfile, 'a', newline='', encoding="utf-8") as newfile:
        filewriter = csv.DictWriter(newfile, fieldnames=wlist)
        filewriter.writeheader()  # 写入列名
        filewriter.writerows(outputs)


def check_flag(e_name, temp_list):
    flag = 0
    match_name = ""
    for name in temp_list:
        # add IOU in here
        tmp = matching_name(name, e_name)
        if tmp == "OK":
            match_name = name
            flag = 1  # Successful match
            break
        elif tmp == "None":
            flag = 2
            continue
        elif tmp == "WRONG":
            flag = 0
            continue
    return flag, match_name


def read_file(file_truth, file_predict):
    with open(file_truth, 'r', encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile)
        truth = [row for row in reader]
    with open(file_predict, 'r', encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile)
        outputs = [row for row in reader]
    return truth, outputs


def matching(file_truth, file_predict, fig_name1, fig_name2, gene_name1, gene_name2, wfile, wlist):
    TP_num, FP_num = 0, 0
    truth, predict = read_file(file_truth, file_predict)
    for pt in predict:
        temp_list = list()
        fig = pt[fig_name2]
        for th in truth:
            if th[fig_name1] == fig:
                temp_list.append(th[gene_name1])  # in same fig
        # TODO:: add IOU here
        flag, match_name = check_flag(pt[gene_name2], temp_list)
        if flag == 2:
            pt.update({"evaluation": "DELETE", "match_name": "DELETE"})
            continue
        elif flag == 1:
            pt.update({"evaluation": "TP", "match_name": match_name})
            TP_num += 1
        else:
            pt.update({"evaluation": "FP", "match_name": "None"})
            FP_num += 1
    write_plus(predict, wfile, wlist)
    return TP_num, FP_num


def printout(output_file, TP, FN, FP, relation=""):
    PRECISION = TP / (TP + FP)
    RECALL = TP / (TP + FN)
    if relation != "":
        relation = ' : ' + relation
    print(output_file.replace("plus/", "").replace(".csv", "").title() + relation)
    print("TP = {}, FN = {}, FP = {}".format(TP, FN, FP))
    print("PRECISION = {0:.4f}".format(PRECISION))
    print("RECALL = {0:.4f}".format(RECALL))


if __name__ == "__main__":
    f1 = "csv/finalized_genes.csv"
    f2_list = ["csv/by_article_elements.csv", "csv/by_both_elements.csv", "csv/by_dict_elements.csv",
               "csv/raw_elements.csv", "csv/validation model outputs elements.csv"]
    figname1 = "fig_name"
    figname2 = "fig_name"
    genename1 = "annotated_gene_name"
    genename2 = "gene_name"
    wlist = ["coordinates", "gene_name", "fig_name", "evaluation", "match_name"]
    for f2 in f2_list:
        wfile = f2.replace("csv", "plus").replace(".plus", " plus.csv")
        tp, fp = matching(f1, f2, figname1, figname2, genename1, genename2, wfile, wlist)
        fn = 315 - tp  # version1 truth
        printout(wfile, tp, fn, fp)
        print("----------")
