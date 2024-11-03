import time
from typing import Union, Optional, Tuple

from pydantic import BaseModel

from .client import PhoneTask, AndroidClient, Stage, TaskAsStage
from .logger import get_logger
from .task_comm import SleepStage
from .task_error import InitiativeException
from .task_unlock_phone import UnlockPhoneTask

Logger = get_logger()


class WechatAddFriendData(BaseModel):
    tel_phone: Optional[str] = ""  # 手机号 手机号微信号必有一个
    wechat_id: Optional[str] = ""  # 微信号
    invite_msg: Optional[str] = ""  # 好友申请信息
    remark: Optional[str] = ""  # 备注
    desc: Optional[str] = ""  # 长文本描述
    tags: Optional[list[str]] = []  # 标签
    split_wechat: Optional[int] = 0  # 如果非0 或None 则需要去读取用户控件找到另外一个微信


class OpenWechatStage(Stage):
    def __init__(self, stage_serial: int, system_user_id: int = 0):
        super().__init__(stage_serial)
        self.user_id = system_user_id

    def run(self, client: AndroidClient):

        if not client.user_have_package(self.user_id, "com.tencent.mm"):
            raise InitiativeException("未找到手机用户%s的微信" % self.user_id)

        client.shell(f'am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI --user {self.user_id}')  # 一般0是本机机主 也就是主号

        client.context["userid"] = self.user_id

        time.sleep(2)
        # 判断是否被调起了 打开方式的选择
        if client.is_huawei():
            uid, activity = client.get_focus_activity()
            if activity == "com.huawei.android.internal.app/com.huawei.android.internal.app.HwChooserActivity":
                if self.user_id != 0:
                    # 获取到最右边那个微信
                    right_btn = client.get_max_or_min_node("微信", axios="x")
                    if right_btn.rect[0] < (client.get_screen_size()[0] / 2):
                        raise InitiativeException("未在打开方式中找到最右侧的微信")
                    client.device.click(*right_btn.center())
                else:
                    left_btn = client.get_max_or_min_node("微信", axios="x", max_or_min="min")
                    if left_btn.rect[0] > (client.get_screen_size()[0] / 2):
                        raise InitiativeException("未在打开方式中找到最左侧的微信")
                    client.device.click(*left_btn.center())

        try:
            client.wait_until_activity("com.tencent.mm/com.tencent.mm.ui.LauncherUI", timeout=10)
        except Exception as e:
            _, activity = client.get_focus_activity()
            if activity == "com.tencent.mm/com.tencent.mm.plugin.account.ui.WelcomeActivity":
                raise Exception("微信未登录")
            if activity == "com.tencent.mm/com.tencent.mm.plugin.account.ui.LoginPasswordUI":
                raise Exception("微信需要输入密码")

            client.back_to_activity("com.tencent.mm/com.tencent.mm.ui.LauncherUI")

        bottom_node = client.get_max_or_min_node("微信", "y")
        if bottom_node is None:
            raise Exception("未找到微信底部tab")
        if bottom_node.rect[1] < 500:
            raise Exception("下方微信tab未找到")
        bottom_node.click()


# 跳转到添加朋友页面
class GotoAddFriendUiStage(Stage):
    def __init__(self, stage_serial: int):
        super().__init__(stage_serial)

    def run(self, client: AndroidClient):

        client.relative_click(0.93, 0.07)
        #
        # # 找到微信两个字
        # wechat_node = (client.device.xpath("微信") | client.device.xpath("//*[contains(@text, '微信(')]")).get()
        # # 点击+号
        # x, y, w, h = wechat_node.rect
        # displayWidth = client.device.info["displayWidth"]
        # client.device.click(displayWidth * 0.93, y + h * 0.5)
        # 等待添加朋友
        try:
            client.wait_to_click({"text": "添加朋友"})
        except Exception as e:
            client.relative_click(0.93, 0.07)
            client.wait_to_click({"text": "添加朋友"})

        # 这个比较通用
        client.wait_until_found({"text": "雷达加朋友"})

        # 这种方式在微信分身上会失败
        # client.wait_until_activity("com.tencent.mm/com.tencent.mm.plugin.subapp.ui.pluginapp.AddMoreFriendsUI")


# 输入微信号或手机号
class InputWechatIdStage(Stage):
    def __init__(self, stage_serial: int, data: WechatAddFriendData):
        super().__init__(stage_serial)
        self.data = data

    def run(self, client: AndroidClient):
        # 先点击微信号/手机号
        anchor_node = client.device.xpath("%我的微信号%").get()
        x, y, w, h = anchor_node.rect
        client.device.click(x, y - 50)

        client.wait_until_activity("com.tencent.mm/com.tencent.mm.plugin.fts.ui.FTSAddFriendUI")
        # 再次找到输入节点
        content = self.data.tel_phone
        if self.data.tel_phone is None or self.data.tel_phone == "":
            content = self.data.wechat_id
        (client.device.xpath("微信号/手机号") | client.device.xpath("%手机号%")).set_text(content)
        client.adb_input_hide()
        # 等待搜索
        client.wait_to_click({"text": "%搜索:%"})


