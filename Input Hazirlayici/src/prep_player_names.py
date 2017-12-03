import simplejson as json
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

FILE_NAME = "feed"+os.sep+"players.dat"

def main(js, t1, t2):
    players = ""
    added_lines = 0
    if js[t1]["Players"] is None or js[t2]["Players"] is None:
        return added_lines
    with open(FILE_NAME, 'r') as f:
        lines = f.readlines()
        #print lines
    for player in js[t1]["Players"].keys()+js[t2]["Players"].keys():
        pas = False
        for pl in lines:
            if player.strip().encode("utf-8") not in pl:
                continue
            else:
                #print " burada"
                pas = True
                break
        if not pas:
            players += player.strip() + '\n'
            added_lines += 1
    with open(FILE_NAME, 'a+') as f:
        f.write(players)
    return added_lines

def x():
    if not os.path.exists("feed"):
        os.mkdir("feed")
    with open(FILE_NAME, 'w') as f:
        pass
    line_num = 0
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith(".json"):
                print os.path.join(root, file)
                if "_+_" not in os.path.join(root, file):
                    continue
                with open(os.path.join(root, file), 'r') as f:
                    js=json.load(f)
                team1, team2 = js["FileName"].split("_+_")[1], js["FileName"].split("_+_")[2]
                added_lines = main(js, team1.replace('%20', ' '), team2.replace('%20', ' '))
                line_num += added_lines
    return {"file_name":FILE_NAME, "line_num":line_num}

if __name__ == "__main__":
    x()