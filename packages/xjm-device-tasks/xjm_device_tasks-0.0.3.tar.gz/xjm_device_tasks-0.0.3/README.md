# XJM Publish

私有任务执行包，仅用于内部分发。

## 安装方法

### 方式1：直接从zip安装
1. 下载 XJM Publish 的 zip 包文件（例如：`xjm_publish.zip`）

2. 使用 Python 的 zipimport 方式导入：
```python
import zipimport
importer = zipimport.zipimporter('xjm_publish.zip')
xjm_publish = importer.load_module('xjm_publish')

```

python -m build
python -m twine upload dist/*

git tag v0.0.2
git push origin v0.0.2