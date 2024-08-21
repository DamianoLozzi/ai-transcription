import os
import psutil
import simple_logger as sl

log = sl.Logger()

log.info('Starting Gunicorn configuration')

num_cores = psutil.cpu_count(logical=False)
num_threads = psutil.cpu_count(logical=True)

log.info(f'Number of cores: {num_cores}')
log.info(f'Number of threads: {num_threads}')

#workers = int(os.environ.get('GUNICORN_PROCESSES', max(1, num_cores - 1)))

workers=1

log.info(f'Number of workers: {workers}')

threads = int(os.environ.get('GUNICORN_THREADS', num_cores * 4))

log.info(f'Number of threads: {threads}')

bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8080')

#forwarded_allow_ips = '*'

#secure_scheme_headers = { 'X-FORWARDED-PROTO': 'https' }