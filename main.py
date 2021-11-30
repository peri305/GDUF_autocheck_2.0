import util
import requests
from yiban import YiBan


def push(bark, err):
    api = "https://api.day.app/%s/易班打卡异常提醒/%s?" % (bark, err)
    send = requests.post(api)


def check(account, password, bark, address):
    t = 1
    while t <= 3:
        try:
            yb = YiBan(account, password, address)
            yb.login()
            yb.getHome()
            if yb.submit() == True:
                print(util.get_time(), "[第%s次执行] %s" % (t, yb.result_str))
                push(bark, yb.result_str)
                t = 5
            else:
                print(util.get_time(), "[第%s次执行] %s 打卡成功" % (t, yb.name))
                t = 5
        except Exception as errors:
            err = "[第%s次执行] %s %s" % (t, yb.account, errors)
            print(util.get_time(), err)
            push(bark, err)
            t += 1


def main():
    i = 2
    while i <= util.get_rows():
        if util.get_data(i, 3) is not None:
            if util.get_data(i, 4) is not None:
                check(util.get_data(i, 1), util.get_data(i, 2),
                      util.get_data(i, 3), util.get_data(i, 4))
            else:
                check(util.get_data(i, 1), util.get_data(i, 2),
                      util.get_data(i, 3), "广东省广州市天河区迎福路靠近广东金融学院")
        else:
            if util.get_data(i, 4) is not None:
                check(util.get_data(i, 1), util.get_data(i, 2),
                      "这里替换主（帮别人打卡的管理员的）BARK", util.get_data(i, 4))
            else:
                check(util.get_data(i, 1), util.get_data(i, 2),
                      "这里替换主（帮别人打卡的管理员的）BARK", "广东省广州市天河区迎福路靠近广东金融学院")
        i += 1


if __name__ == '__main__':
    main()
