from .client import PublishClient, create_usb_client, PublishData
from .task_douyin_update_signature import DouyinUpdateSignatureTask, DouyinUpdateSignatureData

data = DouyinUpdateSignatureData(
    mention_id="",
    # signature="前面一个@@@这是后面的"
    signature="前面一个这是后面的"
)

cli = create_usb_client("281511f39805")

task = DouyinUpdateSignatureTask(data=data, system_user_id=999)
cli.set_task(task)
cli.run_current_task(clear_task=False)
print(cli.context)
