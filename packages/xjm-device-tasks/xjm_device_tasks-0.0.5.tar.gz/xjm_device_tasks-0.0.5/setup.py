from setuptools import setup, find_packages
import os

# 获取 setup.py 所在目录的绝对路径
here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 使用绝对路径读取 requirements.txt
with open(os.path.join(here, 'requirements.txt')) as f:
    required = f.read().splitlines()

setup(
    name="xjm_device_tasks",
    version="0.0.5",
    author="23233",
    author_email="",
    description="Android device management and automation tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"xjm_device_tasks": "xjm_publish"},
    packages=["xjm_device_tasks"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=required,
)
