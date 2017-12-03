import simplejson as json
import os

import map_based_prep_dat as MaPPD

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def main(js, team1, team2):
    with open("file_index.json", 'r') as f:
        index_json = json.load(f)
    player_number = index_json["PPN"]["line_num"]

    team1p = ["0"]*player_number
    MaPPD.find_players(js, team=team1, teamp=team1p)
    team2p = ["0"]*player_number
    MaPPD.find_players(js, team=team2, teamp=team2p)

    if team1p.count("1") == 0 or team2p.count("1") == 0:
        return

    line_data = ""
    line_data_2 = ""
    out = ""
    out2 = ""
    format = js["GameFormat"].split()[-1]
    sk1, sk2 = js[team1]["Score BO"], js[team2]["Score BO"],
    if sk1 >= sk2:
        out = "1"
        out2 = "0"
    elif sk1 < sk2:
        out = "0"
        out2 = "1"
    if sk1 is None or sk2 is None:
        return
    line_data += format + " " + " ".join(team1p) + " " + " ".join(team2p)
    line_data_2 += format + " " + " ".join(team2p) + " " + " ".join(team1p)
    with open(os.path.abspath("..")+os.sep+"NN"+os.sep+"match_based"+os.sep+"match_prepared.dat", 'a+') as f:
        f.write(line_data + '\n')
        f.write(line_data_2 + '\n')
    with open(os.path.abspath("..")+os.sep+"NN"+os.sep+"match_based"+os.sep+"match_out_prepared.dat", 'a+') as f:
        f.write(out + '\n')
        f.write(out2 + '\n')

def x(lower=0, upper=0):
    num_of_matches = 0
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith(".json"):
                print os.path.join(root, file)
                if "_+_" not in os.path.join(root, file) or num_of_matches < lower:
                    num_of_matches += 1
                    continue
                with open(os.path.join(root, file), 'r') as f:
                    js=json.load(f)
                    team1, team2 = js["FileName"].split("_+_")[1], js["FileName"].split("_+_")[2]
                    main(js, team1.replace('%20', ' '), team2.replace('%20', ' ', ))
                    num_of_matches += 1
                    if (num_of_matches >= upper):
                        return
if __name__ == "__main__":
    x()
