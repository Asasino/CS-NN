import os
import simplejson as json

FILE_NAME = "feed"+os.sep+"maps.dat"

def main(js):
    added_lines = 0
    with open(FILE_NAME, 'r+') as f:
        lines = f.readlines()
    gameformat = int(js["GameFormat"].split()[-1])
    for i in range(1, gameformat+1):
        match = js["Match "+str(i)]
        map = match["Map"]
        if map is None:
            continue
        found=False
        for line in lines:
            if map in line:
                found=True
        if found:
            continue
        with open(FILE_NAME, 'a+') as f:
            f.write(map+'\n')
            added_lines += 1
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
                    js = json.load(f)
                added_lines = main(js)
                line_num += added_lines
    return {"file_name":FILE_NAME, "line_num":line_num}

if __name__ == "__main__":
    x()