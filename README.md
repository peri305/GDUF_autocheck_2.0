<h1 align="center">

GDUF_autocheck_2.0

</h1>

**广东金融学院易广金健康打卡**
- [x] 支持多人打卡👨‍👩‍👧‍👧
- [x] 支持Bark通知打卡结果💬
- [x] 默认地址是校本部🏫
- [x] 需要自己部署服务器✔

## 前提准备
- 在服务器上cd到你存放该项目的目录
- 在```data.xlsx```中填好相关信息

|account|password|bark|address|
|:-|:-|:-|:-|
|账号1|密码1|BARK1(可留空)|地址1(可留空)|
|账号2|密码2|BARK2(可留空)|地址2(可留空)|

- 备注：<br>
①地址项可留空，留空则默认校本部,可用作放假回家自定义地址<br>
②BARK推送生效的前提是在```main.py```中填入你的主BARK<br>
③在```data.xlsx```中留空的BARK当打卡失败时会向主BARK用户发送提醒<br>
④BARK的Value填入的是在你的Bark客户端里得到```https://api.day.app/XXXXXXXXXXXXXXXXXXXXXX```后面的那串字符<br>
⑤添加BARK这一步为可选步骤（非必要），不添加不会影响打卡，只是当打卡失败时不会向手机推送失败提醒<br>
⑥BARK获取教程：<br>
![image](https://github.com/feizao67/GDUF_autocheck/blob/main/如何获取BARK.jpg)

## 安装必要模块
- 运行如下代码<br>
```pip install -r requirements.txt```

## 启动
- 运行如下代码<br>
```python ./main.py```

## 与我联系
- 有任何问题可以提交[issues](https://github.com/feizao67/GDUF_autocheck_2.0/issues/new)  
- QQ交流群：[550758147](https://qm.qq.com/cgi-bin/qm/qr?k=NM9kxBkkvWsNiKx-4y0IzzzpaaXbjGOx&jump_from=webapi)


## 许可
本项目以 GPL-3.0 协议开源，详情请见 [LICENSE](LICENSE) 文件。
