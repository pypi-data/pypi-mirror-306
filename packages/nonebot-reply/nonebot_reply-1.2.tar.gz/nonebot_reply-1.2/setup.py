import setuptools #导入setuptools打包工具
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="nonebot_reply", # 用自己的名替换其中的YOUR_USERNAME_
    author="hriyel",    #作者，可以写自己的姓名
    author_email="1249781871@qq.com",    #作者联系方式，可写自己的邮箱地址
    description="nonebot复读插件",#包的简述
    url="https://github.com/hriyel/nonebot_reply.git",    #自己项目地址，比如github的项目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',    #对python的最低版本要求
)
