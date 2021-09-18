import asyncio
from asyncio.windows_events import ERROR_CONNECTION_ABORTED
import aiohttp
from bs4 import BeautifulSoup
import re
import time


def gen_url(id,page):
    return f'https://bbs.saraba1st.com/2b/thread-{id}-{page}-1.html'

async def fetch_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            text=await resp.text('utf-8')
            return text

async def parse_num_pages(id):
    url=gen_url(id,1)
    text=await fetch_async(url)
    res=re.search('共 (\d+) 页',text)
    return 1 if res is None else int(res.group(1))


def _parse_posts(source_html):
    soup=BeautifulSoup(source_html,"html.parser")
    res=[]
    divs=soup.find_all('div',id=re.compile('post_\d+'))
    for div in divs:
        try:
            user=div.find('a',attrs={'class':'xw1'}).text
            tie_time=div.find('em',id=re.compile('authorposton')).text
            comment=div.find('td',attrs={'class':'t_f'}).text.strip()
            res.append((user,tie_time,comment))
        except Exception as e:
            res.append(('error','error','error'))
    return res

async def parse_posts(url,page_no):
    while True:
        try:
            text=await fetch_async(url)
            posts=_parse_posts(text)
        except Exception as e:
            await asyncio.sleep(5)
            continue
        else:
            break
    if not text or not posts:
        print(f'page {page_no} error,retry...')
        await asyncio.sleep(2)
        return await parse_posts(url,page_no)
    else:
        return posts


async def work(id,max_pages=-1):
    pages=await parse_num_pages(id)
    if max_pages!=-1:
        pages=min(pages,max_pages)
    print(f'页数：{pages}')
    tasks=[]
    for index in range(1,pages+1):
        url=gen_url(id,index)
        tasks.append(parse_posts(url,index))
    posts=await asyncio.gather(*tasks)
    floor=1
    
    with open(f'{id}.txt','w',encoding='utf-8') as f:
        for per_page in posts:
            for post in per_page:
                f.write(f'{floor}楼 {post[0]} {post[1]}\n')
                f.write(f'{post[2]}\n')
                f.write('----------------\n')
                floor+=1


    

def main():
    print('id:',end='')
    id=input()
    loop=asyncio.get_event_loop()
    loop.run_until_complete(work(id))

if __name__=='__main__':
    main()
