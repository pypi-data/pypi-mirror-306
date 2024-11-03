import setuptools
with open("README.md",  "r" , encoding='gbk' , errors='ignore') as fh:
    long_description = fh.read()
setuptools.setup(
    name="kimi_craw",  # 模块名称
    version="1.0.5",  # 当前版本
    author="windheart",  # 作者
    author_email="2916311184@qq.com",  # 作者邮箱
    description="kimi_craw",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    # url="https://github.com/wupeiqi/fucker",  # 模块github地址
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        # 'pillow',
        "requests",
        "qrcode"
    ],
    python_requires='>=3',
)

# 打包上传命令
# 要先删掉dist和build文件夹
# python setup.py sdist bdist_wheel
# twine upload dist/*