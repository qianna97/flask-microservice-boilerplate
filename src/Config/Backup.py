import os
import json
import datetime

from .Main import app
from .Core import db, celery
from .Types import SERVICE_NAME
from pathlib import Path
from celery.schedules import crontab


Path("database_backup").mkdir(parents=True, exist_ok=True)


app.config['CELERYBEAT_SCHEDULE'] = {
    'backup-every-midnight': {
        'task': 'backup',
        #'schedule': crontab(minute="*")
        'schedule': crontab(minute=0, hour=0)
    }
}


def get_tables():
    classes, models, table_names = [], [], []
    for clazz in db.Model._decl_class_registry.values():
        try:
            table_names.append(clazz.__tablename__)
            classes.append(clazz)
        except:
            pass
    for table in db.metadata.tables.items():
        if table[0] in table_names:
            models.append(classes[table_names.index(table[0])])
    
    return models, table_names


@celery.task(name="backup")
def database_backup():
    filename = 'database_backup/'+SERVICE_NAME+'_'+datetime.datetime.now().strftime('%d-%m-%Y')+'.json'
    with app.app_context():
        datas = {}
        models, tables = get_tables()

        for model, table in zip(models, tables):
            rows = db.session.query(model).all()
            tmp = []
            for row in rows:
                dictret = dict(row.__dict__)
                dictret.pop('_sa_instance_state', None)
                tmp.append(dictret)
            datas[table] = tmp
        
        json.dump(datas, open(filename, 'w'), default=str)


class DatabaseBackup(Command):
    option_list = (
        Option('--status', '-s', dest='status'),
        Option('--filename', '-f', dest='filename')
    )

    def _database_recovery(self, filename):
        f = open('database_backup/'+filename)
        data = json.loads(f.read())
        models, tables = get_tables()

        for model, table in zip(models, tables):
            print(table)
            for x in data[table]:
                res = model(**x)
                db.session.add(res)
                db.session.commit()

    def run(self, status, filename=None):
        if status == 'start':
            os.system('celery -A app.celery beat --detach')
            os.system('celery -A app.celery worker -f backup.log &')
            # using bash to direct access for docker
            #os.system("docker exec -t ka_postgres_restaurant_servcies pg_dumpall -c -U kasumi_restaurant_services > dump_`date +%d-%m-%Y`.sql")
        elif status == 'stop':
            os.system('pkill -f "celery worker"')
        elif status == 'recovery':
            # using bash to direct access for docker
            #os.system('cat '+filename+' | docker exec -i ka_postgres_restaurant_servcies psql -U kasumi_restaurant_services')
            if filename is None:
                print("Please insert file from database backup")
            else:
                self._database_recovery(filename)