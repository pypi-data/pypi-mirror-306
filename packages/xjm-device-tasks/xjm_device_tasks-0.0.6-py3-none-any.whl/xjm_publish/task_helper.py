# 同步下载 传入文件夹
import pathlib
from urllib.parse import urljoin, urlparse
import os
import requests


def url_extract_filename(url):
    parsed_url = urlparse(url)
    return os.path.basename(parsed_url.path)


def get_posix_directory(path: str) -> str:
    posix_path = pathlib.PurePosixPath(path)
    return str(posix_path.parent)


# 同步下载文件
# 传入下载的url和保存的文件夹路径
def sync_download_file(url, save_path):
    # 确保保存的文件夹存在
    directory = os.path.dirname(save_path)
    os.makedirs(directory, exist_ok=True)
    # 从URL中提取文件名
    filename = url_extract_filename(url)

    # 发送GET请求
    response = requests.get(url, stream=True, timeout=10)

    # 检查请求是否成功
    if response.status_code == 200:
        # 打开文件进行写入
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        return save_path, filename
    else:
        response.raise_for_status()
