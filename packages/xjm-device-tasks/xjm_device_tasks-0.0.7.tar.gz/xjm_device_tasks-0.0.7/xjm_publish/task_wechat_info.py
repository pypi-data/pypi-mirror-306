import time
from typing import Union, Optional, Tuple


from .backend import get_backend
from .client import PhoneTask, AndroidClient, Stage, TaskAsStage
from .logger import get_logger
from .task_comm import SleepStage
from .task_error import InitiativeException
from .task_unlock_phone import UnlockPhoneTask
from .task_wechat_add_friend import OpenWechatStage

Logger = get_logger()


class GetMyInfoStage(Stage):
    def __init__(self, stage_serial: int):
        super().__init__(stage_serial)

    def run(self, client: AndroidClient):
        bottom_btn = client.get_max_or_min_node("我", "y")
        if bottom_btn.rect[1] < (client.get_screen_size()[0] * 0.7):
            raise InitiativeException("未找到底部的(我)的选项")
        client.device.click(*bottom_btn.center())
        client.wait_until_found({"text": "朋友圈"})
        client.wait_until_found({"text": "设置"})


class WeChatInfoStage(Stage):
    def __init__(self, stage_serial: int):
        super().__init__(stage_serial)

    def run(self, client: AndroidClient):
        id_node = client.device.xpath("%微信号%")
        id_text = id_node.get_text()
        # 如何获取微信昵称呢?
        id_elem = id_node.get()
        x, y, w, h = id_elem.rect
        click_x = w / 2
        click_y = y - 70
        nickname_node = client.get_node_containing_point(click_x, click_y)
        client.context["nick_name"] = nickname_node.attrs.get("text", "")
        client.context["id"] = id_text.replace("微信号：", "")


class WechatInfoTask(PhoneTask):
    def __init__(self,
                 priority: int = 3,
                 unlock_path: Optional[list[Tuple[int, int]]] = [],
                 system_user_id: int = 0
                 ):
        super().__init__(priority)
        self.system_user_id = system_user_id

        unlock = UnlockPhoneTask(unlock_path)
        self.stages.append(TaskAsStage(0, unlock))
        self.stages.append(OpenWechatStage(0, system_user_id))
        self.stages.append(SleepStage(1, 2))
        self.stages.append(GetMyInfoStage(2))
        self.stages.append(WeChatInfoStage(3))
        self.auto_serial()
        self.set_finnish_callback(self.on_finish)

    def on_finish(self, client: AndroidClient):
        Logger.info("微信信息获取完成finnish")

        if "id" in client.context:
            Logger.info(
                f'微信信息 {client.context["nick_name"]} 微信号:{client.context.get("id")} 手机用户空间号:{self.system_user_id}')
            # 写入db
            backend = get_backend()
            backend.add_platform_account(
                client.device.serial,
                f'微信',
                client.context["id"],
                client.context["nick_name"],
                system_user_id=self.system_user_id,
            )

            Logger.info("写入数据库成功")

        found = False
        for _ in range(5):
            client.shell("input keyevent 4")
            time.sleep(1)
            _, activity = client.get_focus_activity()
            if activity == "com.tencent.mm/com.tencent.mm.ui.LauncherUI":
                found = True
                break
        # 回到桌面
        client.shell("input keyevent 3")
