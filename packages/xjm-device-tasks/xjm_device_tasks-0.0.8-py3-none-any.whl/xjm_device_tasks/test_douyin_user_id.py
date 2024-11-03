from .client import PublishClient, create_usb_client, PublishData
from .task_douyin_user_id import GetUserIdTask


cli = create_usb_client("deeb6adc0504")
task = GetUserIdTask()
cli.set_task(task)
cli.run_current_task(clear_task=False)
print(cli.context)
