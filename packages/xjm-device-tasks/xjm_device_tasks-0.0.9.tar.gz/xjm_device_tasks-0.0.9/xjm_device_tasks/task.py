from .task_douyin_last_work_count import GetDouyinFirstPageCountTask
from .task_douyin_publish import DouyinVideoPublishTask
from .task_douyin_sec_uid import GetSelfSecUidTask
from .task_douyin_update_signature import DouyinUpdateSignatureTask
from .task_wechat_add_friend import WechatAddFriendTask
from .task_wechat_info import WechatInfoTask
from .task_xhs_publish import XhsVideoPublishTask


class All_Task:
    task_mapping = {
        "douyin_publish": DouyinVideoPublishTask,
        "douyin_userinfo": GetSelfSecUidTask,
        "douyin_update_signature": DouyinUpdateSignatureTask,
        "xhs_publish": XhsVideoPublishTask,
        "wechat_add_friend": WechatAddFriendTask,
        "wechat_info": WechatInfoTask,
        "douyin_work_view_get": GetDouyinFirstPageCountTask,
    }

    task_define = [
        {
            "id": "douyin_publish",
            "name": "抖音发布作品",
            "data_type": "PublishData",
            "show_automate": True,
            "show_task": True,
            "enable": True,
            "need_video": True,
            "need_form": True,
        },
        {
            "id": "douyin_work_view_get",
            "name": "抖音作品浏览量获取",
            "show_automate": False,
            "show_task": True,
            "enable": True,
            "need_video": False,
            "need_form": False,
        },
        {
            "id": "douyin_userinfo",
            "name": "抖音用户信息同步",
            "show_automate": False,
            "show_task": True,
            "enable": True,
            "need_video": False,
            "need_form": False,
        },
        {
            "id": "douyin_update_signature",
            "name": "抖音更新签名",
            "data_type": "DyUpdateSignature",
            "show_automate": True,
            "show_task": True,
            "enable": True,
            "need_video": False,
            "need_form": True,
        },
        {
            "id": "xhs_publish",
            "name": "小红书发布作品",
            "data_type": "PublishData",
            "show_automate": True,
            "show_task": True,
            "enable": True,
            "need_video": True,
            "need_form": True,
        },
        {
            "id": "wechat_add_friend",
            "name": "微信添加好友",
            "show_automate": True,
            "show_task": True,
            "data_type": "WechatAdd",
            "enable": True,
            "need_video": False,
            "need_form": True,
        },
        {
            "id": "wechat_info",
            "name": "微信用户信息同步",
            "show_automate": False,
            "show_task": True,
            "data_type": "WechatInfo",
            "enable": True,
            "need_video": False,
            "need_form": False,
        },
    ]

    @staticmethod
    def get_task(name, params):
        task_class = All_Task.task_mapping.get(name)
        if task_class:
            return task_class(**params)
        return None

    @staticmethod
    def get_task_define(name):
        for task in All_Task.task_define:
            if task["id"] == name:
                return task
        return None

    @staticmethod
    def have_task(name):
        return name in All_Task.task_mapping
