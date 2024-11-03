from .client import PublishClient, create_usb_client, PublishData
from .task_douyin_sec_uid import GetSelfSecUidTask


cli = create_usb_client("281511f39805")
print(cli.get_all_user())
task = GetSelfSecUidTask(system_user_id=999)
cli.set_task(task)
cli.run_current_task(clear_task=True)
print(cli.context)
