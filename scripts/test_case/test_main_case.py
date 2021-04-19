import datetime
import re

import allure
import pytest
import config
import os
from api import Traversing_path
from tools.file_tool_1 import MyXlrs
from tools.file_tool import FileTool
from tools.mylog import Logger
from scripts import common_function
from scripts.init_env import current_env
from tools.myxls import Read_xls

log = Logger()
main_device_list = config.main_device_list

# 运行设备控制阶段
common_function.run_main_case()

nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
result_file = os.path.join(os.path.join(config.base_path, "result"), f"{current_env}_MainCase_TestResult_{nowdate}.xls")
r = Read_xls(result_file)
w = r.copy_book()


def get_all_caseinfo():
    sheet_names = r.get_sheet_names()
    all_caseinfo = list()
    for devicetype in sheet_names:
        data = r.read_data(start_line=2, sheetname=devicetype, is_addsheetname=True)
        dict_data = FileTool().dict_info(data, devicetype=devicetype, isindex=True)
        all_caseinfo += dict_data
    print(all_caseinfo)
    return all_caseinfo


all_caseinfo = get_all_caseinfo()


class TestMain:
    def setup_class(self):
        log.info("========%s开始执行主场景用例测试用例:========" % __class__.__name__)

    def teardown_class(cls):
        Logger().info("========%s执行主场景用例测试用例结束!========" % __class__.__name__)

    @pytest.mark.parametrize("case", all_caseinfo)
    def test_maincase(self, case):
        log.info("执行用例{}".format(case))
        device_type = case["devicetype"]
        allure.dynamic.feature(device_type)
        case_category = case["case_category"]
        allure.dynamic.story(case_category)
        allure.dynamic.title(case["case_name"])
        common_function.Commonfunction().runstep(r, w, device_type, case, result_file)
