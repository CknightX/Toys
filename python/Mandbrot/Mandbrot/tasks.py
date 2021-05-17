import time
from Mandbrot.celery import app
from Mandbrot.Mandbrot import draw

class Img:
    def __init__(self,zoom,img_data):
        self.filename=f'{zoom}.jpg'
        self.img_data=img_data

@app.task
def get_img(x,y,zoom,no):
    img_data=draw((x,y),zoom)
    res=Img(no,img_data)
    return res

