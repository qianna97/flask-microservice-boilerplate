from flask import Flask, jsonify, render_template, request
from .Types import *
from celery import Celery


app                                          = Flask(__name__, template_folder='../Templates', static_folder='../Static')
app.config['SECRET_KEY']                     = SECRET_KEY
app.config['CACHE_TYPE']                     = "redis"
app.config['CACHE_DEFAULT_TIMEOUT']          = 86400
app.config['CACHE_REDIS_URL']                = REDIS_CACHE_URL
app.config['SQLALCHEMY_DATABASE_URI']        = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CELERY_BROKER_URL']              = REDIS_BROKER_URL
app.config['CELERY_RESULT_BACKEND']          = REDIS_BROKER_RESULT


# for make celery obj
def make_celery_app(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


# 404 handling
@app.errorhandler(404)
def page_not_found(e):
    data = {
        "Status": 404,
        "Message": 'Not Found.'
    }

    return jsonify(data), 404