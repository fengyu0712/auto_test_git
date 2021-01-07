# coding: utf-8
# @Time : 2021-1-7 14:14 
# @Author : xx
# @File : test_xf.py.py 
# @Software: PyCharm
from tools.get_log import GetLog
from tools.file_tool import FileTool
from scripts.common_function import Commonfunction

log = GetLog.get_logger()  # 初始化日志对象
import allure
import pytest


class Testxf:
    # 1、实列化获取工具类对象
    log.info("执行讯飞328固件空调入口测试用例..............")
    device_type = "讯飞328"  # 入口类型：328 固件的空调
    tool = FileTool("data_case.csv", device_type)
    # 读取excel的内容信息
    testcaseinfo = tool.read_excel()
    print(testcaseinfo)
    Commonfunction().runcase(testcaseinfo, device_type, tool)
    @allure.feature("讯飞328固件空调入口")
    @pytest.mark.parametrize("case", testcaseinfo)
    def testxf(self, case):
        log.info("执行用例{}".format(case))
        current_sheet = case.get('case_catory')
        allure.dynamic.story(current_sheet)
        allure.dynamic.title(case.get("case_name"))
        Commonfunction().runstep(case, Testxf.tool, Testxf.device_type, log)