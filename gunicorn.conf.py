import multiprocessing
import os


bind = '0.0.0.0:{}'.format(os.environ['PORT'])
preload = True
workers = multiprocessing.cpu_count() * 2
worker_class = 'gevent'

def post_fork(server, worker):
    from psycogreen.gevent import patch_psycopg
    patch_psycopg()
    worker.log.info('Colored psycopg green.')
