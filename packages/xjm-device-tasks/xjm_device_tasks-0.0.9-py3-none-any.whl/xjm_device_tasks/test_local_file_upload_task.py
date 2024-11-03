from .client import PublishClient, create_usb_client
from task_file_upload import LocalFileToPhoneTask
from task_helper import url_extract_filename

# local_path = r"D:\xuejimao_cache\WebAV-export-1723020493219.mp4"
# local_path = r"D:\xuejimao_cache\xuejimao_export_1723032504439.mp4"
# local_path = r"E:\素材\骑自行车 转码\1040g0cg311vac6uo32005orvjlg7rdij92gjrqg.mp4"
local_path = r"E:\py_project\video_publish\m2.mp4"
filename = url_extract_filename(local_path)
remote_save_path = "/sdcard/DCIM/Camera/dy_tmp/" + filename

# cli = create_usb_client("A7QDU18901000934")
# cli = create_usb_client("7de9da060704")
cli = create_usb_client("7de9da060704")
task = LocalFileToPhoneTask(local_path, remote_save_path)
cli.set_task(task)
cli.run_current_task()
