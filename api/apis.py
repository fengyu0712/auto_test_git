# coding: utf-8
from scripts.init_env import http_host
import requests
from tools.mylog import Logger
from urllib import parse

log = Logger()  # 初始化日志对象


class Api(object):

    # 新增方法,获取设备状态
    def post(self, mid):
        try:
            headers = {"Content-Type": "application/json "}
            params = {"mid": "%s" % mid}
            device_host = http_host + "/v1/common/device/getDeviceStatus"
            #device_host="http://sit.aimidea.cn:11003/v1/common/device/getDeviceStatus"
            log.info("获取设备状态,请求参数为:{},地址:{}".format(params, device_host))
            jsonvalue = requests.post(device_host, json=params, headers=headers).json()

        except Exception as e:
            log.info("获取设备状态异常:{}".format(e))
            raise e
        else:
            log.info("获取设备状态信息:{}".format(jsonvalue))
            return jsonvalue

    def open_api(self, paramsdata):
        # headers = {"Content-Type": "application/x-www-form-urlencoded"}

        device_host = http_host + "/v1/base2pro/data/transmit"
        log.info(f"open_api测试,请求参数为:{paramsdata},地址:{device_host}")
        try:
            response = requests.post(device_host, params=parse.urlencode(paramsdata))
            jsonvalue = response.json()
        except Exception as e:
            raise e
        else:
            log.info("open_api接口返回信息:{}".format(jsonvalue))
            return jsonvalue

    # 获取token信息
    def get_token(self, uid):
        device_host = http_host + "/v1/user/token/getToken"
        print(device_host)
        data = {"clientId": "e256482c-2b93-4f79-bda5-c76da8de2129", "uid": uid, "permission": "AutomationTest"}
        try:
            a = requests.get(device_host, params=parse.urlencode(data)).json()
            token = a['data']
        except Exception as e:
            log.info("获取token信息异常:{}".format(e))
            return {}
        else:
            return token


if __name__ == '__main__':
    #jsonvalue = Api().post("ed855a919cfc11ebae79309c23f58a21")
    #print(jsonvalue)
    # data = {"serviceUrl": "/v1/device/speech/fullDuplex",
    #         "data": {"deviceId": 3298544982176, "fullDuplex": 1,
    #                  "fullDuplexSkillConfig": [{"skillId": "midea-deviceControl", "timeOut": "10"}]}}
    # data = {"serviceUrl": "/v1/tts/voice/set",
    #         "data": {"deviceId":"3298544982176","voiceId":"xiyaof"}}
    #data0 = {'serviceUrl': '/v1/accent/set',
    #         'data': {'deviceId': '160528698598412', 'accentId': 'cantonese', 'enableAccent': '1',
    #                  'mixedResEnable': '1'}}
    # r = Api().open_api(data)
    # print(r)
    n = Api().get_token("80920524eedef3574e64c3dab72dd0bd")
    print(n)
