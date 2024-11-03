import os
import re
import threading
from typing import Callable, Any, Union, Optional, Tuple, List

from pydantic import BaseModel

from .logger import get_logger
import bs4
import uiautomator2
from bs4 import BeautifulSoup
import time

from .task_error import InitiativeException
from .util import posix_path_join

Logger = get_logger()


def create_network_client(addr):
    return AndroidClient(uiautomator2.connect(addr))


def create_usb_client(serial: str = None):
    return AndroidClient(uiautomator2.connect_usb(serial))


def parse_coordinates(bounds: str):
    """
    Parse bounds string in xml attribute 'bounds' and make a set of coordinates indicates two point on screen.
    :param bounds: bounds string in xml attribute 'bounds', example:[162,36][192,79]
    :return: a set of coordinates indicates two point on screen
    """
    coordinates = []
    temp = ""
    coordinate_flag = False
    for c in bounds:
        if '0' <= c <= '9':
            temp = temp + c
            coordinate_flag = True
        elif coordinate_flag:
            coordinate_flag = False
            coordinates.append(int(temp))
            temp = ""
    x1 = coordinates[0]
    y1 = coordinates[1]
    x2 = coordinates[2]
    y2 = coordinates[3]
    return x1, x2, y1, y2


class ClientWaitTimeout(TimeoutError):
    def __init__(self, target="", timeout=0):
        super().__init__(f'client执行{target}操作超时{timeout}秒')


