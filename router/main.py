#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Time  :  2019/7/24 13:43
# @Author:  GaoJun


from BeautifulReport import BeautifulReport
import unittest
import os
from unittest import TestLoader

from .time_limit_dir.test_Web_limitTime import LimitTime
from .rate_limit_dir.test_Web_limitRate import LimitRate
from .websiteblacklist_limit_dir.test_Web_limitWebsiteBlacklist import LimitWebsiteBlacklist
from .wifi_set_dir.test_Web_wifiSettings import WifiSettings
from .guest_wifi__dir.test_Web_guestWifiSettings import GuestWifiSettings
from .device_blacklist_dir.test_Web_blacklist import DeviceBlacklist
from .static_dhcp_lease_dir.test_Web_staticDhcpLease import StaticDHCPLease









def core():
    s = []
    class_tests = [
        StaticDHCPLease
    ]

    for t in class_tests:
        suite = TestLoader().loadTestsFromTestCase(t)
        s.append(suite)
    t_s = unittest.TestSuite(s)
    return t_s


if __name__ == "__main__":
    t_suites = core()
    result = BeautifulReport(t_suites)
    log_path = 'report/router'
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    result.report(filename="功能自动化测试",
                  description="路由器功能自动化测试报告",
                  log_path=log_path)



