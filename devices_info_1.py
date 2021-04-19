# coding: utf-8
# 328
import re
import time
import uuid
from scripts.init_env import terminal_devices


class Deviceset():
    def __init__(self, terminal_type):
        self.devicetype = terminal_type  # 设备类型
        self.device_info = terminal_devices.get(terminal_type)  # 获取设备信息
        if not self.device_info:
            self.device_info = terminal_devices.get("328_halfDuplex")
        self.sn = self.device_info["sn"]  # sn信息
        self.clientid = self.device_info.get("clientid")  # clientid信息
        self.deviceId = self.device_info.get("deviceId")  # deviceId信息
        self.module_version = self.device_info.get("module_version")
        if self.devicetype == "3308_halfDuplex":
            self.version = "1.0"
        else:
            self.version = "3.0"

    def get_time_stamp(self):
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = "%s.%03d" % (data_head, data_secs)
        return time_stamp

    def ota_check(self):
        ota_check_data = {
            "topic": "cloud.ota.check",
            "mid": f"{uuid.uuid1().hex}",
            "version": self.version,
            "request": {
                "timestamp": f"{self.get_time_stamp()}"
            },
            "params": {
                "sn": f"{self.sn}",
                "category": "AC",
                "model": "172",
                "id": f"{self.deviceId}",
                "clientId": "%s" % self.clientid,
                "brand": "Midea"
            }
        }

        def ota_module_version(module_version):
            module_version_slitList = module_version.split(".")
            module_version_json = {"hardwarePlat": module_version_slitList[0],
                                   "hardwareVer": module_version[:5],
                                   "hardwareCategory": module_version_slitList[1],
                                   "hardwareModel": module_version_slitList[4],
                                   "hardwareFullVer": module_version[:14],
                                   "firmwareVer": module_version}
            return module_version_json

        ota_check_data["params"].update(ota_module_version(self.module_version))
        return ota_check_data

    def audio_staus_data(self, volume=None):
        if volume == None:
            volume = 50
        status_data = {
            "version": self.version,
            "topic": "cloud.report.status",
            "mid": "%s" % uuid.uuid1().hex,
            "category": "AC",
            "id": f"{self.deviceId}",
            "clientId": "%s" % self.clientid,
            "sn": f"{self.sn}",
            "request": {
                "timestamp": self.get_time_stamp()
            },
            "params": {
                "status": [{
                    "class": "audio",
                    "audio": {
                        "level": "4",
                        "max": "100",
                        "min": "1",
                        "volume": f"{str(volume)}"
                    }
                }]
            }
        }
        return status_data

    def send_play_status(self, status=None):
        if status == None or status == "resume":
            status = "play"
        play_status = {
            "version": self.version,
            "topic": "cloud.report.status",
            "mid": "%s" % uuid.uuid1().hex,
            "category": "AC",
            "id": f"{self.deviceId}",
            "clientId": "%s" % self.clientid,
            "sn": f"{self.sn}",
            "request": {
                "timestamp": self.get_time_stamp()
            },
            "params": {
                "status": [{
                    "class": "player",
                    "player": {
                        "status": status,
                        "resource": {
                            "urlType": "media",
                            "skillType": "",
                            "autoResume": True,
                            "text": "浪人情歌",
                            "url": "http://mp3cdn.hifiok.com/00/0E/wKgBeVBdTYaA_OZBAKfeJQULj-M020.mp3?sign=0b57017c2d9b000b02e130377d008364&t=1613756930",
                            "seq": 1
                        }
                    }
                }]
            }
        }
        # print(play_status)
        return play_status

    # 添加上线的信息
    def online_data(self):
        if self.devicetype == "yuyintie_1":
            online_data = {
                "topic": "cloud.online",
                "version": "3.0",
                "mid": f"{uuid.uuid1().hex}",
                "request": {
                    "apiVer": "1.0.0",
                    "timestamp": self.get_time_stamp(),
                    "paramsSignBase64": "8b0NLQ0rJ1Vb/MpTZ9vXHLsRMCk="
                },
                "params": {
                    "category": "8",
                    "clientId": f" {self.clientid}",
                    "id": f"{self.deviceId}",
                    "ip": "127.0.0.1",
                    "mac": "50:2d:bb:b3:e5:a5",
                    "model": "22",
                    "productId": "1596681815",
                    "sn": f"{self.sn}",
                }
            }
        elif self.devicetype == "328_halfDuplex":
            online_data = {
                "topic": "cloud.online",
                "version": self.version,
                "mid": f"{uuid.uuid1().hex}",
                "request": {
                    "apiVer": "1.0.0",
                    "timestamp": self.get_time_stamp(),
                    "paramsSignBase64": "8b0NLQ0rJ1Vb/MpTZ9vXHLsRMCk="
                },
                "params": {
                    "category": "AC",
                    "clientId": f"{self.clientid}",
                    "id": f"{self.deviceId}",
                    "ip": "127.0.0.1",
                    "mac": "f0:c9:d1:b5:f9:a7",
                    "model": "172",
                    "productId": "1596681815",
                    "sn": f"{self.sn}",
                }
            }
        elif self.devicetype == "3308_halfDuplex":
            online_data = {
                "topic": "cloud.online",
                "version": self.version,
                "mid": f"{uuid.uuid1().hex}",
                "request": {
                    "apiVer": "1.0.0",
                    "timestamp": f"{self.get_time_stamp()}"
                },
                "params": {
                    "category": "0xAC",
                    "clientId": f"{self.clientid}",
                    "id": f"{self.deviceId}",
                    "sn": f"{self.sn}",
                    "magicCode": "TSETIA"
                }
            }
        else:
            online_data = {
                "topic": "cloud.online",
                "mid": f"{uuid.uuid1().hex}",
                "version": self.version,
                "request": {
                    "apiVer": "1.0.0",
                    "timestamp": self.get_time_stamp(),

                },
                "params": {
                    "id": "%s" % self.deviceId,
                    "sn": "%s" % self.sn,
                    "clientId": "%s" % self.clientid,
                    "category": "0xAC",
                    "magicCode": "TSETIA"
                }
            }

        # self.headers.append(online_data)
        return online_data

    def content_data(self):
        if self.devicetype == "328_halfDuplex":
            content_data = {
                "version": self.version,
                "topic": "cloud.speech.trans",
                "mid": "%s" % uuid.uuid1().hex,
                "id": "%s" % self.deviceId,
                "category": "AC",
                "request": {
                    "apiVer": "1.0.0",
                    "sessionId": "%s" % uuid.uuid1().hex,
                    "recordId": "%s" % uuid.uuid1().hex,
                    "isMore": False
                },
                "params": {
                    "audio": {
                        "audioType": "wav",
                        "sampleRate": 16000,
                        "channel": 1,
                        "sampleBytes": 2
                    },
                    "ttsIsp": "dui-real-sound",
                    "nluIsp": "DUI",
                    "asrIsp": "DUI",
                    "serverVad": False,
                    "accent": "mandarin",
                    "mixedResEnable": "0"
                }
            }
        elif self.devicetype == "328_fullDuplex":
            content_data = {
                "version": self.version,
                "topic": "cloud.speech.trans",
                "mid": uuid.uuid1().hex,
                "id": "%s" % self.deviceId,
                "sn": "%s" % self.sn,
                "clientId": "%s" % self.clientid,
                "category": "AC",
                "request": {
                    "apiVer": "1.0.0",
                    "sessionId": "%s" % uuid.uuid1().hex,
                    "recordId": "%s" % uuid.uuid1().hex,
                    "isMore": False
                },
                "params": {
                    "audio": {
                        "audioType": "wav",
                        "sampleRate": 16000,
                        "channel": 1,
                        "sampleBytes": 2
                    },
                    "ttsIsp": "dui-real-sound",
                    "nluIsp": "DUI",
                    "asrIsp": "DUI",
                    "serverVad": False,
                    "accent": "mandarin",
                    "fullDuplex": True
                }
            }

        elif self.devicetype == "yuyintie_1":
            content_data = {
                "topic": "cloud.speech.trans",
                "mid": uuid.uuid1().hex,
                "version": self.version,
                "request": {
                    "timestamp": self.get_time_stamp(),
                    "sessionId": "%s" % uuid.uuid1().hex,
                    "recordId": "%s" % uuid.uuid1().hex,
                },
                "params": {
                    "audio": {
                        "audioType": "wav",
                        "sampleRate": 16000,
                        "channel": 1,
                        "sampleBytes": 2
                    }
                }
            }
        elif self.devicetype == "xf":
            content_data = {
                "topic": "cloud.speech.trans",
                "mid": uuid.uuid1().hex,
                "version": self.version,
                "request": {
                    "timestamp": self.get_time_stamp(),
                    "sessionId": "%s" % uuid.uuid1().hex,
                    "recordId": "%s" % uuid.uuid1().hex,
                },
                "params": {
                    "audio": {
                        "audioType": "wav",
                        "sampleRate": 16000,
                        "channel": 1,
                        "sampleBytes": 2
                    },
                    "fullDuplex": False,
                    "asrIsp": "xf-aiui",
                    "accent": "mandarin",
                }
            }
        elif self.devicetype == "3308_halfDuplex":
            content_data = {
                "version": self.version,
                "topic": "cloud.speech.trans",
                "mid": f"{uuid.uuid1().hex}",
                "id": f"{self.deviceId}",
                "sn": self.sn,
                "clientId": f"{self.clientid}",
                "category": "AC",
                "request": {
                    "apiVer": "1.0.0",
                    "sessionId": f"{uuid.uuid1().hex}",
                    "recordId": f"{uuid.uuid1().hex}",
                    "isMore": False
                },
                "params": {
                    "audio": {
                        "audioType": "wav",
                        "sampleRate": 16000,
                        "channel": 1,
                        "sampleBytes": 2
                    }
                }
            }
        else:
            content_data = {
                "version": self.version,
                "topic": "cloud.speech.trans",
                "mid": "%s" % uuid.uuid1().hex,
                "id": "%s" % self.deviceId,
                "category": "AC",
                "request": {
                    "apiVer": "1.0.0",
                    "sessionId": "%s" % uuid.uuid1().hex,
                    "recordId": "%s" % uuid.uuid1().hex,
                    "isMore": False
                },
                "params": {
                    "audio": {
                        "audioType": "wav",
                        "sampleRate": 16000,
                        "channel": 1,
                        "sampleBytes": 2
                    },
                    "ttsIsp": "dui-real-sound",
                    "nluIsp": "DUI",
                    "asrIsp": "DUI",
                    "serverVad": False,
                    "accent": "mandarin",
                    "mixedResEnable": "0"
                }
            }
        return content_data

if __name__ == '__main__':
    a=Deviceset("328").content_data()
    print(a)