class PhoneLoginException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class AndroidClient:
    """
    Base client for controlling android devices
    """

    def __init__(self, device: uiautomator2.Device):
        self.device = device
        self.xml = ''
        self.task: Optional[ClientTask] = None
        self.rs: Optional[bs4.ResultSet] = None
        self.occupied = False
        self.xml_interceptors = {}
        self.parser: Optional[BeautifulSoup] = None
        self.unlock_path = []
        self.context = {}
        # 必须要设置这个 才可以读取到toast
        # 升级到3.2.5时 调用这个会报错
        # 实测不设置一样能搞定了
        # self.device.jsonrpc.setToastListener(True)
        # 启动adb键盘 在3.2.5会安装atx 2.4.0 但是只有这样才能正常的输入 直接启动免得任务走到一半需要手工去点击一下确认安装
        self.device.set_input_ime(True)

    def restart_app(self, package_name: str, clear_data=False):
        """
        Restart app by package name. This will reset app state to open state.
        Notice: some apps cannot be started by app_start, use adb shell am instead.
        :param package_name: package name of the app
        :param clear_data: clear app data before open
        :return: None
        """
        self.device.app_stop(package_name)
        if clear_data:
            self.device.app_clear(package_name)
        self.device.app_start(package_name)

    def shell(self, cmd: Union[str, list[str]], su: bool = False, print_ret: bool = False):
        if su:
            ret = self.su_shell(cmd)
        else:
            ret = self.device.shell(cmd)
        if ret.exit_code != 0:
            raise RuntimeError('Shell exit code not zero: {} error:{}'.format(ret.exit_code, ret.output))
        if print_ret:
            print(ret.output)
        return ret

    def adb_input_hide(self):
        self.shell("am broadcast -a ADB_KEYBOARD_HIDE")

    # 获取所有用户 一般系统应用分身就是多个用户
    def get_all_user(self):
        r = self.shell("pm list users").output.strip()
        # 使用正则表达式匹配 UserInfo 结构
        pattern = re.compile(r"UserInfo\{(\d+):([^:]+):\d+\}")

        # 使用字典存储结果
        users = {}

        # 查找所有匹配的内容
        matches = pattern.findall(r)

        # 遍历所有匹配项并填充字典
        for match in matches:
            user_id, user_name = match
            users[int(user_id)] = user_name

        return users

    # 获取用户下所有包名
    def get_user_all_packages(self, userid):
        all_packages = self.shell(f'pm list packages --user {userid}')
        return all_packages.output.strip().replace("package:", "").split('\n')

    # 判断用户下是否有这个包
    def user_have_package(self, userid, package_name):
        all_package = self.get_user_all_packages(userid)
        return package_name in all_package

    def su_shell(self, cmd: Union[str, list[str]]):
        """
        Execute command as root user. Use only on rooted clients.
        """
        if isinstance(cmd, str):
            return self.device.shell(f"su -c {cmd}")
        elif isinstance(cmd, list):
            return self.device.shell(['su', '-c'] + cmd)

    def get_sdcard_real_path(self):
        sd_real_path = self.shell("ls -l /sdcard ").output.strip()
        match = re.search(r'-> (\/.*)', sd_real_path)
        if match:
            return match.group(1)
        return None

    def xpath_find(self, xpath: str):
        return self.device.xpath(xpath).all()

    def xpath_exists(self, xpath: str):
        return self.device.xpath(xpath).exists

    def screen_wakeup(self, timeout=10):
        start_time = time.time()
        while True:
            if self.device.info["screenOn"]:
                break
            current_time = time.time()
            if start_time + timeout < current_time:
                raise ClientWaitTimeout('wakeup', timeout)
            time.sleep(0.1)
            self.device.unlock()

    # 会把"bounds": "[281,259][1037,367]" 解析出来
    # 这个坐标是左上角和右下角的坐标
    # 我们需要解析出来为 x,y 左上角 w,h右下角
    def parse_bounds(self, bounds: str) -> list[int]:
        """
        解析 bounds 属性，将其转换为两个 (x, y) 点的元组。
        """
        match = re.findall(r'\d+', bounds)
        x = int(match[0])
        y = int(match[1])
        w = int(match[2]) - x
        h = int(match[3]) - y
        return [x, y, w, h]

    def toast_show(self, retry_count=5, interval=1, exclude_list=[]):
        count = retry_count
        while count > 0:
            # 发送之后 可能会报出频繁 之类的错误
            try:
                message = self.device.toast.get_message()
            except Exception as e:
                Logger.error("获取toast出错", e)
                message = None
            if message:
                if message in exclude_list:
                    continue
                raise InitiativeException(message)
            count -= 1
            time.sleep(interval)

    def back_to_activity(self, activity: str, max_retry=5, interval=1, raise_exception=True):
        found = False
        for _ in range(max_retry):
            _, activity = self.get_focus_activity()
            Logger.info(f'预期{activity} 当前:{activity}')
            if activity == activity:
                found = True
                break
            self.shell("input keyevent 4")
            time.sleep(interval)

        if not found and raise_exception:
            raise RuntimeError(f'未回退到指定的{activity}页面中')

    def back_to_see_node(self, xpath, max_retry=5, interval=1, raise_exception=True):
        found = False
        for _ in range(max_retry):
            self.shell("input keyevent 4")
            time.sleep(interval)
            if self.device.xpath(xpath).exists:
                found = True
                break

        if not found and raise_exception:
            raise RuntimeError(f'未回退找到指定的元素{xpath}')

    def is_point_inside(self, point: tuple[int, int], bounds: str) -> bool:
        """
        判断给定的点 (x, y) 是否在指定的矩形 bounds 内。
        """
        x, y, w, h = self.parse_bounds(bounds)
        px, py = point
        return x <= px <= x + w and y <= py <= y + h

    def calculate_area(self, bounds: str) -> int:
        """
        计算并返回指定矩形 bounds 的面积。
        """
        _, _, w, h = self.parse_bounds(bounds)
        return w * h

    def get_node_containing_point(self, x: float, y: float, class_name=None) -> Optional[bs4.element.Tag]:
        """
        找到包含给定 (x, y) 点且面积最小的节点。
        """
        self.refresh_xml()
        x = int(x)
        y = int(y)
        smallest_area = float('inf')
        best_node = None

        attrs = {
            'bounds': True
        }
        if class_name:
            attrs['class'] = class_name
        all_nodes = self.parser.find_all(attrs=attrs)
        for node in all_nodes:
            bounds = node.get('bounds')
            text = node.attrs.get("text")
            content_desc = node.attrs.get("content-desc")

            exists_rect = self.is_point_inside((x, y), bounds)
            if exists_rect:
                area = self.calculate_area(bounds)
                if area < smallest_area:
                    smallest_area = area
                    best_node = node
        if best_node is None:
            raise RuntimeError(f'未在坐标 {x} {y} 中找到任何节点')
        return best_node

    def get_neighbour_node(self, xpath, direction: str = "up", class_name=None, offset=25):
        # First, find the target node using xpath
        target_node = self.device.xpath(xpath).get()
        if not target_node:
            return None

        x, y, w, h = target_node.rect

        # Define the search area based on the direction
        if direction == "up":
            target_x = x + w / 2
            target_y = y - offset
        elif direction == "down":
            target_x = x + w / 2
            target_y = y + offset
        elif direction == "left":
            target_x = x - offset
            target_y = y + h / 2
        elif direction == "right":
            target_x = x + w + offset
            target_y = y + h / 2
        else:
            raise ValueError("Invalid direction. Choose 'up', 'down', 'left', or 'right'.")

        return self.get_node_containing_point(target_x, target_y, class_name)

    def is_symbolic_link(self, path: str, su: bool = False) -> bool:
        ret = self.shell(['file', path], su).output.strip()
        if ret == f'{path}: cannot open':
            raise FileNotFoundError(path)
        return ret == f'{path}: symbolic link'

    def mkdir(self, path: str, su: bool = False, exists_ok: bool = False):
        if self.exists(path):
            if not exists_ok:
                raise FileExistsError(path)
        else:
            self.shell(['mkdir', path], su)

    def rmdir(self, path: str, su: bool = False, force: bool = False):
        if not self.exists(path):
            raise FileNotFoundError(path)
        cmd_lst = ['rm', '-r', path]
        if force:
            cmd_lst.insert(1, '-f')
        self.shell(cmd_lst, su)

    def exists(self, path: str, su: bool = False):
        try:
            self.is_file(path, su)
            return True
        except FileNotFoundError:
            return False

    def is_file(self, path: str, su: bool = False) -> bool:
        """
        Test if a path is a file.
        Args:
            path (str): Path to be tested.
            su (bool): Use superuser.
        Returns:
            True if the path is a file, False if it is a directory.
        Raises:
            FileNotFoundError: If the path does not exist.
        """
        # Check if the 'file' command exists on the device
        try:
            self.shell(['command', '-v', 'file'], su)
            file_cmd_exists = True
        except RuntimeError as e:
            file_cmd_exists = False

        if file_cmd_exists:
            # Use 'file' command to check the file type
            ret = self.shell(['file', path], su)
            output = ret.output.strip()
            if ': cannot open' in output:
                raise FileNotFoundError(path)
            if output == f'{path}: symbolic link':
                next_path = self.shell(['readlink', path], su).output.strip()
                if next_path == path:
                    raise RuntimeError(f'Recursive symbolic link detected on path {path}')
                return self.is_file(next_path, su)
            return 'directory' not in output
        else:
            # Fallback to 'ls' command to check if the path exists and is a file
            try:
                ret = self.shell(['ls', '-l', path], su)
                output = ret.output.strip()
                if 'No such file or directory' in output:
                    raise FileNotFoundError(path)
                if output.startswith('l'):
                    next_path = self.shell(['readlink', path], su).output.strip()
                    if next_path == path:
                        raise RuntimeError(f'Recursive symbolic link detected on path {path}')
                    return self.is_file(next_path, su)
                return not output.startswith('d')
            except RuntimeError as e:
                if 'No such file or directory' in str(e):
                    raise FileNotFoundError(path)
                else:
                    raise e

    def is_dir(self, path: str) -> bool:
        return not self.is_file(path)

    def ls(self, path: str, su: bool = False) -> list[str]:
        """
        List files in a directory.
        Raises:
            RuntimeError
        """
        if self.is_file(path, su):
            raise RuntimeError(f'Path {path} is a file.')
        res = []
        for output in self.shell(['ls', path], su).output.split('\n'):
            if output != '':
                res.append(output.strip())
        return res

    def pull(self, src: str, dst: str, su: bool = False, skip_not_found: bool = False) -> None:
        basename = os.path.basename(src)
        try:
            if self.is_file(src, su):
                Logger.info(f'上传的文件:{src}')
                self.device.pull(src, posix_path_join(dst, basename))
            else:
                os.makedirs(posix_path_join(dst, basename), exist_ok=True)
                for file_name in self.ls(src, su):
                    next_path = posix_path_join(src, file_name)
                    self.pull(next_path, posix_path_join(dst, basename), su)
        except FileNotFoundError as e:
            if not skip_not_found:
                raise e

    def push(self, src: str, dst: str, su: bool = False) -> None:
        basename = os.path.basename(src)
        if os.path.isfile(src):
            Logger.info(f'上传的文件:{src}')
            self.device.push(src, posix_path_join(dst, basename))
        else:
            self.mkdir(posix_path_join(dst, basename), su, exists_ok=True)
            for file_name in os.listdir(src):
                next_path = posix_path_join(src, file_name)
                self.push(next_path, posix_path_join(dst, basename), su)

    # 获取出某一个方位最大或最小的那个元素
    def get_max_or_min_node(self, xpath, axios="x", max_or_min="max"):
        all_node = self.get_direction_nodes(xpath, axios)
        if max_or_min == "max":
            return all_node[-1]
        return all_node[0]

    def get_direction_nodes(self, xpath, axios="x"):
        all_node = self.device.xpath(xpath).all()
        if len(all_node) < 1:
            return None
        if axios == "x":
            all_node.sort(key=lambda x: x.rect[0])
        else:
            all_node.sort(key=lambda y: y.rect[1])
        return all_node

    def get_screen_size(self):
        info = self.device.info
        return [info["displayWidth"], info["displayHeight"]]

    def dump_xml(self):
        return self.device.dump_hierarchy()

    def refresh_xml(self):
        self.xml = self.dump_xml()
        self.parser = BeautifulSoup(self.xml, 'xml')
        for when, do in self.xml_interceptors:
            if when(self.parser):
                do(self)

    def find_xml_by_attr(self, attrs) -> bs4.ResultSet:
        if 'text' in attrs:
            value = attrs['text']
            # 构建正则表达式
            if value.startswith('%') and value.endswith('%'):
                pattern = re.compile(re.escape(value.strip('%')))
            elif value.startswith('%'):
                pattern = re.compile(f'{re.escape(value.strip("%"))}$')
            elif value.endswith('%'):
                pattern = re.compile(f'^{re.escape(value.strip("%"))}')
            else:
                pattern = re.compile(f'^{re.escape(value)}$')

            # 自定义过滤函数
            def match_text(tag):
                attrs_text = tag.attrs.get("text", None)
                if attrs_text is None or len(attrs_text) < 1:
                    return False
                return pattern.search(attrs_text)

            self.rs = self.parser.find_all(match_text)
        else:
            self.rs = self.parser.find_all(attrs=attrs)

        return self.rs

    def node_exists(self, attrs) -> bool:
        return len(self.find_xml_by_attr(attrs)) > 0

    def wait_until_finish(self, bool_func, refresh_xml: bool = True, timeout=5, target=""):
        """
        Block current thread until this client reached its destination.
        Args:
            bool_func: Pass in a quick detection lambda function to check if the condition is fulfilled, which will end
            this loop. It accepts only one param in type of AndroidClient.
            refresh_xml: Deside if this client's xml will be refreshed in every loop.
            timeout: Max time to wait on this blocking.
            :param target: 执行目标描述
        """
        start_time = time.time()
        while True:
            if refresh_xml:
                self.refresh_xml()
            if bool_func(self):
                return
            current_time = time.time()
            if start_time + timeout < current_time:
                raise ClientWaitTimeout(target=target, timeout=timeout)
            time.sleep(0.1)

    def click_center(self, coordinates: (int, int, int, int)):
        """
            Click center on a set of coordinates, usually works on simple buttons.
            Args:
                coordinates: (x1, x2, y1, y2)
        """
        x = (coordinates[0] + coordinates[1]) / 2
        y = (coordinates[2] + coordinates[3]) / 2
        self.device.click(x, y)

    def click_xml_node(self, node):
        self.click_center(parse_coordinates(node['bounds']))

    def attr_func(self, attr: dict):
        # 如果attr中有text属性，使用find_xml_by_text方法
        def bool_func(client_: AndroidClient):
            return len(client_.find_xml_by_attr(attr)) > 0

        return bool_func

    def wait_to_click(self, attr: dict, timeout=5, gap=0):
        """
        Use given params to find the right node and click it. This method is used on the most common situations.
        An exception will be thrown if it finds nothing using the given attr param.
        :param gap: the gap time in secs between finding and clicking.
        :param timeout: Max time to wait in secs on this element.
        :param attr: the attribute used on finding xml nodes.
        :return: None
        """

        bool_func = self.attr_func(attr)
        self.wait_until_finish(bool_func, timeout=timeout, target=f"查找{attr}")
        time.sleep(gap)
        self.click_xml_node(self.rs[0])

    def wait_until_found(self, attr: dict, timeout=10):
        target = ','.join(f'{k}={v}' for k, v in attr.items())
        bool_func = self.attr_func(attr)

        self.wait_until_finish(bool_func, timeout=timeout, target=f"查找{target}")

    def relative_click(self, width_offset: float, height_offset: float, double=False):
        displayWidth = self.device.info["displayWidth"]
        displayHeight = self.device.info["displayHeight"]
        if double:
            self.device.double_click(displayWidth * width_offset, displayHeight * height_offset)
        else:
            self.device.click(displayWidth * width_offset, displayHeight * height_offset)

    def get_focus_activity(self):
        response = self.shell(
            "dumpsys window | grep 'mCurrentFocus'")
        output = response.output.strip()
        if output == "":
            return None
        parts = output.split(" ")
        user_id = parts[1].replace("u", "")
        activity = parts[2].replace("}", "")
        return [int(user_id), activity]

    def wait_until_activity(self, activity: str, timeout=10):
        def bool_lambda(client_: AndroidClient):
            user_id, now_focus_activity = self.get_focus_activity()
            # Logger.info(f"当前活动:{now_focus_activity}")
            return now_focus_activity == activity

        self.wait_until_finish(bool_lambda, timeout=timeout, target=f"找到{activity}")

    def run_current_task(self, failure_callback: Callable = None, success_callback: Callable = None,
                         clear_task: bool = True, retries: int = 2):
        attempt = 0
        while attempt < retries:
            try:
                self.task.run(self)
                break  # 成功时退出循环
            except Exception as e:
                if self.task.exception is None:
                    self.task.exception = e
                if isinstance(e, InitiativeException):
                    Logger.info(f"任务被主动中断 中止重试:{e} ")
                    attempt = retries + 1
                else:
                    attempt += 1
                if attempt >= retries:
                    if self.task.is_exception():
                        if failure_callback is not None:
                            failure_callback(self)
                    break  # 最后一次失败后退出循环

        if self.task.is_finished():
            if success_callback is not None:
                success_callback(self)

        if clear_task:
            self.clear_task()

    def run_current_task_async(self, failure_callback: Callable = None, success_callback: Callable = None,
                               clear_task: bool = True):
        threading.Thread(target=self.run_current_task, args=(failure_callback, success_callback, clear_task,)).start()

    def clear_task(self):
        self.task = None
        self.context = {}

    def set_task(self, task):
        self.task = task

    def drag(self, slider: (int, int, int, int), rail: (int, int, int, int)):
        self.device.drag((slider[0] + slider[1]) / 2,
                         (slider[2] + slider[3]) / 2,
                         rail[1],
                         (rail[2] + rail[1]) / 2)

    def drag_node(self, slider, rail):
        self.drag(parse_coordinates(slider['bounds']), parse_coordinates(rail['bounds']))

    def click_phone_center(self, wait_before=0, wait_after=0):
        w, h = self.device.window_size()
        time.sleep(wait_before)
        self.device.click(w / 2, h / 2)
        time.sleep(wait_after)

    def lock(self):
        self.occupied = True

    def unlock(self):
        self.occupied = False

    def is_usable(self):
        return self.task is None or self.task.is_finished() or self.task.is_exception() and not self.lock

    def alive(self):
        return self.device.alive() and self.device.agent_alive()

    def intercept_xml(self, when: Callable[[BeautifulSoup], bool], do: Callable):
        """
        XML interceptors will listen on xml changes and call `do()` when `when()` return True.
        This method is used on handling unexpected jump-outs globally.
        Args:
            when: condition function.
            do: called when condition is fulfilled.
        """
        self.xml_interceptors[when] = do

    # 判断是什么手机

    def is_xiaomi(self):
        return self.shell("getprop ro.product.manufacturer").output.strip() == "Xiaomi"

    def get_miui_version(self):
        return self.shell("getprop ro.miui.ui.version.name").output.strip()

    def is_huawei(self):
        return self.shell("getprop ro.product.manufacturer").output.strip() == "HUAWEI"

    def get_huawei_version(self):
        return self.shell("getprop ro.build.version.emui").output.strip()

    def clear_xml_interceptors(self):
        """
        Clear all xml interceptors.
        """
        self.xml_interceptors = {}


