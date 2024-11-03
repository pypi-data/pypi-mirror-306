import os.path

from .client import Stage, PublishClient, ClientTask, AndroidClient, get_logger
from .task_helper import sync_download_file, get_posix_directory

Logger = get_logger()


# 通过adb上传本地文件到指定的文件夹中
class LocalFileUploadStage(Stage):
    def __init__(self, serial, local_path: str, remote_path: str):
        super().__init__(serial)
        self.local_path = local_path
        self.remote_path = remote_path

    def run(self, client: PublishClient):
        # 先判断文件是否存在
        if not os.path.exists(self.local_path):
            raise FileNotFoundError(self.local_path)
        Logger.info("上传文件从 %s 到 %s" % (self.local_path, self.remote_path))
        directory = get_posix_directory(self.remote_path)
        # 先创建远程路径
        client.shell("mkdir -p %s" % directory)
        # 把本地文件上传上去
        client.device.push(self.local_path, self.remote_path)
        # 判断文件是否存在
        if not client.exists(self.remote_path):
            raise FileNotFoundError(self.remote_path)


# 把文件下载到本地指定的保存目录中
class FileDownloadStage(Stage):
    def __init__(self, serial, url: str, save_path: str):
        super().__init__(serial)
        self.url = url
        self.save_path = save_path

    def run(self, client: PublishClient):
        sync_download_file(self.url, self.save_path)


# 刷新相册 仅对安卓11以下有用
class RefreshPhoneAlbumStage(Stage):
    def __init__(self, serial, remote_file_path: str):
        super().__init__(serial)
        self.remote_file_path = remote_file_path

    def run(self, client: AndroidClient):
        directory = get_posix_directory(self.remote_file_path)
        # 先获取到sdcard的路径
        sd_real_path = client.get_sdcard_real_path()
        abs_path = self.remote_file_path.replace("/sdcard", sd_real_path)
        # android.intent.action.MEDIA_SCANNER_SCAN_FILE 的路径必须是 绝对路径 也就是 /mnt/sdcard/ 而不是 /sdcard/
        client.shell(
            "am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://%s" % abs_path)
        # 在小米上 会报Permission Denial 无权限发送
        # 很多设备都会报错无权限 所以能发就发
        try:
            client.shell("am broadcast -a android.intent.action.MEDIA_MOUNTED -d file://%s" % directory)
        except Exception as e:
            pass


# 仅对安卓11以下有效
class RemoteFileToPhoneTask(ClientTask):
    def __init__(self, url: str, save_path: str, remote_path: str):
        super().__init__()
        self.url = url
        self.stages.append(FileDownloadStage(0, self.url, save_path))
        self.stages.append(LocalFileUploadStage(1, save_path, remote_path))
        self.stages.append(RefreshPhoneAlbumStage(2, remote_path))


# 仅对安卓11以下有效
class LocalFileToPhoneTask(ClientTask):
    def __init__(self, local_path: str, remote_path: str):
        super().__init__()
        self.stages.append(LocalFileUploadStage(0, local_path, remote_path))
        self.stages.append(RefreshPhoneAlbumStage(1, remote_path))
