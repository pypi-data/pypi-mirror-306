import os.path
import time
from typing import Optional, Tuple, Union

from .client import Stage, PublishTask, PublishClient, AndroidClient, \
    ClientWaitTimeout, TaskAsStage, PublishData, \
    get_logger
from .task_comm import SleepStage
from .task_error import InitiativeException
from .task_file_upload import RemoteFileToPhoneTask, RefreshPhoneAlbumStage, LocalFileToPhoneTask
from .task_helper import url_extract_filename
from .task_unlock_phone import UnlockPhoneTask
from .util import combine_with_hash

Logger = get_logger()


class OpenAppStage(Stage):
    def __init__(self, serial, clear_data: bool = False, system_user_id=0):
        self.clear_data = clear_data
        super().__init__(serial)
        self.app_name = "com.ss.android.ugc.aweme"
        self.user_id = system_user_id

    def run(self, client: PublishClient):
        if self.user_id:
            if not client.user_have_package(self.user_id, self.app_name):
                raise InitiativeException("未找到手机用户%s的抖音" % self.user_id)

        indexActivity = "com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.main.MainActivity"
        # 判断当前抖音是否已经打开了
        if client.device.info["currentPackageName"] == self.app_name:
            # 在抖音里面 则回到首页
            # 注意这里 在首页和我的 都是在MainActivity中
            client.back_to_activity(indexActivity)
        else:
            # 为什么要stop 因为无法判断当前在那一个页面
            client.device.app_stop(self.app_name)
            if self.clear_data:
                client.device.app_clear(self.app_name)

            start_shell = f'am start -n {indexActivity} --user {self.user_id}'
            client.device.shell(start_shell)
            if self.clear_data:
                client.wait_to_click({'text': '同意'})
            time.sleep(30)
            # 等待打开抖音
            client.wait_until_activity(indexActivity, timeout=60)


class PressAddIconStage(Stage):
    def run(self, client: PublishClient):
        client.relative_click(0.5, 0.96, double=True)
        # 等待进入视频发布的activity
        try:
            client.wait_until_activity(
                "com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.shortvideo.ui.VideoRecordNewActivity", timeout=60)
        except ClientWaitTimeout as e:
            s = ClearModalStage(self.stage_serial)
            s.run(client)
            client.relative_click(0.5, 0.96, double=True)
            client.wait_until_activity(
                "com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.shortvideo.ui.VideoRecordNewActivity",
                timeout=10)


# 选择第一个视频
class ChoiceVideoStage(Stage):
    def run(self, client: PublishClient):
        ban_node = client.device.xpath("%禁止发布%")
        if ban_node.exists:
            raise InitiativeException(ban_node.get_text())
        # 选择相册
        client.wait_to_click({'text': "相册"}, timeout=10)
        time.sleep(2)
        # 等待所有照片列表出现
        client.device.xpath('//*[@text="所有照片"]').wait()
        time.sleep(2)
        # 选择视频栏目
        client.device.xpath('//*[@text="视频"]').click()
        time.sleep(3)
        firstClick = False
        for el in client.device.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/root_view"]').all():
            if el.elem.tag == 'android.widget.FrameLayout':
                firstClick = True
                el.click()
                break
        if not firstClick:
            raise Exception("无法找到第一个视频点击")
        client.wait_to_click({'text': "下一步"})
        if client.device.xpath('//*[@text="下一步"]').wait():
            client.device.xpath('//*[@text="下一步"]').click()
        # 等待高级设置出现 就算完成
        client.wait_until_found({'text': '高级设置'})


