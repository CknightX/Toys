from Mandbrot.tasks import get_img
from Mandbrot.celery import app
from celery.result import AsyncResult
from PIL import Image
from tasks_dao import *
import redis,os
import time

def save_img(path,filename,img_data):
    im=Image.fromarray(img_data)
    im.save(os.path.join(path,filename))

def main():
    r=redis.Redis(host='172.16.20.98',port=6379,decode_responses=True,db=0)
    conn=create_db('tasks.db')
    tasks=get_all_unfinished_task(conn)
    counts=len(tasks)
    while counts>0:
        c=0
        for task in tasks:
            async_result=AsyncResult(id=task[0],app=app)
            if async_result.ready():
                c+=1
                result=async_result.get()
                print(result)
                save_img('./result',f'{result.filename}',result.img_data)
                set_task_status(conn, task[0],1)
                r.delete('celery-task-meta-'+task[0])
        counts-=c
        time.sleep(5)
    conn.close()
    r.close()

if __name__=='__main__':
    main()