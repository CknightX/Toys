from Mandbrot.tasks import get_img
from tasks_dao import *
import time
import os

# 放大点
p = (121,345)
# 张数
count=1000
# 倍数步长
zoom_step=1.1

def main():
    if os.path.exists('tasks.db'):
        os.remove('tasks.db')
    conn=create_db('tasks.db')
    zoom=1
    for i in range(count):
        zoom*=zoom_step
        async_task=get_img.delay(p[0],p[1],zoom,i)
        set_task_status(conn, async_task.id, 0)
if __name__=='__main__':
    main()

	#img=draw((121,340),1000000000000)