# 选择封面
class ChoiceCoverStage(Stage):
    def run(self, client: PublishClient):
        # 选择封面
        client.device.xpath('//*[@text="选封面"]').click()
        time.sleep(1)
        # 封面点击相册
        client.device.xpath('//*[@text="相册"]').click()

        # 等待所有照片列表出现
        if not client.device.xpath('//*[@text="所有照片"]').wait():
            raise Exception("选择封面 所有照片 页面未出现")

        if client.device.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/root_view"]').wait():
            # 选择第一张图片
            for el in client.device.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/root_view"]').all():
                if el.elem.tag == 'android.widget.FrameLayout':
                    el.click()
                    break
        # 等待下一步出现
        if not client.device.xpath('//*[@text="下一步"]').wait():
            raise Exception("选择封面后下一步按钮未出现")
        # 需要向下移动才能显示完这个封面
        client.device.swipe_ext("down", scale=0.8)
        # 点击下一步
        client.device.xpath('//*[@text="下一步"]').click()
        # 这种地方都需要给一点延迟 因为会向服务器发送请求
        if not client.device.xpath('//*[@text="保存封面"]').wait():
            raise Exception("保存封面按钮未出现")
        time.sleep(2)
        # 点击保存封面
        client.device.xpath('//*[@text="保存封面"]').click()
        time.sleep(2)


# 输入文案和tag
class InputTextStage(Stage):
    def __init__(self, stage_serial: int, data: PublishData):
        super().__init__(stage_serial)
        self.data = data

    def run(self, client: PublishClient):
        # 把文案和话题组合成一个字符串 话题最多5个
        # 新版本话题最多3个
        # 如果文字太多
        description = self.data.wenan + combine_with_hash(self.data.topic[:3])
        client.device.xpath('//android.widget.EditText[contains(@text,"添加作品描述")]').set_text(description)
        if client.device.xpath("com.github.uiautomator:id/keyboard").exists:
            # 输入完成之后把 输入框关闭掉
            client.adb_input_hide()


# 选择地理位置
class PressPositionStage(Stage):
    def __init__(self, stage_serial: int, data: PublishData):
        super().__init__(stage_serial)
        self.data = data

    def run(self, client: PublishClient):
        client.wait_to_click({'text': "你在哪里"})
        client.wait_until_activity(
            "com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.poi.anchor.poi.publish.lynx.SelectPoiActivity")
        time.sleep(5)

        if client.device.xpath("以后再说").exists:
            client.device.xpath("以后再说").click()
        # 这个是权限弹窗
        if client.device.xpath("暂不").exists:
            client.device.xpath("暂不").click()
        time.sleep(5)
        lynx_input = client.device.xpath("//com.bytedance.ies.xelement.input.LynxInputView").get()
        # 页面布局不是通过text 而是lynxInputView 所以无法通过text定位
        # client.device.xpath("搜索位置").set_text(self.data.position)
        client.device.click(*lynx_input.center())  # 点亮输入模式
        client.device.send_keys(self.data.position)  # 输入内容
        time.sleep(5)
        if client.device.xpath("没有搜索到相关位置").exists:
            raise InitiativeException("地理位置未搜索到POI")
        # 选择第一个
        _, y, _, h = lynx_input.rect
        client.device.click(lynx_input.center()[0], y + h * 4)
        # 会自动返回到发布页
        client.wait_until_found({'text': "高级设置"})


# 点击发布等待上传完成
class PressPublishStage(Stage):
    def run(self, client: PublishClient):
        # 等待发布按钮出现
        # 版本不同的时候 这个按钮的文字不同 但是位置是固定的
        # 若再不稳定则可以考虑通过位置去定位
        btnText = ["发布", "发作品"]
        foundText = None
        for text in btnText:
            if not client.device.xpath(text).wait(timeout=5):
                continue
            foundText = text

        if foundText is None:
            raise Exception(f'发布按钮未出现')
        Logger.info(f"发布按钮文字：{foundText}")

        # 点击发布按钮
        client.device.xpath(foundText).click()
        if not client.device.xpath(foundText).wait_gone():
            # 再次点击一下
            client.relative_click(0.8, 0.95)
            if not client.device.xpath(foundText).wait_gone():
                raise Exception(f'{foundText}按钮未消失')

        # 等待进度条消失
        client.device.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/progress"]').wait_gone(timeout=120)

        # 发布按钮成功之后 也需要等待上传完成 这里需要时间长一点
        client.device.xpath('//*[@text="发布成功"]').wait(timeout=120)

        # 获取当前这一条视频的id?


