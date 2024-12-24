# PySMS780E
## 基于Python3的跨平台LuatOS Air780E短信转邮件平台

**重要提示**

本项目仅限用于**个人目的性质的，接收自用的手机号码的短信**，严禁用于其他任何用途。如有因为正当或不当使用本软件导致的包括但不限于法律问题、人身安全、财产损失等均与本项目无任何关系。

本项目及作者不对项目的使用者做任何背书及任何保证。

这个项目尚处于测试阶段，请勿用于生产环境。**任何因为使用本工具造成的信息泄露、信息丢失等问题，后果自负**

本项目需要配合合宙Air780E LTE Cat.1开发板以及专用固件使用。

专用固件项目：https://github.com/simotsukiyuki/sms_forwarding_uart

# 写入固件

刷入固件请参考合宙官方教程https://wiki.luatos.com/boardGuide/flash.html

注意需要使用上节提到的**专用固件**而不是合宙的官方固件！

*虽然使用官方固件配合上节项目的脚本也可以使用，但是官方固件未屏蔽RNDIS，可能会导致电脑使用手机卡的流量导致损失。*

# 查看端口

刷入固件后建议重启（软/硬件均可）开发板。在开发板的Log里可以看到一个叫做**用户虚拟端口COMx**（x代表具体数字）的端口号，记下来。

> Linux系统下780E系列模块大概率是/dev/ttyACM3。如果不是，请以实际测试为准

# 安装依赖项目

建议**不要使用root**用户！

```
python3 -m venv [你的venv名字]
source ./[你的venv名字]/bin/active
pip3 install zmail==0.2.8 pyserial==3.5
```

# 下载及配置PySMS780E
```
git clone -b main https://github.com/simotsukiyuki/PySMS780E.git
cd ./PySMS780E
nano Config.py
```
NOTE: 当前版本需要打开Config.py文件修改源代码，你可以根据里面的信息进行配置端口及邮箱转发。

具体的配置文件说明已经补充。

# 测试邮箱

```
source ./[你的venv名字]/bin/active
python TestMail.py
```

# 启动软件

## 使用控制台直接启动

建议使用tmux等持久化工具以避免断开SSH时导致软件退出。
```
source ./[你的venv名字]/bin/active
python main.py
```
## 使用systemctl构建为服务（推荐）

1. 创建Unit文件，内容参考：

> nano /usr/lib/systemd/system/pysms780e.service

```
#/usr/lib/systemd/system/pysms780e.service
[Unit]
Description=SMS780E Daemon

[Service]
Type=simple
StartLimitIntervalSec=0
Restart=always
RestartSec=1

ExecStart=/[你的venv名字]/bin/python3 /[你的代码路径]/main.py

PrivateTmp=false

[Install]
WantedBy=multi-user.target
```

2. 注册并启动服务

```
sudo systemctl daemon-reload
sudo systemctl enable pysms780e.service
sudo systemctl start pysms780e.service
```

3. 查看服务状态

```systemctl status pysms780e.service```

```
● pysms780e.service - SMS780E Daemon
     Loaded: loaded (/lib/systemd/system/pysms780e.service; enabled; preset: enabled)
     Active: active (running) since Wed 2024-07-17 14:19:30 CST; 18min ago
   Main PID: 658 (python3)
      Tasks: 2 (limit: 1000)
     Memory: 22.3M
        CPU: 6.397s
     CGroup: /system.slice/pysms780e.service
             ├─ 658 /home/yuki/sms_pyenv/bin/python3 /home/yuki/PySMS780E/main.py
             └─1299 /home/yuki/sms_pyenv/bin/python3 /home/yuki/PySMS780E/main.py

Jul 17 14:19:30 orangepizero3 systemd[1]: Started pysms780e.service - SMS780E Daemon.
Jul 17 14:19:39 orangepizero3 python3[658]: 2024-07-17 14:19:39.047479 > Database Checking.
Jul 17 14:19:39 orangepizero3 python3[658]: 2024-07-17 14:19:39.048444 > Database Checked over.
```

如果看到Active状态为running，则说明启动成功。

# 短信指令

短信指令目前已经并入主分支，但你需要额外配置Config.py才可以正确启用短信指令功能。**请参阅配置Config.py这一节内容**

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
```
smscmd_enable=False # SMS Command Enable / 是否激活短信指令功能，是=True；否=False

smscmd_save_cmdsms=False # Save and forward Command SMS Enable / 是否保存并转发指令短信，是=True；否=False

smscmd_admin_phone="12345678901" # Administrator's Phone Number / 允许接受管理员短信指令的管理号码。只有对应的号码发送过来的短信才会响应短信指令。

smscmd_cmd_split_flag="#" # Split Flag of SMS Command / 指令的分隔符，见后续详细说明

smscmd_cmd_nextsms_countdown=30 # Cold-Down time(seconds) of sending Next SMS / 连续发送短信指令的间隔时间，单位为秒，见后续详细说明

smscmd_command_sendsms="sms780e_sendto" # Command title of sending sms / 发送短信的指令，见后续详细说明

smscmd_command_exit="sms780e_exit" # Command title of stop server / 退出的指令，见后续详细说明
```
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

# 已知问题

1. 测试中使用QQ邮箱在发送邮件时会在发送邮件成功时抛出一个返回码为<code>b'\x00\x00\x00'</code>的SMTPResponseException，并导致进程退出；
  
   进程退出的问题在Commit 38243dd已被修复。
   
   目前使用QQ邮箱进行邮件转发仍会触发此异常并提示邮件发送失败，~~但邮件会正常发出，不影响转发功能的正常使用~~2024年12月测试发现此问题已会导致邮件发送速度极慢且存在发送失败概率。
   
   此为QQ邮箱的问题，测试使用其他邮箱无此情况。因此程序暂无法对此进行修正，请使用其他邮箱进行发送。

   相关情况的参考连接：https://www.vnpy.com/forum/topic/33242-yi-zhi-zheng-chang-fa-de-you-jian-tu-ran-bao-cuo
