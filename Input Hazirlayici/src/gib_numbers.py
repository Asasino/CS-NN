import simplejson as json

def team_numbers(FILE_NAME):
    with open(FILE_NAME, 'r') as f:
        lines = f.readlines()
    new = ""
    cnt = 0
    for line in lines:
        if line:
            new += line.strip() + "_+_" + str(cnt) + '\n'
            cnt += 1
    with open(FILE_NAME, 'w') as f:
        f.write(new)

def player_numbers(FILE_NAME):
    with open(FILE_NAME, 'r') as f:
        lines = f.readlines()
    new = ""
    cnt = 0
    for line in lines:
        if line:
            new += line.strip() + "_+_" + str(cnt) + '\n'
            cnt += 1
    with open(FILE_NAME, 'w') as f:
        f.write(new)

def map_numbers(FILE_NAME):
    with open(FILE_NAME, 'r') as f:
        lines = f.readlines()
    new = ""
    cnt = 0
    for line in lines:
        if line:
            new += line.strip() + "_+_" + str(cnt) + '\n'
            cnt += 1
    with open(FILE_NAME, 'w') as f:
        f.write(new)

def x():
    js = None
    with open("file_index.json", 'r') as f:
        js = json.load(f)
    team_numbers(js["PTN"]["file_name"])
    player_numbers(js["PPN"]["file_name"])
    map_numbers(js["PM"]["file_name"])

if __name__ == "__main__":
    team_numbers()
    player_numbers()
    map_numbers()