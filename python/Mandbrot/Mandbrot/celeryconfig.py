broker_url = 'redis://172.16.20.98:6379/1'
result_backend = 'redis://172.16.20.98:6379/0'
task_serializer = 'pickle'
result_serializer = 'pickle'
result_expires = 60 * 60 * 24
accept_content = ["pickle"]
