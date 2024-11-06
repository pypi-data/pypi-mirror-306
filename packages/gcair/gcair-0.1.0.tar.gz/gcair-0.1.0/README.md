## 构建前需要安装
pip install setuptools wheel twine  # twine 用于发布包的


## 构建
python setup.py sdist bdist_wheel

## 测试
pytest tests


## 检查是否有错
python setup.py check