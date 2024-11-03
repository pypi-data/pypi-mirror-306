import re
import time
from typing import Optional, Union, Tuple

from pydantic import BaseModel

from .client import ClientTask, TaskAsStage, Stage, AndroidClient, PhoneTask
from .logger import get_logger
from .task_comm import SleepStage, PressTextStage, WaitTextStage, PressRelativePositionStage
from .task_douyin_publish import OpenAppStage, ClearModalStage
from .task_douyin_user_id import OpenMyBtnStage, OpenSettingDrawerStage, ParseCountsStage
from .task_error import InitiativeException
from .task_unlock_phone import UnlockPhoneTask

Logger = get_logger()


# 2024年9月6日 简介的修改 一天只能修改5次


class DouyinUpdateSignatureData(BaseModel):
    user_id: Optional[int] = 0
    signature: str  # 字符串中可以有 @@@ 符号作为占位符 会自动判断是否是否关注 然后打上备注
    mention_id: Optional[str] = None


class RunAddFriendStage(Stage):
    def __init__(self, stage_serial: int, data: DouyinUpdateSignatureData):
        super().__init__(stage_serial)
        self.data = data

    def run(self, client: AndroidClient):
        if not self.data.mention_id:
            return
        client.wait_to_click({"text": "添加朋友"})
        client.wait_until_activity("com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.friends.ui.RawAddFriendsActivity")
        time.sleep(2)
        # 找到添加朋友的title
        title_node = client.get_max_or_min_node("添加朋友", axios="y", max_or_min="min")
        x, y, w, h = title_node.rect
        click_x = x + w / 2
        click_y = y + h * 2
        client.device.click(click_x, click_y)
        # 找到输入框节点
        input_node = client.get_node_containing_point(click_x, click_y)
        # 获取到唯一的resource-id
        resource_id = input_node.attrs.get("resource-id")
        # 进行内容的传递
        client.device.xpath(f'@{resource_id}').set_text(self.data.mention_id)
        # 点击搜索
        client.wait_to_click({"text": "搜索"})
        client.wait_until_found({"text": "关注"})
        # 找到匹配节点
        match_node = client.device.xpath(f"//android.widget.TextView[contains(@text, '{self.data.mention_id}')]").get()
        # 获取到匹配节点的坐标
        mx, my, mw, mh = match_node.rect
        target_btn_x = client.device.info["displayWidth"] * 0.85
        target_btn_y = my + mh / 2
        # 找到这个按钮
        btn_node = client.get_node_containing_point(target_btn_x, target_btn_y, class_name="android.widget.TextView")
        btn_resource_id = btn_node.attrs.get("resource-id")
        # 获取他的文字
        text = btn_node.attrs.get("text")
        if text == "关注":
            client.device.click(target_btn_x, target_btn_y)
            time.sleep(5)
        # 然后回退到我的
        client.back_to_see_node((client.device.xpath("我的小程序") | client.device.xpath("我的钱包")))


class EditSignatureStage(Stage):
    def __init__(self, stage_serial: int, data: DouyinUpdateSignatureData):
        super().__init__(stage_serial)
        self.data = data

    def run(self, client: AndroidClient):
        client.wait_to_click({"text": "编辑资料"})
        client.wait_until_activity("com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.profile.ui.ProfileEditActivity")
        # 找到简介二字
        jj_label = client.device.xpath("简介").get()
        x, y, w, h = jj_label.rect
        client_x = client.device.info["displayWidth"] * 0.7
        client_y = y + h / 2
        client.device.click(client_x, client_y)
        # 等待修改简介的title出现
        client.wait_until_found({"text": "修改简介"})
        # 找到所有输入框
        all_input = client.device.xpath("//android.widget.EditText").all()
        Logger.info(f"输入框数量{len(all_input)}")
        first_input = all_input[0]
        first_input.click()
        client.device.clear_text()  # 清除输入
        # 判断@@@ 是否存在
        if "@@@" in self.data.signature:
            prefix, suffix = self.data.signature.split("@@@")
            # 先输入prefix
            client.device.send_keys(prefix)
            # 然后输入@符号
            client.device.send_keys("@")
            # 等待添加用户弹窗出现
            client.wait_until_found({"text": "添加用户"})
            # 找到搜索
            client.device.xpath("搜索用户").set_text(self.data.mention_id)
            client.wait_until_found({"text": "添加"})
            # 找到第一个添加按钮 点击
            client.wait_to_click({"text": "添加"})
            # 再输入suffix
            client.device.send_keys(suffix)
        else:
            client.device.send_keys(self.data.signature)
        # 点击保存
        client.wait_to_click({"text": "保存"})
        client.toast_show(exclude_list=["设置成功"])
        # 等待修改简介按钮消失
        if not client.device.xpath("修改简介").wait_gone():
            raise InitiativeException("修改简介失败 达到次数或网络波动或与上次文案相同")


class DouyinUpdateSignatureTask(PhoneTask):
    def __init__(self,
                 data: Union[DouyinUpdateSignatureData, dict] = {},
                 priority: int = 3,
                 unlock_path: Optional[list[Tuple[int, int]]] = [],
                 system_user_id: int = 0,
                 ):
        super().__init__(priority)
        if isinstance(data, dict):
            self.data = DouyinUpdateSignatureData(**data)
        else:
            self.data = data
        if self.data is None:
            raise Exception("必须有对应内容")

        # 签名可以为空

        if self.data.signature:
            if "@@@" in self.data.signature and not self.data.mention_id:
                raise Exception("签名中有@占位符但未传递抖音用户id")
        unlock = UnlockPhoneTask(unlock_path, back_to_home=False)
        self.stages.append(TaskAsStage(0, unlock))
        self.stages.append(OpenAppStage(1, system_user_id=system_user_id))
        # 清理掉各种弹窗
        self.stages.append(ClearModalStage(3))
        self.stages.append(SleepStage(3, 3))
        # 点击我的
        self.stages.append(OpenMyBtnStage(4))
        # 添加提及人的关注
        self.stages.append(RunAddFriendStage(5, self.data))
        # 编辑资料
        self.stages.append(EditSignatureStage(6, self.data))
        self.auto_serial()
        self.set_finnish_callback(self.on_finnish)

    def on_finnish(self, client: AndroidClient):
        Logger.info("设置抖音用户签名执行结束")
        client.device.app_stop('com.ss.android.ugc.aweme')
