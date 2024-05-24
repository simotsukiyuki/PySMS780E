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

# 短信指令

**注意*****短信指令功能尚在测试阶段，不能确保稳定性。请自行决定是否启用该功能。请勿用于生产环境，后果自负***

短信指令目前并未并入主分支，如需使用，请将分支切换到sms_command分支并修改Config.py。

注意：Config.py有**可能被覆盖**，在进行任何操作以前，请先备份！

> git clone -b sms_command https://github.com/simotsukiyuki/PySMS780E.git
>
> cd ./PySMS780E
>
> nano Config.py

sms_command分支的Config.py与当前版本的主分支有所不同，你需要额外配置Config.py才可以正确启用短信指令功能。**请参阅配置Config.py这一节内容**

## 使用方式

目前的短信指令只有两个，分别对应退出程序和使用Air780E内的sim卡发送短信。

以下内容均假设**发送指令的手机号码**为114514,**Air780E内的SIM卡号码**为1919810。

### 退出程序

代码：<code>sms780e_exit</code>

操作：使用手机号码为114514的手机向号码1919810发送一条内容为<code>sms780e_exit</code>的短信。

### 发送短信

代码：<code>sms780e_sendto#[收件人手机号码]#[短信内容]</code>

假设此时Air780E内号码为1919810的sim卡需要向号码为151376666的手机发送一条名为“我要抽瑞克V代”的短信。

操作：使用手机号码为114514的手机向号码1919810发送一条内容为<code>sms780e_sendto#151376666#我要抽瑞克V代</code>的短信。

## 配置Config.py

> smscmd_enable=False # SMS Command Enable / 是否激活短信指令功能，是=True；否=False
> 
> smscmd_save_cmdsms=False # Save and forward Command SMS Enable / 是否保存并转发指令短信，是=True；否=False
> 
> smscmd_admin_phone="12345678901" # Administrator's Phone Number / 允许接受管理员短信指令的管理号码。只有对应的号码发送过来的短信才会响应短信指令。
> 
> smscmd_cmd_split_flag="#" # Split Flag of SMS Command / 指令的分隔符，见后续详细说明
> 
> smscmd_cmd_nextsms_countdown=30 # Cold-Down time(seconds) of sending Next SMS / 连续发送短信指令的间隔时间，单位为秒，见后续详细说明
> 
> smscmd_command_sendsms="sms780e_sendto" # Command title of sending sms / 发送短信的指令，见后续详细说明
> 
> smscmd_command_exit="sms780e_exit" # Command title of stop server / 退出的指令，见后续详细说明

smscmd_enable和smscmd_save_cmdsms顾名思义，不再详细介绍。

### smscmd_admin_phone

此配置项用于指定可以接受管理员短信指令的管理号码。

只有对应的号码发送过来的短信，才会执行短信指令。

例如在上一节中的示例中，你需要将这一变量修改为114514。

### smscmd_cmd_split_flag

此配置为设定分隔符。

在上一节发送短信的示例中，使用了#作为分割短信内容的分隔符。你可以把这个分隔符改成其他的。

比如，如果将#改为了$，则你发送的短信内容也应该是<code>sms780e_sendto$151376666$我要抽瑞克V代</code>。

### smscmd_cmd_nextsms_countdown

此配置为设定连续发送短信的冷却时间。在贤者时间内发送的短信将会被忽略。

此值最小设置为0，但是不可以设置为负数。

### smscmd_command_sendsms

此配置指定了发送短信的指令。

在上一节的短信指令示例中，如果你嫌sms780e_sendto太长，你可以改成其他的，比如改成send。相应的，你发送的短信内容也应该是<code>send#151376666#我要抽瑞克V代</code>。

注意指令冲突！不要和其他指令重复！

### smscmd_command_exit

此配置指定了退出程序的指令。

在上一节的退出指令示例中，如果你嫌sms780e_exit太长，你可以改成其他的，比如改成exit。相应的，你发送的短信内容也应该是<code>exit</code>。

注意指令冲突！不要和其他指令重复！
