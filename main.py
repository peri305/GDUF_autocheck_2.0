import time
import util
import requests
from yiban import YiBan


def push(bark, err):
    api = "https://api.day.app/%s/易班打卡异常提醒/%s?" % (bark, err)
    send = requests.post(api)


def check(account, password, bark, address):
    yb = YiBan(account, password, address)
    yb.login()
    yb.getHome()
    if yb.submit() == True:
        print("[%s]" % util.get_time(), yb.result_str)
        push(bark, yb.result_str)
    else:
        print("[%s]" % util.get_time(), "%s 打卡成功" % yb.name)


def data_input():
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
                      "这里填你的BARK", util.get_data(i, 4))
            else:
                check(util.get_data(i, 1), util.get_data(i, 2),
                      "这里填你的BARK", "广东省广州市天河区迎福路靠近广东金融学院")
        time.sleep(1)
        i = i+1


def main():
    try:
        data_input()
    except BaseException as errors:
        err = "%s %s" % (yb.account, errors)
        print("[%s]" % util.get_time(), err)
        push(bark, err)
        main()


if __name__ == '__main__':
    main()