class PublishClient(AndroidClient):
    """
    Client for publishing content on social media.
    """

    def __init__(self, device: uiautomator2.Device):
        super().__init__(device)


class Stage:
    """
    Base abstract class for a single step in a task.
    """

    def __init__(self, stage_serial: int):
        self.stage_serial = stage_serial

    def run(self, client: AndroidClient):
        pass

    def get_serial(self):
        return self.stage_serial


class CallbackWaitTimeoutException(TimeoutError):
    def __init__(self, stage_serial):
        super().__init__(f"Wait too long on this callback. Stage:{stage_serial}")


class InvalidStageSerialException(Exception):
    def __init__(self, stage):
        super().__init__(f"Invalid stage serial for stage '{type(stage).__name__}'."
                         "Using a wrong stage serial can cause unexpected execution sequence for stages in a task."
                         "Assign valid stage serial in [0, n-1]")


class ClientTask:
    def __init__(self, priority: int = 3):
        self.stages = list[Stage]()
        self.current_stage = -1
        self.finished = False
        self.exception: Optional[Exception] = None
        self.success_callback: Optional[Callable] = None
        self.fail_callback: Optional[Callable] = None
        self.finish_callback: Optional[Callable] = None
        self.priority = priority
        self.sub_task = False
        self.clear_interceptors = True
        # 数据库条目信息
        self.db_info = None
        # 注入的额外信息
        self.meta_data = None
        # 若有上传 则有上传放置的位置
        self.upload_local_files = []
        self.upload_remote_files = []

    def run(self, client: AndroidClient):
        try:
            # if self.fail_callback is None and not self.sub_task:
            #     warnings.warn(f'Handler for task {type(self).__name__} has not been implemented yet.'
            #                   'This may cause a crash when using manager to dispatch tasks.')
            Logger.info(f'[{client.device.serial}] 执行{type(self).__name__}任务 有{len(self.stages)}个序列')
            for i, stage in enumerate(self.stages):
                Logger.info(
                    f'[{client.device.serial}] 执行{type(self).__name__}任务 [{i + 1}]{type(stage).__name__}序列 开始执行')
                self.current_stage = i
                try:
                    stage.run(client)
                    Logger.info(
                        f'[{client.device.serial}] 执行{type(self).__name__}任务 [{i + 1}]{type(stage).__name__}序列 执行成功')
                except Exception as e:
                    Logger.info(
                        f'[{client.device.serial}] 执行{type(self).__name__}任务 [{i + 1}]{type(stage).__name__}序列 执行失败 错误:{e}')
                    self.exception = e
                    if self.fail_callback is not None:
                        if not self.fail_callback(client, self, e):
                            break
                    else:
                        client.clear_xml_interceptors()
                        raise e
            self.finished = True
            if self.clear_interceptors:
                client.clear_xml_interceptors()
            if self.success_callback is not None:
                self.success_callback(client, self)
        except Exception as e:
            Logger.error(f'[{client.device.serial}] 执行{type(self).__name__}任务 执行失败')
            raise e
        finally:
            Logger.info(f'[{client.device.serial}] 执行{type(self).__name__}任务 执行流程结束')
            if self.finish_callback is not None:
                self.finish_callback(client)

    def __lt__(self, other):
        return self.priority < other.priority

    def get_stage(self):
        return self.current_stage

    def is_going(self):
        return -1 < self.current_stage < len(self.stages) and not self.is_exception()

    def is_finished(self):
        return self.finished

    def is_exception(self):
        return self.exception is not None

    def append(self, stage: Stage):
        if len(self.stages) != stage.stage_serial:
            raise InvalidStageSerialException(stage)
        self.stages.append(stage)

    def set_callback(self, callback: Callable[[AndroidClient, Any], None]):
        """
        This method set callback for the task, it will be called when a task is finished successfully.
        Implement a function with sign [(AndroidClient, ClientTask) -> None] to accept callback.
        """
        self.success_callback = callback

    def set_finnish_callback(self, callback: Callable[[AndroidClient, Any], None]):
        """
        This method set callback for the task, it will be called when a task is finished successfully.
        Implement a function with sign [(AndroidClient, ClientTask) -> None] to accept callback.
        """
        self.finish_callback = callback

    def set_handler(self, handler: Callable[[AndroidClient, Any, Exception], bool]):
        """
        This method set callback for the task, it will be called when a task is interrupted by an exception.
        Implement a function with sign [(AndroidClient, ClientTask, Exception) -> bool] to handle exception.
        """
        self.fail_callback = handler

    def clear_self(self):
        self.current_stage = -1
        self.exception = None
        self.finished = False
        self.upload_local_files = []
        self.upload_remote_files = []

    def shift_down_priority(self):
        self.current_stage = -1
        self.exception = None
        self.finished = False
        self.priority += 1

    def auto_serial(self):
        for i, stage in enumerate(self.stages):
            stage.stage_serial = i


