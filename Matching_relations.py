import Matching_elements as mc


def matching(file_truth, file_2, wfile, wlist):
    TP_num, FP_num = 0, 0
    truth, outputs = mc.read_file(file_truth, file_validation=file_2)
    for row2 in outputs:
        startor_list, receptor_list, category_id_list = list(), list(), list()
        flag_c = False
        fig = row2["file_name"]
        for row1 in truth:
            if row1["fig_name"] == fig:
                startor_list.append(row1["activator"])
                receptor_list.append(row1["receptor"])
                category_id_list.append(row1["relation_type"])  # in same fig
        # TODO:: Add IOU here
        flag_s, match_name_s = mc.check_flag(row2["startor"], startor_list)
        flag_r, match_name_r = mc.check_flag(row2["receptor"], receptor_list)
        for category_id in category_id_list:
            if row2["category_id"] == category_id:
                flag_c = True
        if flag_s == 2 or flag_r == 2:
            row2.update({"evaluation": "DELETE", "match_name_startor": "DELETE",
                         "match_name_receptor": "DELETE"})
            continue
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
    mc.write_plus(outputs, wfile, wlist)
    return TP_num, FP_num


if __name__ == "__main__":
    f1 = "csv/finalized_relations.csv"
    f2_list = ["csv/by_article_relation.csv", "csv/by_both_relation.csv", "csv/by_dict_relation.csv",
               "csv/raw_relation.csv", "csv/validation model outputs relation.csv"]
    wlist = ["category_id", "bbox", "startor", "receptor", "file_name", "evaluation", "match_name_startor",
             "match_name_receptor"
             ]
    for f2 in f2_list:
        wfile = f2.replace("csv", "plus").replace(".plus", " plus.csv")
        tp, fp = matching(f1, f2, wfile, wlist)
        fn = 196 - tp  # version1 truth
        mc.printout(wfile, tp, fn, fp)
        print("----------")
