import re

from .client import Stage, AndroidClient, \
    TaskAsStage, get_logger, ClientTask, ClientWaitTimeout

Logger = get_logger()


# https://m.douyin.com/web/api/v2/user/info/?reflow_source=reflow_page&sec_uid=MS4wLjABAAAAOPTdszkGizxqIjweeeKMx39X0IhufHuZYso2fXVX31RHQaYy4fy2esAg5yUlcgcN

class OpenMyBtnStage(Stage):
    def run(self, client: AndroidClient):
        client.device.xpath('我').click()
        try:
            if client.wait_until_activity(
                    "com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.account.business.login.DYLoginActivity",
                    timeout=5):
                # 如果找到了登录框 则说明报错了
                raise Exception("登录框出现 未登录或掉登录了")
        except ClientWaitTimeout as e:
            pass
        (client.device.xpath("我的小程序") | client.device.xpath("我的钱包")).get()


class ParseCountsStage(Stage):
    def run(self, client: AndroidClient):
        # 找到赞

        like_count_node = client.get_neighbour_node("获赞", "up")
        if like_count_node:
            client.context["like"] = int(like_count_node.attrs.get("text", 0))

        fans_count_node = client.get_neighbour_node("粉丝", "up")
        if fans_count_node:
            client.context["fans"] = int(fans_count_node.attrs.get("text", 0))


class OpenSettingDrawerStage(Stage):
    def run(self, client: AndroidClient):
        client.relative_click(0.9, 0.08)
        client.wait_until_found({"text": "抖音创作者中心"})


class PressSettingBtnStage(Stage):
    def run(self, client: AndroidClient):
        client.wait_to_click({"text": "设置"})
        # com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.setting.ui.DouYinSettingNewVersionActivity
        client.wait_until_activity(
            "com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.setting.ui.DouYinSettingNewVersionActivity")


class ScrollToBottomStage(Stage):
    def run(self, client: AndroidClient):
        count_down = 10
        while True:
            if client.device.xpath("//*[contains(@text, 'version')]").exists:
                break
            client.device.swipe_ext("up", scale=0.8)
            count_down -= 1
            if count_down == 0:
                raise Exception("未找到版本信息")


class PressVersionBtnStage(Stage):
    def run(self, client: AndroidClient):
        node = client.device.xpath("//*[contains(@text, 'version')]")
        for i in range(5):
            node.click_nowait()
        if not client.device.xpath("//*[contains(@text, 'UserId')]").wait(timeout=5):
            raise Exception("未点出隐藏信息")


def parse_to_dict(input_string):
    # Regex pattern to match key-value pairs
    pattern = r'(\w+): ([\w\.\-_\(\) ]+)'

    # Find all matches in the input string
    matches = re.findall(pattern, input_string)

    # Convert matches to a dictionary
    parsed_dict = {key: value.strip() for key, value in matches}

    return parsed_dict


class GetUserIdStage(Stage):
    def run(self, client: AndroidClient):
        node = client.device.xpath("//android.widget.TextView[contains(@text, 'UserId')]")
        if not node.exists:
            raise Exception("未找到UserId")
        text = node.get_text()
        parsed_dict = parse_to_dict(text)
        client.context["version"] = parsed_dict


# snssdk1128://
# snssdk1128://user/profile/userId
# snssdk1128://user/profile/2188470837323732
# am start -a android.intent.action.VIEW -d "snssdk1128://user/profile/2188470837323732"
# userId可以从设置 中点击5下 最下面的抖音 version 即可获得
# 未启用
# class GetUserIdTask(ClientTask):
#     def __init__(self, priority: int = 3, unlock_path: Optional[list[Tuple[int, int]]] = []):
#         super().__init__(priority)
#         # 解锁手机
#         unlock = UnlockPhoneTask(unlock_path)
#         self.stages.append(TaskAsStage(0, unlock))
#         self.stages.append(OpenAppStage(1))
#         # 清理掉各种弹窗
#         self.stages.append(ClearModalStage(3))
#         self.stages.append(SleepStage(3, 3))
#         # 点击我的
#         self.stages.append(OpenMyBtnStage(4))
#         self.stages.append(ParseCountsStage(5))
#         # 展开设置
#         self.stages.append(OpenSettingDrawerStage(5))
#         # 点击设置
#         self.stages.append(PressSettingBtnStage(6))
#         # 滚动到底部
#         self.stages.append(ScrollToBottomStage(7))
#         # 点击版本号
#         self.stages.append(PressVersionBtnStage(8))
#         # 获取出用户id
#         self.stages.append(GetUserIdStage(9))
#         self.auto_serial()
