from .client import PublishClient, create_usb_client
from task_unlock_phone import UnlockPhoneTask

cli = create_usb_client("15992a1a0806") # 小米
# cli = create_usb_client("A7QDU18901000934") # 华为
task = UnlockPhoneTask()
cli.set_task(task)
cli.run_current_task()
