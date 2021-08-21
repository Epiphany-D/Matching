import Matching_elements as mc
import os


def matching(file_truth, file_predict, wfile, wlist, relation):
    TP_num, FP_num = 0, 0
    writelist = list()
    truth, predict = mc.read_file(file_truth, file_predict=file_predict)
    for pt in predict:
        if pt["category_id"] == relation:
            del_flag = False
            startor_list, receptor_list = list("#"), list("#")
            fig = pt["file_name"]
            for th in truth:
                if th["relation_type"] == relation and th["fig_name"] == fig:
                    startor_list.append(th["activator"])
                    receptor_list.append(th["receptor"])  # in same fig
            # TODO:: Add IOU here
            flag_s, match_name_s = mc.check_flag(pt["startor"], startor_list)
            flag_r, match_name_r = mc.check_flag(pt["receptor"], receptor_list)
            if flag_s == 2 or flag_r == 2:
                del_flag = True
            if del_flag:
                pt.update({"evaluation": "DELETE", "match_name_startor": "DELETE",
                           "match_name_receptor": "DELETE"})
            else:
                pt.update({"evaluation": "FP"})
                FP_num += 1
                if flag_s:
                    pt.update({"match_name_startor": match_name_s})
                else:
                    pt.update({"match_name_startor": "None"})
                if flag_r:
                    pt.update({"match_name_receptor": match_name_r})
                else:
                    pt.update({"match_name_receptor": "None"})
                if flag_r and flag_s:
                    pt.update({"evaluation": "TP"})
                    FP_num -= 1
                    TP_num += 1
            writelist.append(pt)
    mc.write_plus(writelist, wfile, wlist)
    return TP_num, FP_num


if __name__ == "__main__":
    f1 = "csv/finalized_relations.csv"
    f2 = "csv/test.csv"
    wlist = ["category_id", "bbox", "startor", "receptor", "file_name", "evaluation", "match_name_startor",
             "match_name_receptor"
             ]
    wfile = f2.replace("csv", "plus").replace(".plus", " plus.csv")
    try:
        os.remove(wfile)
    except:
        pass
    for relation in ["activate_relation", "inhibit_relation"]:
        tp, fp = matching(f1, f2, wfile, wlist, relation)
        if relation == "activate_relation":
            tmp = 158
        else:
            tmp = 38
        fn = tmp - tp  # version1 truth
        mc.printout(wfile, tp, fn, fp, relation)
        print("----------")