# 判断是否找到用户
class CheckAddFriendStage(Stage):
    def __init__(self, stage_serial: int):
        super().__init__(stage_serial)

    def run(self, client: AndroidClient):
        not_found_node = (client.device.xpath("该用户不存在")).exists
        if not_found_node:
            raise Exception("未找到用户")
        # 这里有几种可能性
        if client.device.xpath("个人").exists:
            person_node = client.device.xpath("个人").get()
            x, y, w, h = person_node.rect
            client.device.click(x + w / 2, y + h * 2)

        # 判断当前ui是否是有这个人
        client.wait_until_activity("com.tencent.mm/com.tencent.mm.plugin.profile.ui.ContactInfoUI")

        if client.device.xpath("发消息").exists:
            raise Exception("该用户已是好友")

        client.wait_to_click({"text": "添加到通讯录"})

        # 添加好友申请页
        client.wait_until_activity("com.tencent.mm/com.tencent.mm.plugin.profile.ui.SayHiWithSnsPermissionUI")


# 填写申请信息
class InputAddFriendInfoStage(Stage):
    def __init__(self, stage_serial: int, data: WechatAddFriendData):
        super().__init__(stage_serial)
        self.data = data

    def run(self, client: AndroidClient):
        all_input = client.device.xpath("//android.widget.EditText").all()
        Logger.info(f"输入框数量{len(all_input)}")
        if self.data.invite_msg is not None and self.data.invite_msg != "":
            first_node = all_input[0]
            first_node.click()
            client.device.clear_text()  # 清除输入
            client.device.xpath(f'@{first_node.info["resourceId"]}').set_text(self.data.invite_msg[:50])
            client.adb_input_hide()
        if self.data.remark is not None and self.data.remark != "":
            client.device.xpath(f'@{all_input[1].info["resourceId"]}').set_text(self.data.remark[:16])
            client.adb_input_hide()

        if self.data.tags is not None and len(self.data.tags) >= 1:
            # client.wait_to_click({"text": "标签"})
            # 这样做是因为有些可能是二次添加的 已经设置了标签 则会找不到标签
            # 标签的文本会变为已设置的标签
            tags_title_node = client.device.xpath("添加标签与描述").get()
            x, y, w, h = tags_title_node.rect
            client.device.click(w / 2, y + (h * 2))
            for tag in self.data.tags:
                client.device.xpath("%搜索标签%").set_text(tag)
                client.shell("input keyevent 66")
            client.wait_to_click({"text": "保存"})

        client.wait_to_click({"text": "发送"})

        # 发送之后 可能会报出频繁 之类的错误
        client.toast_show()

        # 等���请求发送成功
        client.wait_until_activity("com.tencent.mm/com.tencent.mm.plugin.profile.ui.ContactInfoUI", timeout=20)


class WechatAddFriendTask(PhoneTask):
    def __init__(self,
                 data: Union[WechatAddFriendData, dict] = {},
                 priority: int = 3,
                 unlock_path: Optional[list[Tuple[int, int]]] = [],
                 system_user_id: int = 0,
                 ):
        super().__init__(priority)
        if isinstance(data, dict):
            self.data = WechatAddFriendData(**data)
        else:
            self.data = data
        if self.data is None:
            raise Exception("必须有对应内容")

        if (self.data.tel_phone is None and self.data.wechat_id is None) or (
                self.data.tel_phone == "" and self.data.wechat_id == ""):
            raise Exception("手机号和微信号不能同时为空")
        unlock = UnlockPhoneTask(unlock_path)
        self.stages.append(TaskAsStage(0, unlock))
        self.stages.append(OpenWechatStage(0, system_user_id))
        self.stages.append(SleepStage(1, 2))
        self.stages.append(GotoAddFriendUiStage(1))
        self.stages.append(InputWechatIdStage(2, self.data))
        self.stages.append(SleepStage(3, 5))
        self.stages.append(CheckAddFriendStage(4))
        self.stages.append(InputAddFriendInfoStage(5, self.data))

        self.auto_serial()
        self.set_finnish_callback(self.on_finish)

    def on_finish(self, client: AndroidClient):
        Logger.info("微信添加好友任务结束finish")

        client.back_to_activity("com.tencent.mm/com.tencent.mm.ui.LauncherUI", raise_exception=False)

        # 回到桌面
        client.shell("input keyevent 3")
