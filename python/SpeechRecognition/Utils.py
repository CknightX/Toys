import json,configparser
import pypinyin,re


pes = ['氢','氦','锂','皮','硼','碳','氮','氧','氟','氖',
        '钠','镁','铝','硅','磷','硫','氯','氩',
            '钾','钙','钪','钛','钒','铬','锰','铁','钴','镍','铜','锌','镓','锗','砷','硒','溴','氪',
                '铷','锶','钇','锆','铌','钼','碍','钌','铑','钯','银','镉','铟','锡','锑','碲','碘','氙',
                    '铯','钡','镧','铈','镨','钕','钷','钐','铕','钆','铽','镝','钬','铒','铥','镱','镥','铪','钽','钨','铼','锇','铱','铂','金','汞','铊','铅','铋','钋','砹','氡',
                        '钫','镭','锕','钍','镤','铀','镎','钚','镅','锔','锫','锎','锿','镄','钔','锘','铹','鑪']

pes_pinyin = None # 元素拼音库
have_shengdiao = True  # 是否有声调

def to_pinyin(setence : str,have_shengdiao = have_shengdiao):
    """ 文本转拼音 """
    setence = setence.replace(' ','')
    if not have_shengdiao:
        pinyins = pypinyin.pinyin(setence,style=pypinyin.NORMAL)
    else:
        pinyins = pypinyin.pinyin(setence,style=pypinyin.Style.TONE3)

    res = ''
    for pinyin in pinyins:
        if len(setence) == 1:
            res += f'{pinyin[0]}'
        else:
            res += f'{pinyin[0]} '
    return res

def setence2no(s):
    """ 从文本中提取元素序号 """

    # 构建元素拼音库
    global pes_pinyin
    if pes_pinyin is None:
        pes_pinyin = []
        for p in pes:
            pes_pinyin.append(to_pinyin(p))
    

    s_pinyin = to_pinyin(s) # 文本转到拼音

    try:
        # 有声调
        if have_shengdiao:
            yuansu = re.search(r'([a-z1-4]+) yuan\d? zi\d?',s_pinyin) # 尝试提取对应的元素拼音
            if yuansu is None:
                yuansu = re.search(r'([a-z1-4]+) yuan\d? su\d?',s_pinyin) # 尝试提取对应的元素拼音
            yuansu = yuansu.group(1)
        # 无声调
        else:
            yuansu = re.search('([a-z]+) yuan zi',s_pinyin) # 尝试提取对应的元素拼音
            if yuansu is None:
                yuansu = re.search('([a-z]+) yuan su',s_pinyin) # 尝试提取对应的元素拼音
            yuansu = yuansu.group(1)

    except:
        return -1
    # 将元素拼音转到对应序号
    return pe2no(yuansu)
        


def pe2no(pe):
    """ 元素转序号，pe是拼音 """
    if pe not in pes_pinyin:
        return -1
    return pes_pinyin.index(pe) + 1

def no2pe(no):
    if no > len(pes) or no < 1:
        return ''
    return pes[no]

def get_conf(section,key):
    conf = configparser.ConfigParser()
    conf.read('./config.ini',encoding='utf-8')
    return conf.get(section,key)

if __name__ == '__main__':
    print(setence2no('皮 原子'))