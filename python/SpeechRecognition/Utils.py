import json,configparser

pes = ['氢','氦','锂','铍','硼','碳','氮','氧','氟','氖','钠','镁','铝','硅','磷','硫','氯','氩','钾','钙','钪','钛','钒','铬','锰','铁','钴','镍','铜','锌','镓','锗','砷','硒','溴','氪','铷','锶','钇','锆','铌','钼','碍','钌','铑','钯','银','镉','铟','锡','锑','碲','碘','氙','铯','钡','镧','铈','镨','钕','钷','钐','铕','钆','铽','镝','钬','铒','铥','镱','镥','铪','钽','钨','铼','锇','铱','铂','金','汞','铊','铅','铋','钋','砹','氡','钫','镭','锕','钍','镤','铀','镎','钚','镅','锔','锫','锎','锿','镄','钔','锘','铹','鐪']

def pe2no(pe):
    for i in range(len(pes)):
        if pes[i] == pe:
            return i+1
    return -1

def no2pe(no):
    if no > len(pes) or no < 1:
        return ''
    return pes[no]

def get_conf(section,key):
    conf = configparser.ConfigParser()
    conf.read('./config.ini',encoding='utf-8')
    return conf.get(section,key)


if __name__ == '__main__':
    print(no2pe(1000))
    print(get_conf('BAIDU','APP_ID'))