class PublishData(BaseModel):
    id: str  # 数据的id 必传
    video_url: Optional[str] = None  # 视频的下载url
    cover_url: Optional[str] = None  # 预览图的下载url
    local_video_path: Optional[str] = None  # 本地视频路径
    local_cover_path: Optional[str] = None  # 本地预览图
    title: Optional[str] = None  # 标题 可选 20个字内 小红书可需要
    wenan: Optional[str] = None  # 文案 适合短内容
    content: Optional[str] = None  # 正文 适合长内容
    topic: Optional[list[str]] = []  # 话题
    position: Optional[str] = ""  # 地理位置


class PublishTask(ClientTask):
    """
    Base abstract class for a publishing-type task
    """

    def __init__(self, priority: int, data: Union[PublishData, dict]):
        super().__init__(priority)
        if isinstance(data, dict):
            self.data = PublishData(**data)
        else:
            self.data = data


class LoginTask(ClientTask):
    """
    Base abstract class for logining on apps.
    """
    pass


class PhoneTask(ClientTask):
    """
    Base abstract class for using phone to login on apps.
    """
    pass


class PasswordLoginTask(LoginTask):
    """
    Base abstract class for using password to login on apps.
    """

    def __init__(self, account: str, password: str):
        """
        :param account: Can be username or phone number, depends on real situations.
        :param password: Password used to log in on apps.
        """
        self.account = account
        self.password = password
        super().__init__()


