import re
import time


from .backend import get_backend
from .client import ClientTask, TaskAsStage, Stage, AndroidClient
from .logger import get_logger
from .task_comm import SleepStage, PressTextStage, WaitTextStage, PressRelativePositionStage
from .task_douyin_publish import OpenAppStage, ClearModalStage
from .task_douyin_user_id import OpenMyBtnStage, OpenSettingDrawerStage, ParseCountsStage
from .task_error import InitiativeException
from .task_unlock_phone import UnlockPhoneTask

Logger = get_logger()


# 获取出作品列表页中最新的哪一个
class GetDouyinFirstPageWorkCountStage(Stage):
    def __init__(self, stage_serial: int):
        super().__init__(stage_serial)

    def run(self, client: AndroidClient):
        # 得向上面滚动一些 展示出这些作品
        client.device.swipe_ext("up", scale=1)
        # 等个2秒钟 等待数据的加载
        time.sleep(2)
        # 获取出作品的数量
        frame_all = client.device.xpath(
            "//androidx.recyclerview.widget.RecyclerView//android.widget.FrameLayout").all()
        if not len(frame_all):
            raise InitiativeException("未找到作品列表")
        number_list = []
        for index, frame in enumerate(frame_all):
            # 获取出所有的 //android.widget.TextView
            text_all = frame.elem.xpath(".//android.widget.TextView")
            # 过滤掉其中attrib["text"]包含 没有 的条目

            params = {
                "is_top": False,
                "index": index,
                "text": "-1"
            }
            is_match = False
            for text in text_all:
                if "置顶" == text.attrib["text"]:
                    params["is_top"] = True
                    continue
                t = text.attrib["text"]  # 下面有一个text显示 暂时没有更多了
                if "更多" in t:
                    continue
                # 判断t 如果是一个纯数字或有.号的话 就应该是了
                if t.isdigit() or "." in t:
                    is_match = True
                    params["text"] = t
                    break
            if is_match:
                number_list.append(params)
        client.context["number_list"] = number_list


# 获取抖音最前的一页作品的播放数

class GetDouyinFirstPageCountTask(ClientTask):
    def __init__(self, priority: int = 3, system_user_id=0, *args, **kwargs):
        super().__init__(priority)

        # 解锁手机
        unlock = UnlockPhoneTask([], back_to_home=False)
        self.stages.append(TaskAsStage(0, unlock))
        self.stages.append(OpenAppStage(1, system_user_id=system_user_id))
        # 清理掉各种弹窗
        self.stages.append(ClearModalStage(3))
        self.stages.append(SleepStage(3, 3))
        # 点击我的
        self.stages.append(OpenMyBtnStage(4))
        self.stages.append(GetDouyinFirstPageWorkCountStage(5))

        self.auto_serial()
        self.set_finnish_callback(self.on_finnish)

    def on_finnish(self, client: AndroidClient):
        Logger.info("获取抖音作品列表播放量执行结束")
        backend = get_backend()
        try:
            if client.context.get("number_list", None):
                backend.report_platform_works_views(client.device.serial, "抖音", client.context["number_list"])
        except Exception as e:
            Logger.error("上报抖音作品列表播放量错误", e)
