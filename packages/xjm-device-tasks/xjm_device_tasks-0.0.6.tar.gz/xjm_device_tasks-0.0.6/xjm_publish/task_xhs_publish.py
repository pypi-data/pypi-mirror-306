import os
import time
from typing import Union, Optional, Tuple

from .client import PublishTask, PublishData, TaskAsStage, Stage, PublishClient, AndroidClient
from .logger import get_logger
from .task_comm import PressRelativePositionStage, WaitActivityStage, SleepStage
from .task_file_upload import RemoteFileToPhoneTask, LocalFileToPhoneTask, RefreshPhoneAlbumStage
from .task_helper import url_extract_filename
from .task_unlock_phone import UnlockPhoneTask
from .util import combine_with_hash

Logger = get_logger()

xhs_app_package_name = "com.xingin.xhs"


class OpenXhsStage(Stage):
    def __init__(self, serial, clear_data: bool = False, system_user_id=0):
        super().__init__(serial)
        self.clear_data = clear_data
        self.app_package_name = xhs_app_package_name
        self.user_id = system_user_id

    def run(self, client: PublishClient):
        client.device.app_stop(self.app_package_name)
        if self.clear_data:
            client.device.app_clear(self.app_package_name)

        client.device.shell(
            f'am start -n com.xingin.xhs/com.xingin.xhs.index.v2.IndexActivityV2 --user {self.user_id}')

        time.sleep(30)
        client.wait_until_activity("com.xingin.xhs/com.xingin.xhs.index.v2.IndexActivityV2", timeout=60)


class ClearModalStage(Stage):
    def __init__(self, serial, ):
        super().__init__(serial)

    def run(self, client: PublishClient):
        if client.device.xpath('//*[@text="存草稿"]').exists and client.device.xpath('//*[@text="去编辑"]').exists:
            # 获取到去编辑的父级
            x, y, w, h = client.device.xpath('//*[@text="去编辑"]').parent('//android.view.ViewGroup').rect
            click_x = w + 40
            click_y = y + 40
            client.device.click(click_x, click_y)
        # 版本升级?

        # 已经被封禁
        if client.device.xpath("//*[contains(@text, '发布失败')]").exists:
            msg = client.device.xpath("//*[contains(@text, '联系薯队长')]").get_text()
            raise Exception(msg)


class ChoiceVideoStage(Stage):
    def __init__(self, serial, ):
        super().__init__(serial)

    def run(self, client: PublishClient):
        # 如果没找到内容
        if client.xpath_exists('//*[@text="相册内没有视频或照片"]'):
            raise Exception("没有找到任何视频和图片")
        # 点击视频
        client.wait_to_click({"text": "视频"})
        # 点击第一个
        client.relative_click(0.14, 0.23)
        # 点击下一步
        client.wait_to_click({"text": "下一步"})
        # 这里要等久一点 确保视频的关键帧载入成功了
        time.sleep(15)
        # 选择音乐这一步 也要下一步
        client.wait_to_click({"text": "下一步"})
        # 等待进入发布汇总页
        client.wait_until_found({"text": "发布笔记"}, timeout=10)


class ChoiceCoverStage(Stage):
    def __init__(self, serial, ):
        super().__init__(serial)

    def run(self, client: PublishClient):
        client.wait_to_click({"text": "添加封面"})
        time.sleep(1)
        client.wait_to_click({"text": "相册"})
        time.sleep(1)
        # 点选第一个
        client.relative_click(0.18, 0.17)
        time.sleep(1)
        # 向下滚动
        client.device.swipe_ext("down", scale=1)
        time.sleep(1)
        # 点击下一步
        client.wait_to_click({"text": "下一步"})
        time.sleep(1)
        # 再次点击完成
        client.wait_to_click({"text": "完成"})
        # 等待封面合成完成
        client.device.xpath('完成').wait_gone(timeout=60)


# 输入文案和tag
class InputTextStage(Stage):
    def __init__(self, stage_serial: int, data: PublishData):
        super().__init__(stage_serial)
        self.data = data

    def run(self, client: PublishClient):
        # 把文案和话题组合成一个字符串 话题最多5个
        description = self.data.wenan + combine_with_hash(self.data.topic)
        client.device.xpath('//android.widget.EditText[contains(@text,"添加正文")]').set_text(description)
        if client.device.xpath("com.github.uiautomator:id/keyboard").exists:
            # 输入完成之后把 输入框关闭掉
            client.adb_input_hide()