class PhoneLoginTask(LoginTask):
    """
    Base abstract class for using phone verify-code to login on apps.
    """

    def __init__(self, phone: str):
        """
        :param phone: User phone number
        """
        self.phone = phone
        self.code = None
        super().__init__()

    def get_code(self) -> str:
        return self.code

    def send_captcha(self, captcha):
        self.code = captcha
        pass


class StatisticTask(ClientTask):
    def __init__(self):
        super().__init__()
        self.statistic = None

    def statistic_callback(self, statistic: dict):
        self.statistic = statistic


class WaitCallBackStage(Stage):
    def __init__(self, stage_serial: int, max_wait_time: float, callback: Callable[[], str],
                 task_callback: Callable[[str], None]):
        self.max_wait_time = max_wait_time
        self.callback = callback
        self.task_callback = task_callback
        self.res = None
        super().__init__(stage_serial)
        self.signal_terminate = False

    def get_code_wrapper(self):
        c = None
        while c is None:
            c = self.callback()
            time.sleep(0.05)
            if self.signal_terminate:
                return
        self.task_callback(c)

    def terminate(self):
        self.signal_terminate = True

    def run(self, client: AndroidClient):

        t = threading.Thread(target=self.get_code_wrapper)
        t.start()
        current_wait_time = 0.0
        while True:
            if not t.is_alive():
                break
            else:
                time.sleep(0.1)
                current_wait_time += 0.1
                if current_wait_time > self.max_wait_time:
                    self.terminate()
                    raise CallbackWaitTimeoutException(self.stage_serial)


