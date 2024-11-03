import re
from urllib.parse import urlparse, parse_qs

import requests

from .backend import get_backend
from .client import ClientTask, TaskAsStage, Stage, AndroidClient
from .logger import get_logger
from .task_comm import SleepStage, PressTextStage, WaitTextStage, PressRelativePositionStage
from .task_douyin_publish import OpenAppStage, ClearModalStage
from .task_douyin_user_id import OpenMyBtnStage, OpenSettingDrawerStage, ParseCountsStage
from .task_error import InitiativeException
from .task_unlock_phone import UnlockPhoneTask

Logger = get_logger()


def extract_urls(text):
    # Regular expression to match URLs
    url_pattern = r'https?://[^\s,;:]+'

    # Find all URLs using the regular expression
    urls = re.findall(url_pattern, text)

    return urls[0] if urls else None


def sec_uid_get_info(sec_uid):
    # 通过sec_uid 获取到用户信息
    next_url = f'https://m.douyin.com/web/api/v2/user/info/?reflow_source=reflow_page&sec_uid={sec_uid}'
    response = requests.get(next_url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"},
                            timeout=10)
    response.raise_for_status()
    try:
        body = response.json()
    except Exception as e:
        if response.headers.get("Bdturing-Verify"):
            Logger.error("抖音接口返回验证码", sec_uid)
            raise InitiativeException("抖音接口返回需要验证码")
        Logger.error("抖音接口返回用户信息为空", sec_uid)
        raise Exception("抖音接口返回用户信息为空")
    return body


# 4- 长按复制此条消息，打开抖音搜索，查看TA的更多作品。 https://v.douyin.com/irApF5hX/ 7@8.com :5pm
# 8- 长按复制此条消息，打开抖音搜索，查看TA的更多作品。 https://www.iesdouyin.com/share/user/MS4wLjABAAAAOPTdszkGizxqIjweeeKMx39X0IhufHuZYso2fXVX31RHQaYy4fy2esAg5yUlcgcN?u_code=26j0kf5fi121&did=MS4wLjABAAAAMX8nBPjf_NE3rhVMFebIKnPDaQE_SXtRQlHWVL1nzXYaJs8HcKYZ8NK75jy8FdxB&iid=MS4wLjABAAAAw-FqiH4iByaKkKfPYgyNgnzFhOWvSLFZNzAGc68wIt-BwQjA49ZPMBtEDaokzWe3&with_sec_did=1&sec_uid=MS4wLjABAAAAOPTdszkGizxqIjweeeKMx39X0IhufHuZYso2fXVX31RHQaYy4fy2esAg5yUlcgcN&from_ssr=1&from_aid=1128&timestamp=1723519155&utm_source=copy&utm_campaign=client_share&utm_medium=android&app=aweme 1@7.com :9pm
class ShareLinkGetInfoStage(Stage):
    def __init__(self, stage_serial: int):
        super().__init__(stage_serial)

    def run(self, client: AndroidClient):
        link_text = client.device.clipboard
        if link_text is None:
            raise Exception("剪切板为空")
        if "长按复制" not in link_text:
            raise Exception("分享链接格式错误")
        link = extract_urls(link_text)
        # 判断链接格式
        if 'share/user' in link:
            sec_uid = urlparse(link).path.split("/")[-1]
        else:
            # 发送请求 禁止302
            response = requests.get(link, allow_redirects=False, timeout=10)
            if response.status_code != 302:
                raise Exception("获取跳转url失败")
            # 获取重定向的URL
            redirect_url = response.headers['Location']
            # Parse the URL
            parsed_url = urlparse(redirect_url)

            # Extract the query parameters from the parsed URL
            query_params = parse_qs(parsed_url.query)

            # Get the sec_uid parameter (if present)
            sec_uid = query_params.get('sec_uid', [None])[0]

        body = sec_uid_get_info(sec_uid)
        client.context["sec_uid"] = sec_uid
        client.context["user_info"] = body["user_info"]
        userinfo = body["user_info"]
        client.context["signature"] = userinfo.get('signature', "")  # 签名
        client.context["aweme_count"] = userinfo.get("aweme_count", 0)  # 作品数量

        client.context["is_exception"] = False
        client.context["exception_msg"] = ""

        # 判断是否为自己注销
        if userinfo.get("special_state_info", {}).get("special_state", "") == 1:
            msg = userinfo.get("special_state_info", {}).get("title", "用户已注销")
            client.context["is_exception"] = True
            client.context["exception_msg"] = msg
            raise InitiativeException(msg)
        # 判断是否被禁言惩罚
        punish_remind_info = userinfo.get("punish_remind_info", {})
        content = punish_remind_info.get("prompt_bar", {}).get("content", "")
        if len(content) >= 1:
            ban_type = punish_remind_info.get("ban_type", -1)
            client.context["is_exception"] = True
            client.context[
                "exception_msg"] = f'{punish_remind_info.get("punish_title", "")} {content} ban_type:{ban_type}'
            raise InitiativeException(content)


# 通过分享链接获取用户的sec uid 和用户信息
class GetSelfSecUidTask(ClientTask):
    def __init__(self, priority: int = 3, system_user_id=0, *args, **kwargs):
        super().__init__(priority)
        self.system_user_id = system_user_id
        # 解锁手机
        unlock = UnlockPhoneTask([], back_to_home=False)
        self.stages.append(TaskAsStage(0, unlock))
        self.stages.append(OpenAppStage(1, system_user_id=system_user_id))
        # 清理掉各种弹窗
        self.stages.append(ClearModalStage(3))
        self.stages.append(SleepStage(3, 3))
        # 点击我的
        self.stages.append(OpenMyBtnStage(4))
        self.stages.append(ParseCountsStage(5))
        # 展开设置
        self.stages.append(OpenSettingDrawerStage(5))
        self.stages.append(SleepStage(6, 2))
        # 点击我的二维码
        self.stages.append(PressTextStage(6, "我的二维码"))
        # 等待扫一扫出现
        self.stages.append(WaitTextStage(7, "扫一扫"))
        # 点击右上角相对位置
        self.stages.append(PressRelativePositionStage(8, 0.9, 0.08))
        # 点击复制链接
        self.stages.append(PressTextStage(9, "复制链接"))
        # 这里会发送请求 所以需要等一下
        self.stages.append(SleepStage(10, 1))
        # 从剪切板读取链接并进行转化
        self.stages.append(ShareLinkGetInfoStage(11))
        #
        self.auto_serial()
        self.set_finnish_callback(self.on_finnish)

    def on_finnish(self, client: AndroidClient):
        Logger.info("获取用户sec_uid和用户信息执行结束")
        if "sec_uid" in client.context:
            Logger.info(f"用户sec_uid:{client.context['sec_uid']}")
            # 写入db
            backend = get_backend()
            backend.add_platform_account(
                client.device.serial,
                "抖音",
                client.context["user_info"]["unique_id"],
                client.context["user_info"]["nickname"],
                fans=client.context["fans"],
                like=client.context["like"],
                signature=client.context["signature"],
                work_count=client.context["aweme_count"],
                uid=client.context['sec_uid'],
                is_exception=client.context["is_exception"],
                exception_msg=client.context["exception_msg"],
                system_user_id=self.system_user_id,
            )
            Logger.info("写入数据库成功")
        client.device.app_stop('com.ss.android.ugc.aweme')
