from setuptools import setup, find_packages

setup(
    name="duoyinfixer",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pypinyin",  # 依赖项后加逗号
    ],
    author="LY",  # 添加作者信息
    description="替换句子中的多音字，防止文字配音中因为多音字而出现问题",  # 添加描述
    package_data={
        '': ['*.json'],  # 包含所有目录下的 JSON 文件
    },
)