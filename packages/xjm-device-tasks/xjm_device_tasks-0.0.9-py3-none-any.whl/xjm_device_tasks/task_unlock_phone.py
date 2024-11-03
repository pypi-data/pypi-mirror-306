from typing import Optional, Tuple

from .client import Stage, AndroidClient, PhoneTask, ClientWaitTimeout


class BackToHomeException(Exception):
    def __init__(self, device_name: str):
        super().__init__(f'{device_name} 不在系统首页')


# 唤起手机
class WalkPhoneStage(Stage):
    def __init__(self, stage_serial: int):
        super().__init__(stage_serial)

    def run(self, client: AndroidClient):
        client.screen_wakeup()
        client.refresh_xml()

        if client.is_huawei():
            try:
                if (client.device.xpath("使用指纹或上滑解锁") | client.device.xpath("上滑解锁")).exists:
                    client.device.swipe_ext("up")
            except ClientWaitTimeout as e:
                return
        if client.is_xiaomi():
            try:
                client.wait_until_found({"resource-id": "com.android.systemui:id/wallpaper_des"})
                client.device.swipe_ext("up")
            except ClientWaitTimeout as e:
                return


# 滑块解锁手机输入
class SliderUnlockStage(Stage):
    def __init__(self, stage_serial: int, unlock_path: Optional[list[Tuple[int, int]]] = []):
        super().__init__(stage_serial)
        self.unlock_path = unlock_path

    def run(self, client: AndroidClient):
        if len(self.unlock_path) == 0:
            return
        try:
            client.wait_until_found({'text': "绘制您的图案"})
            client.device.swipe_points(self.unlock_path, 0.3)
        except ClientWaitTimeout as e:
            return


# 返回到手机系统桌面
class BackToSystemHomeStage(Stage):
    def __init__(self, stage_serial: int):
        super().__init__(stage_serial)

    def run(self, client: AndroidClient):
        currentPackageName = ""
        if client.is_huawei():
            currentPackageName = "com.android.systemui"
        elif client.is_xiaomi():
            currentPackageName = "com.miui.home"
        if client.device.info["currentPackageName"] != currentPackageName:
            client.shell("input keyevent 3")


# 弹出usb连接方式的选项关闭
class CloseUsbConnectStage(Stage):
    def __init__(self, stage_serial: int):
        super().__init__(stage_serial)

    def run(self, client: AndroidClient):
        try:
            client.wait_until_found({'text': "仅充电"})
            client.wait_to_click({'text': "取消"})
        except ClientWaitTimeout as e:
            return


# 判断是否在系统桌面上了
class IsOnSystemHomeStage(Stage):
    def __init__(self, stage_serial: int):
        super().__init__(stage_serial)

    def run(self, client: AndroidClient):
        if client.is_huawei():
            if client.device.info["currentPackageName"] == "com.android.systemui":
                return
        elif client.is_xiaomi():
            if client.device.info["currentPackageName"] == "com.miui.home":
                return
        raise BackToHomeException(client.device.serial)


# 解锁手机并回到桌面 关闭掉其他干扰因素
class UnlockPhoneTask(PhoneTask):
    def __init__(self, unlock_path: Optional[list[Tuple[int, int]]] = [], back_to_home=True):
        super().__init__(priority=1)
        self.unlock_path = unlock_path
        self.append(WalkPhoneStage(0))
        self.append(SliderUnlockStage(1, unlock_path))
        self.append(CloseUsbConnectStage(2))
        if back_to_home:
            self.append(BackToSystemHomeStage(3))
        self.auto_serial()
