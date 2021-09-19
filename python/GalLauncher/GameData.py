import json
import os
from json import encoder

path = 'data.json'
cwd = os.getcwd()




def _version_update():
    """ json格式升级 """
    jobj = get_data()

    # 增加序号
    index = 1
    for name,info in jobj.items():
        if 'id' in info:
            break
        info['id'] = index
        index += 1
    update(jobj)



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

    # 按序号重排
    items = jobj.items()
    items = sorted(items,key = lambda x : x[1]['id']) 
    d = {}
    for item in items:
        d[item[0]] = item[1]
    jobj = d
    with open(path,'w',encoding='utf-8') as f:
        f.write(json.dumps(jobj,ensure_ascii=False,indent=4))

def add_game(name,path,id = None):
    process_name = path[path.rfind('/') + 1 :]
    games = get_data()

    if id is None:
        id = len(games) + 1

    game_info = {
        "id" : id,
        "timeline" : [],
        "process" : process_name,
        "path" : path
    }
    games[name] = game_info
    update(games)


def del_game_by_name(name,adjust_id = True):
    games = get_data()
    id = games[name]['id']
    del games[name]

    # 调整序号
    if adjust_id:
        for game in games:
            if games[game]['id'] > id:
                games[game]['id'] -= 1

    update(games)

def get_game_info_by_name(name):
    games = get_data()
    return games[name]

def get_id_by_name(name):
    games = get_data()
    if name not in games:
        return -1
    return games[name]['id']

def get_name_by_id(id):
    games = get_data()
    for game in games:
        if games[game]['id'] == int(id):
            return game
    return ''

def add_game_time(name,time_begin,time_end):
    games = get_data()
    games[name]['timeline'].append(f"{time_begin}-{time_end}")
    update(games)

if __name__ == '__main__':
    _version_update()