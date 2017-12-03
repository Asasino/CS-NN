import simplejson as json
import os
from src import gib_numbers as GN
from src import prep_maps as PM
from src import prep_player_names as PPN
from src import prep_team_names as PTN
from src import map_based_prep_dat as MaBPD
from src import match_based_prep_dat as MBPD


CHOICE_LIST = [1, 2]

def update_index(pm, ptn, ppn):
    if not os.path.isfile("file_index.json"):
        with open("file_index.json", 'w') as f:
            pass
    js = {}
    try:
        with open("file_index.json", 'r') as f:
            js = json.load(f)
    except: pass
    js["PM"] = pm
    js["PTN"] = ptn
    js["PPN"] = ppn
    with open("file_index.json", 'w') as f:
        json.dump(js, f, indent=2, sort_keys=True)

def prepare_data():
    if not os.path.exists("data") or not os.path.exists("jsons"):
        print "Data is missing, cannot continue."
        return
    pm_data = PM.x()
    ptn_data = PTN.x()
    ppn_data = PPN.x()
    update_index(pm_data, ptn_data, ppn_data)
    GN.x()

def create_input(lower, upper, map):
    if map == 1:
        MaBPD.x(lower, upper)
    if map == 2:
        MBPD.x(lower, upper)

def main(choice):
    if choice == 1:
        prepare_data()
    if choice == 2:
        lower = input("\nLower bound for input:")
        upper = input("Upper bound for input:")
        if isinstance(lower, int) and isinstance(upper, int) and upper > lower:
            choice = input("1- Map based data\n2- Match based data\nEnter your choice:")
            if choice in CHOICE_LIST:
                create_input(lower, upper, choice)
            else:
                print "Wrong info."
        else:
            print "Wrong bounds."


if __name__ == "__main__":
    choice = input("1- Prepare new data\n2- Create input\nEnter your choice:")
    if choice in CHOICE_LIST:
        main(choice)
    else:
        print "Wrong info."