# 对抖音弹出的弹出层进行关闭
class ClearModalStage(Stage):

    def run(self, client: PublishClient):
        # 之前有作品的弹窗

        # 每次减一
        try_count = 2
        while try_count > 0:
            try:
                cancel_node = (client.device.xpath("存草稿") |
                               client.device.xpath("拒绝") |
                               client.device.xpath("取消") |
                               client.device.xpath("关闭") |
                               client.device.xpath("以后再说")).get(timeout=5)
                cancel_node.click()
            except Exception as e:
                pass
            try_count -= 1
            time.sleep(2)
            continue
        #
        #
        # if client.device.xpath('//*[@text="继续编辑作品吗？"]').exists:
        #     if client.device.xpath('//*[@content-desc="取消"]').exists:
        #         client.device.xpath('//*[@content-desc="取消"]').click()
        #     elif client.device.xpath("存草稿").exists:
        #         client.device.xpath("存草稿").click()
        #     else:
        #         raise Exception("无法找到编辑作品弹窗的取消按钮")
        # # 访问通讯录
        # if client.device.xpath("//*[contains(@text, '通讯录')]").exists:
        #     client.device.xpath("拒绝").click()
        #
        # # 青少年模式弹窗
        # if client.device.xpath('//*[@text="青少年模式"]').exists:
        #     client.device.xpath('//*[@text="关闭"]').click()
        #
        # # 只要有以后再说 就点
        # if client.device.xpath("以后再说").exists:
        #     client.device.xpath("以后再说").click()

        # # 如果弹出了更新
        # if client.device.xpath('//*[@text="立即升级"]').exists:
        #     client.device.xpath('//*[@text="以后再说"]').click()
        #
        # # 欢迎体验新版本
        # if client.device.xpath("欢迎体验新版本").exists:
        #     client.device.xpath("以后再说").click()

        # # 发现抖音朋友的弹窗
        # if client.device.xpath("发现抖音朋友").exists:
        #     client.device.xpath("拒绝").click()


# 抖音视频发布任务
class DouyinVideoPublishTask(PublishTask):

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
        unlock = UnlockPhoneTask(unlock_path, back_to_home=False)
        self.stages.append(TaskAsStage(0, unlock))
        # 判断当前安卓版本 如果11以内 则使用普通上传
        # 现在就使用普通上传 上传文件和预览图
        upload_local_tmp_folder = "./dy_tmp"
        upload_remote_tmp_folder = "/sdcard/DCIM/Camera/dy_tmp/"
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

        # 打开抖音
        self.stages.append(OpenAppStage(2, system_user_id=system_user_id))
        self.stages.append(SleepStage(3, 3))
        # 清理掉各种弹窗
        self.stages.append(ClearModalStage(3))
        self.stages.append(SleepStage(3, 3))
        # 点击上传按钮
        self.stages.append(PressAddIconStage(4))
        self.stages.append(SleepStage(4, 2))
        # 进行视频选择
        self.stages.append(ChoiceVideoStage(5))
        # 输入文案和话题
        self.stages.append(InputTextStage(6, self.data))
        # 如果封面存在则选择封面
        if self.data.cover_url or self.data.local_cover_path:
            self.stages.append(ChoiceCoverStage(7))
        # 如果地理位置存在则选择地理位置
        if self.data.position is not None and len(self.data.position) >= 1:
            self.stages.append(PressPositionStage(8, self.data))
        # 点击进行发布
        self.stages.append(PressPublishStage(8))
        self.auto_serial()
        self.set_finnish_callback(self.on_finnish)

    def on_finnish(self, client: AndroidClient):
        Logger.info("抖音上传任务finnish 执行清理工作")
        client.device.app_stop('com.ss.android.ugc.aweme')
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
        Logger.info("抖音上传任务finnish 执行结束")
