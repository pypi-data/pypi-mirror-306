from .adb import ADB
from .client import PublishClient, create_usb_client, PublishData

for device in ADB.device_list():
    cli = create_usb_client(device.serial)
    userid, activity = cli.get_focus_activity()
    print(userid)
    print(activity)
