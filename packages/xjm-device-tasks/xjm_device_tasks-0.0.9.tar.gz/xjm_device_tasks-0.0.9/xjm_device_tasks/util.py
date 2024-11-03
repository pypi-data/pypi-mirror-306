import pathlib


def posix_path_join(*args):
    return str(pathlib.PurePosixPath(*args))


def singleton(cls):
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance


# 输入文案和tag
def combine_with_hash(tags: list[str]) -> str:
    # 使用列表推导将每个字符串前面加上 '#'
    hashed_tags = [f"#{tag}" for tag in tags]
    # 将列表中的字符串用空格连接起来
    result = " ".join(hashed_tags) + " "
    return result