class PublishStage(Stage):
    def __init__(self, stage_serial: int):
        super().__init__(stage_serial)

    def run(self, client: PublishClient):
        # 点击发布笔记
        client.wait_to_click({"text": "发布笔记"})
        # 如果被检测到封面是纯色
        if client.device.xpath("封面检测").exists:
            raise Exception("封面检测到是纯色")
        time.sleep(60)
        if client.device.xpath("//*[contains(@text, '发布失败')]").exists:
            msg = client.device.xpath("//*[contains(@text, '联系薯队长')]").get_text()
            raise Exception(msg)
        # 等待笔记发布完成
        client.wait_until_found({"text": "去看看笔记"}, timeout=180)
        time.sleep(60)


class XhsVideoPublishTask(PublishTask):
    def __init__(self,
                 priority: int = 3,
                 data: Union[PublishData, dict] = {},
                 unlock_path: Optional[list[Tuple[int, int]]] = [],
                 system_user_id: int = 0
                 ):
        super().__init__(priority, data)
        # 判断参数是否正确
        if not self.data.video_url and not self.data.local_video_path:
            raise Exception("视频地址和本地视频路径不能同时为空")
        # 解锁手机
        unlock = UnlockPhoneTask(unlock_path)
        self.stages.append(TaskAsStage(0, unlock))
        # 判断当前安卓版本 如果11以内 则使用普通上传
        # 现在就使用普通上传 上传文件和预览图
        upload_local_tmp_folder = "./xhs_tmp"
        upload_remote_tmp_folder = "/sdcard/DCIM/Camera/xhs_tmp/"
        # 远程文件
        for i, k in enumerate(["video_url", "cover_url"]):
            v = getattr(self.data, k)
            if not v:
                continue
            filename = url_extract_filename(v)
            local_save_path = os.path.join(upload_local_tmp_folder, filename)
            remote_save_path = upload_remote_tmp_folder + filename
            self.upload_local_files.append(local_save_path)
            self.upload_remote_files.append(remote_save_path)
            uploadTask = RemoteFileToPhoneTask(v, local_save_path, remote_save_path)
            self.stages.append(TaskAsStage(1, uploadTask))
        # 本地文件
        for i, k in enumerate(["local_video_path", "local_cover_path"]):
            v = getattr(self.data, k)
            if not v:
                continue
            filename = os.path.basename(v)
            remote_save_path = upload_remote_tmp_folder + filename
            self.upload_remote_files.append(remote_save_path)
            uploadTask = LocalFileToPhoneTask(v, remote_save_path)
            self.stages.append(TaskAsStage(1, uploadTask))
        # 打开小红书
        self.stages.append(OpenXhsStage(3, system_user_id=system_user_id))
        self.stages.append(ClearModalStage(3))
        # 点击加号
        self.stages.append(PressRelativePositionStage(4, 0.5, 0.97))
        # 判断权限弹窗
        # 权限有两个 一个是读取照片和文件 一个是地理位置
        # self.stages.append(PressTextStage(5, "仅在使用中允许", raise_not_found=False))
        # self.stages.append(PressTextStage(6, "仅在使用中允许", raise_not_found=False))
        # 等待进入到activity
        self.stages.append(WaitActivityStage(7, "com.xingin.xhs/com.xingin.capa.lib.entrance.CapaEntranceActivity"))
        # 选择视频
        self.stages.append(ChoiceVideoStage(8))
        # 需要等待加载tag
        self.stages.append(SleepStage(9, 3))

        # 选择封面
        # 如果封面存在则选择封面
        # 现在选择封面有bug 不知道是不是u2的 在选择合成之后会闪烁 然后关闭
        # if self.data.cover_url or self.data.local_cover_path:
        #     self.stages.append(ChoiceCoverStage(9))
        self.stages.append(SleepStage(9, 2))
        # 填写文案内容
        self.stages.append(InputTextStage(10, self.data))
        self.stages.append(SleepStage(10, 2))
        # 进行发布
        self.stages.append(PublishStage(11))

        self.auto_serial()
        self.set_finnish_callback(self.on_finnish)

    def on_finnish(self, client: AndroidClient):
        Logger.info("小红书上传任务finnish 执行清理工作")
        client.device.app_stop(xhs_app_package_name)
        # 删除本地文件
        try:
            for file in self.upload_local_files:
                os.remove(file)
            self.upload_local_files = []
        except Exception as e:
            pass

        # 删除远程文件
        try:
            for file in self.upload_remote_files:
                Logger.info(f"删除远程文件: {file}")
                client.device.shell(f"rm {file}")
                r = RefreshPhoneAlbumStage(0, file)
                r.run(client)
            self.upload_remote_files = []
        except Exception as e:
            pass
        Logger.info("小红书上传任务finnish 执行结束")
