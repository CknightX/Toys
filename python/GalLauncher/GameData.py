import json
import os
from json import encoder

path = 'data.json'
cwd = os.getcwd()

def get_data():
    os.chdir(cwd)
    if not os.path.exists(path):
        with open(path,'w',encoding='utf-8') as f:
            f.write('{}')

    with open(path,'r',encoding='utf-8') as f:
        jobj = json.loads(f.read())
        return jobj

def update(jobj):
    os.chdir(cwd)
    with open(path,'w',encoding='utf-8') as f:
        f.write(json.dumps(jobj,ensure_ascii=False,indent=4))

def add_game(name,path):
    process_name = path[path.rfind('/') + 1 :]
    games = get_data()
    game_info = {
        "timeline" : [],
        "process" : process_name,
        "path" : path
    }
    games[name] = game_info
    update(games)

def del_game(name):
    pass

def get_game_info(name):
    games = get_data()
    return games[name]

def add_game_time(name,time_begin,time_end):
    games = get_data()
    games[name]['timeline'].append(f"{time_begin}-{time_end}")
    update(games)

if __name__ == '__main__':
    print(get_data())