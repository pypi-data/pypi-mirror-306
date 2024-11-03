from .client import PublishClient, create_usb_client, PublishData
from task_wechat_add_friend import WechatAddFriendTask, WechatAddFriendData

# cli = create_usb_client("A7QDU18901000934")
cli = create_usb_client("P7CDU18510001945")

data = WechatAddFriendData(
    wechat_id="superspas",
    invite_msg="",
    remark="",
)

task = WechatAddFriendTask(data)
cli.set_task(task)
cli.run_current_task(clear_task=False)
print(cli.context)
