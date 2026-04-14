bind = "0.0.0.0:8000"

workers = 2
threads = 2
worker_class = "gunicorn.workers.sync.SyncWorker"

max_requests = 1000
max_requests_jitter = 50

timeout = 30
keepalive = 5

loglevel = "info"
accesslog = "-"
errorlog = "-"
