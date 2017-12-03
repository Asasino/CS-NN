import nameSimilarity

def load_team(takim):
    with open("team_names.dat", 'r') as f:
        lines = f.readlines()
    edited_lines = []
    for line in lines:
        edited_lines.append(line.split("_+_")[0])
    similars = nameSimilarity.find_diff(takim, edited_lines)
    tm = similars[len(similars)-1][2]
    print "found: ", similars[len(similars) - 1][-1]
    for line in lines:
        if tm == line.split("_+_")[0]:
            return line.split("_+_")[-1].strip()
def load_player(player):
    with open("player_names.dat", 'r') as f:
        lines = f.readlines()
    edited_lines = []
    for line in lines:
        edited_lines.append("".join(line.split("'")[1:2]))
    similars = nameSimilarity.find_diff(player, edited_lines)
    pl = similars[len(similars)-1][2]
    print "found: ", similars[len(similars) - 1][-1]
    for line in lines:
        if pl == "".join(line.split("'")[1:2]):
            return line.split("_+_")[-1].strip()
def load_map(map):
    with open("map.dat", 'r') as f:
        lines = f.readlines()
    edited_lines = []
    for line in lines:
        edited_lines.append(line.split("_+_")[0])
    similars = nameSimilarity.find_diff(map, edited_lines)
    pl = similars[len(similars)-1][2]
    print "found: ", similars[len(similars)-1][-1]
    for line in lines:
        if pl == line.split("_+_")[0]:
            return line.split("_+_")[-1].strip()
def main(chc):
    out = ""
    for i in range(2):
        #takim = raw_input("Team name: ")
        #out += load_team(takim) + ","
        for i in range(5):
            player = raw_input("Player "+str(i+1)+": ")
            out += load_player(player=player) + ','
    if choice == 2:
        map = raw_input("Map: ")
        map = load_map(map)
        importance = raw_input("Which game of the best of? (importance): ")
        out = map + "," + importance + "," + out[:-1]
    return out
if __name__ == "__main__":
    choice = input("Match based | 1, Map based | 2: ")
    x = main(choice)
    print x.strip()