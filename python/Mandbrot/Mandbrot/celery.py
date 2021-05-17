from celery import Celery

app=Celery('Mandbrot',include=['Mandbrot.tasks'])
app.config_from_object('Mandbrot.celeryconfig')

if __name__=='__main__':
    app.start()