class StatisticFetcher(ClientTask):
    def __init__(self):
        super().__init__()
        pass


class TaskAsStage(Stage):
    """
    Use task as a stage. With this, you can combine tasks dependent on each others together.
    """

    def __init__(self, stage_serial: int, task: ClientTask):
        super().__init__(stage_serial)
        self.task = task
        self.task.sub_task = True

    def run(self, client: AndroidClient):
        self.task.run(client)
        if self.task.is_exception():
            raise self.task.exception


class CombinedSequentialTask(ClientTask):
    """
    Now you can execute sequential tasks dependent on each other together using this combined task.
    This is to assure that multiple tasks can be executed sequentially on same device when using manager.
    :example:  task = CombinedSequentialTask(TaskA(), TaskB(), TaskC())
    """

    def __init__(self, *args):
        super().__init__()
        for i, task in enumerate(args):
            self.append(TaskAsStage(i, task))


class StopAppStage(Stage):
    def __init__(self, stage_serial: int, pkg_name: str):
        super().__init__(stage_serial)
        self.pkg_name = pkg_name

    def run(self, client: AndroidClient):
        client.device.app_stop(self.pkg_name)


class StartAppStage(Stage):
    def __init__(self, stage_serial: int, pkg_name: str):
        super().__init__(stage_serial)
        self.pkg_name = pkg_name

    def run(self, client: AndroidClient):
        client.device.app_start(self.pkg_name)


class ClearAppStage(Stage):
    def __init__(self, stage_serial: int, pkg_name: str):
        super().__init__(stage_serial)
        self.pkg_name = pkg_name

    def run(self, client: AndroidClient):
        client.device.app_clear(self.pkg_name)
