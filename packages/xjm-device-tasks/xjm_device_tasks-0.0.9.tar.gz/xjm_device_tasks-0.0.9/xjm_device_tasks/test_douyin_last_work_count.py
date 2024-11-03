from .client import PublishClient, create_usb_client, PublishData
from .task_douyin_last_work_count import GetDouyinFirstPageCountTask

cli = create_usb_client("a624d41f0304")
task = GetDouyinFirstPageCountTask()
cli.set_task(task)
cli.run_current_task(clear_task=False)
print(cli.context)
