#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    此脚本用于 py 打包和分发工具 `setuptools`。

    主要用来定义如何【安装】和【分发】此 py 项目。

    `setuptools` 是 py 的一个库，它旨在简化打包和分发 py 项目的过程。

    `setuptools` 库官方文档地址：
    【https://setuptools.pypa.io/en/latest/】

    它提供了一系列命令和工具，使开发者能够轻松创建可重用的 py 包，
    并管理它们的依赖关系、版本、发布等。

    `setuptools` 是 `distutils` 的增强版，它在原有基础上增加许多新特性和功能。

    它由 PEP 517 和 PEP 518 标准支持，该标准定义 py 项目的构建要求。

    随着时间推移，`setuptools` 已经成为 py 包创建和管理的事实标准。

    `setuptools` 库主要功能：
        - 安装包：允许用户安装和卸载 py 包。

        - 依赖关系管理：自动处理包依赖项，并确保在安装包时自动下载需要的依赖包。

        - 打包和分发：提供工具来轻松打包 py 代码，并将其分发给其他用户。
                   这通常是通过创建 `.egg` 或 `.wheel` 文件完成的。

        - 版本管理：确保可以为软件包指定版本号以及在需要时指定最小或确切的依赖版本。

        - 扩展构建：针对一些需要编译 C 语言扩展等复杂情况提供支持。

        - 测试支持：集成设置测试套件并运行测试用例的能力。

        - 生成脚本：允许自动创建可以调用软件包中函数的命令行脚本。

        - 声明性配置：使用 `setup.cfg` 或 `pyproject.toml` 文件对项目进行配置，
                   而不是全部通过编写 `setup.py` 脚本来完成。

    使用 `setuptools` 创建一个新项目一般会涉及以下步骤：
        - 创建 `setup.py` 文件，在其中定义项目信息
          （比如项目名、版本、描述等）以及任何相关依赖项。

        - 可选地使用其他配置文件如 `setup.cfg` 或
          `pyproject.toml` 来进一步细化设置（例如定义元数据或选项）。

        - 使用 `setuptools` 提供的命令
          （如 `python setup.py sdist bdist_wheel`）来打包项目。

    随着 py 包管理器 pip 的成熟以及 `wheel` 格式的广泛接受，
    现代 py 打包流程往往更倾向于使用这些工具而非直接操作 `setuptools`。

    不过，`setuptools` 仍然是整个生态系统中一个非常重要且不可或缺的组成部分。

    注意：本文档中出现的 "py"，如无特殊说明，则指代 "Python"。
"""
import os
from setuptools import setup, find_packages

# 初始化 `reqs` 为空列表以防 `requirements.txt` 不存在
reqs = []
# 初始化 `long_description` 为空字符串
long_description = ""

if os.path.exists("requirements.txt"):
    with open(
            file="requirements.txt",
            mode="r",
            encoding="utf-8"
    ) as reqs_file:
        reqs = [
            req.strip()
            for req in reqs_file.readlines()
        ]

if os.path.exists("README.rst"):
    with open(
            file="README.rst",
            mode="r",
            encoding="utf-8"
    ) as description_file:
        long_description = description_file.read()

setup(
    # 指定包的【名称】
    # 在 PyPI 或其他索引服务器上应该是唯一的
    name="wxapis",
    # 给出包的【简短描述】
    description="企业微信服务端 API 操作库。",
    # 提供一个【详细描述】
    long_description=long_description,
    # 指定包描述的【内容类型】
    # 包的长描述（long description）是
    # 用 `reStructuredText` 格式编写的
    long_description_content_type="text/x-rst",
    # 指定软件包的【作者名称】
    author="gary",
    # 指定作者的【电子邮件地址】
    author_email="mepmb@sina.com",
    # 明确列出哪些【平台】适用这个软件包
    # 以便用户和自动化工具知道【兼容性信息】
    platforms=["Linux", "Windows"],
    # 定义映射字典
    # 告诉 `setuptools` 在哪里找到
    # 【源代码文件】来构建 py 包
    # 字典中的【键】是【包名称】，【空字符】串键表示【根包】
    # 【值】是相应【源代码所在目录路径】
    # "." 表示当前目录
    package_dir={"": "."},
    # 使用 `setuptools` 提供的 `find_packages()` 函数
    # 自动查找并包含所有应该被打包为部分安装包的子目录
    # （通常是那些含有 `__init__.py` 文件的目录）
    packages=find_packages(),
    # 直接指定版本号
    version="1.0.9-dev",
    # 配置涉及到 `setuptools_scm` 插件
    # 它使用源码管理（SCM）系统（如 git）来发现项目版本
    use_scm_version={
        "relative_to": __file__,
        "local_scheme": "no-local-version"
    },
    # 列出在运行时需要满足的【依赖项】
    # 确保在安装此软件之前这些依赖项也将被安装
    install_requires=reqs,
    # 列表中指定要在 setup 脚本运行之前要安装好的依赖项
    setup_requires=["setuptools_scm"],
    # `entry_points` 是一种【声明式】方式
    # 来创建【可执行脚本】和【插件系统】
    entry_points={
        # 使用户可以通过【命令行】直接运行某些函数
        # 而不必通过 py 解释器
        "console_scripts": [
            "smsg = wxapis.smsg:main",
        ]
    },
)
