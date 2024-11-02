# *nonebot_reply*
## 简略描述
这是一个随机复读插件,可以通过设置概率的方式来让bot随机复读上一条信息(包括图片).
## 依赖
需求nonebot`2.0`
## 安装与使用
### pip
`pip install nonebot-reply==1.1`
### 使用
请在*.env.prod*文件中加入以下设置:
`group_whitelist = ["",""]`群组白名单,请在""中加入想要启用功能的群组.
`repeat_frequency = `复读频率,在=后添加*数字*(例:需要1/10复读机率,写入10,需要1/5复读几率,写入5)

