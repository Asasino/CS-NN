import simplejson as json
import os

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def find_players(js, team, teamp):
    with open("file_index.json", 'r') as f:
        index_json = json.load(f)
    player_dat_name = index_json["PPN"]["file_name"]
    if js[team]["Players"] is not None:
        with open(player_dat_name, 'r') as f:
            lines = f.readlines()
        pl = 5
        for player in js[team]["Players"]:
            found = False
            lin=""
            for line in lines:
                if player.strip() in line:
                    found=True
                    lin=line
                    break
            if found:
                if pl:
                    pl -= 1
                    teamp[int(lin.split('_+_')[1].strip())] = "1"

def find_map(map, mappoint):
    with open("file_index.json", 'r') as f:
        index_json = json.load(f)
    map_dat_name = index_json["PM"]["file_name"]
    with open(map_dat_name, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if map.lower() in line.lower():
            mappoint[int(line.strip().split('_+_')[-1])] = "1"

def main(js, team1, team2):
    with open("file_index.json", 'r') as f:
        index_json = json.load(f)
    player_number = index_json["PPN"]["line_num"]

    team1p = ["0"]*player_number
    find_players(js, team=team1, teamp=team1p)
    team2p = ["0"]*player_number
    find_players(js, team=team2, teamp=team2p)

    if team1p.count("1") == 0 or team2p.count("1") == 0:
        return

    gameformat = int(js["GameFormat"].split()[-1])
    for i in range(1, gameformat+1):
        line_data = ""
        line_data_2 = ""
        out = ""
        match = js["Match "+str(i)]
        sk1, sk2 = match[team1], match[team2]
        if sk1 >= sk2:
            out = "1"
            out2 = "0"
        elif sk1 < sk2:
            out = "0"
            out2 = "1"
        if sk1 is None or sk2 is None:
            continue
        sk1, sk2 = str(sk1), str(sk2)
        mappoint = ["0"]*12
        map = match["Map"]
        find_map(map, mappoint)
        line_data += " ".join(mappoint) + " " + str(i) + " " + " ".join(team1p) + " " + " ".join(team2p)
        line_data_2 += " ".join(mappoint) + " " + str(i) + " " +" ".join(team2p) + " " + " ".join(team1p)
        #print line_data
        with open(os.path.abspath("..")+os.sep+"NN"+os.sep+"map_based"+os.sep+"map_prepared.dat", 'a+') as f:
            f.write(line_data + '\n')
            f.write(line_data_2 + '\n')
        with open(os.path.abspath("..")+os.sep+"NN"+os.sep+"map_based"+os.sep+"map_out_prepared.dat", 'a+') as f:
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
                #print ""
if __name__ == "__main__":
    x()
