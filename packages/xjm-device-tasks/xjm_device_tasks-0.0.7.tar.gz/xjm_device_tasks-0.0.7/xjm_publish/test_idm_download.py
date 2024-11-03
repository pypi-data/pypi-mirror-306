from .client import PublishClient, create_usb_client
from .task_idm import IDMPullTask

cli = create_usb_client()
task = IDMPullTask('http://192.168.3.125:8000/law.webm')
cli.set_task(task)
cli.run_current_task()
