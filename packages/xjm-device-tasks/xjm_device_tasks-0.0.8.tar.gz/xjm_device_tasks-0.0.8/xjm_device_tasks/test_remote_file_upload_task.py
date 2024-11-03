
from .client import PublishClient, create_usb_client
from task_file_upload import RemoteFileToPhoneTask
from task_helper import url_extract_filename

video_url = "D:\\xuejimao_cache\\xuejimao_export_1723027144149.mp4"
filename = url_extract_filename(video_url)
local_save_path = "./task_tmp/" + filename
remote_save_path = "/sdcard/DCIM/Camera/dy_tmp/" + filename

cli = create_usb_client("15992a1a0806")
task = RemoteFileToPhoneTask(video_url, local_save_path, remote_save_path)
cli.set_task(task)
cli.run_current_task()
