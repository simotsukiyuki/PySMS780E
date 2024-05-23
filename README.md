# PySMS780E
## 【测试项目】基于Python的跨平台LuatOS Air780E短信接收客户端

**重要提示**

*这个项目还处于测试阶段，**请勿用于生产环境，后果自负***

*该程序在Linux/MacOS系统、以及树莓派等各种ARM/RISCV开发板上的运行效果及稳定性尚不明确，请自行测试。*

本项目需要配合合宙Air780E LTE Cat.1开发板以及专用固件使用。
专用固件项目：https://github.com/simotsukiyuki/sms_forwarding_uart

# 写入固件

刷入固件请参考合宙官方教程https://wiki.luatos.com/boardGuide/flash.html。
注意需要使用上节提到的**专用固件**而不是合宙的官方固件！
*虽然使用官方固件配合上节项目的脚本也可以使用，但是官方固件未屏蔽RNDIS，可能会导致电脑使用手机卡的流量导致损失。*

# 查看端口

刷入固件后建议重启（软/硬件均可）开发板。在开发板的Log里可以看到一个叫做**用户虚拟端口COMx**（x代表具体数字）的端口号，记下来。

> Linux系统下780E系列模块大概率是/dev/ttyACM3。如果不是，请以实际测试为准

# 安装依赖项目

建议**不要使用root**用户！

> python3 -m venv [YOUR_VENV_NAME]
> 
> source ./[YOUR_VENV_NAME]/bin/active
> 
> pip3 install zmail==0.2.8 pyserial==3.5

# 下载及配置PySMS780E

> git clone -b main https://github.com/simotsukiyuki/PySMS780E.git
>
> cd ./PySMS780E
>
> nano Config.py

NOTE: 当前版本需要打开Config.py文件修改源代码，你可以根据里面的信息进行配置端口及邮箱转发。

具体的配置文件说明已经补充。

# 测试邮箱

> source ./[YOUR_VENV_NAME]/bin/active
> 
> python TestMail.py

# 启动软件

建议使用tmux等持久化工具以避免断开SSH时导致软件退出。

> source ./[YOUR_VENV_NAME]/bin/active
> 
> python main.py
