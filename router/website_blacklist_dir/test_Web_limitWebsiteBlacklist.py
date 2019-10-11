#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Time  :  2019/7/24 13:43
# @Author:  GaoJun

import unittest
import time
from rweb import const
from selenium import webdriver
from BeautifulReport import BeautifulReport
import os
from unittest import TestLoader


from router.test_base import Base
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from rweb.path.common import CommonLocators
from rweb.path.devices import DevicesLocators
from rweb.path.limitTime import LimitTimeLocators
from rweb.path.limitRate import LimitRateLocators
from rweb.path.websiteBlacklist import WebsiteBlacklistLocators

from .website_blacklist_testcase import Test_website_blacklist



class LimitWebsiteBlacklist(Base):

    def setUp(self):
        super(LimitWebsiteBlacklist, self).setUp()
        # 鼠标移动到切换“我的WiFi”按钮上
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.presence_of_element_located((By.XPATH, CommonLocators.LEVEL_1_MyWifi))
        )
        mouse = self.driver.find_element_by_xpath(CommonLocators.LEVEL_1_MyWifi)
        ActionChains(self.driver).move_to_element(mouse).perform()
        # 点击 接入设备
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, CommonLocators.Devices))
        )
        self.driver.find_element_by_xpath(CommonLocators.Devices).click()
        self.driver.refresh()
        # 点击主网-设置
        Set = DevicesLocators.Set.format(num=1)
        WebDriverWait(self.driver, const.SLOW_WAIT+10).until(
            EC.element_to_be_clickable((By.XPATH, Set))
        )
        time.sleep(0.5)
        self.driver.find_element_by_xpath(Set).click()
        # 切换到网址黑名单页
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Page_WebsiteBlacklist))
        ).click()




    #@unittest.skip("跳过")
    def test_A_limitWebsiteBlacklist_add(self):
        """操作步骤：新增网址：www.baidu.com"""

        # 点击黑名单 新增 按钮
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Add))
        ).click()
        # 输入：WWW.BAIDU.COM
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Website))
        ).send_keys("WWW.BAIDU.COM")
        # 完成添加
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Save))
        ).click()
        # 断言:toast提示：添加成功
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
        )
        assert self.driver.find_element_by_xpath(CommonLocators.Success_Toast).text == "Successful operation"

        # 断言：用例-1980 : 新增网址框-输入正确网址，点击“保存”，关闭弹框，新增成功，显示在列表
        # 断言：用例-1969 : 网址列表-网址为大写字母，保存成功后，配置都存为小写字母
        self.driver.refresh()
        List_Website = WebsiteBlacklistLocators.List_Website.format(num="last()")
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, List_Website))
        )
        assert self.driver.find_element_by_xpath(List_Website).text == "www.baidu.com"







    #@unittest.skip("跳过")
    def test_B_limitWebsiteBlacklist_statu_on(self):
        """操作步骤：将开关开启"""
        # 状态理应为关闭，如果为关闭状态才进行if的启用操作
        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        if Statu_class == "switch switch-animation":
            # 打开网址黑名单开关
            time.sleep(1)
            WebDriverWait(self.driver, const.SLOW_WAIT).until(
                EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
            ).click()
            # 断言:toast提示：打开开关成功
            WebDriverWait(self.driver, const.SLOW_WAIT).until(
                EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
            )
            assert self.driver.find_element_by_xpath(CommonLocators.Success_Toast).text == "Successful operation"

        self.driver.refresh()
        time.sleep(2)   #用于状态按钮切换
        # 断言：判断开关是否开启
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
        )
        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        assert Statu_class == "switch switch-animation checked", Statu_class






    #@unittest.skip("跳过")
    def test_C_limitWebsiteBlacklist_1(self):
        """【检验】用例-5032:开关开启，设备A添加一个完整的网址黑名单a，设备A不可以访问网址a(设备a不可以访问www.baidu.com)"""

        # 前提条件：开关开启
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
        )
        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        if Statu_class == "switch switch-animation checked":
            Result = Test_website_blacklist.test_website_blacklist_1()
            if Result == 1:
                print("【成功】限制住了：www.baidu.com")
                assert True
            else:
                print("【失败】没有限制住：www.baidu.com")
                assert False
        else:
            print("【备注】该用例无法验证，原因：开关未开启")
            assert False





    #@unittest.skip("跳过")
    def test_D_limitWebsiteBlacklist_2(self):
        """【检验】用例-7216:开关开启，设备A添加一个完整的网址黑名单a，设备A可以访问非网址a的网址（设备a不可以访问www.baidu.com，但是可以访问new.baidu.com,www.jd.com）"""
        # 前提条件：开关开启
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
        )
        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        if Statu_class == "switch switch-animation checked":
            Result = Test_website_blacklist.test_website_blacklist_2()
            if Result == 1:
                print("【成功】没有限制其它未添加的网站，如：new.baidu.com")
                assert True
            else:
                print("【失败】限制住了其它未添加的网站，如：new.baidu.com")
                assert False
        else:
            print("【备注】该用例无法验证，原因：开关未开启")
            assert False





    #@unittest.skip("跳过")
    def test_E_limitWebsiteBlacklist_3(self):
        """【检验】用例-7214:开关开启，设备A添加一个完整的网址黑名单a，设备B可以访问网址a（设备a不可以访问www.baidu.com，设备b不可以访问www.baidu.com）"""
        # 前提条件：开关开启
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
        )
        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        if Statu_class == "switch switch-animation checked":

            Result = Test_website_blacklist.test_website_blacklist_3()
            print(Result)
            if Result == 1:
                print("【成功】设备A限制的网址a，设备B可以正常访问网址a")
                assert True
            else:
                print("【失败】设备A限制的网址a，设备B不可以正常访问网址a")
                assert False
        else:
            print("【备注】该用例无法验证，原因：开关未开启")
            assert False






    #@unittest.skip("跳过")
    def test_F_limitWebsiteBlacklist_delete(self):
        """操作步骤：删除网址：www.baidu.com"""
        flag = False
        while flag == False:
            try:
                assert self.driver.find_element_by_xpath(WebsiteBlacklistLocators.List_Null).is_displayed()
                flag = True
            except:
                Delete = WebsiteBlacklistLocators.Delete.format(num="last()")
                WebDriverWait(self.driver, const.SLOW_WAIT).until(
                    EC.element_to_be_clickable((By.XPATH, Delete))
                ).click()
                # 断言:toast提示：成功
                WebDriverWait(self.driver, const.SLOW_WAIT).until(
                    EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
                )
                time.sleep(2)

        # 断言：用例-1987 : 删除一个网址，删除成功，从列表消失
        self.driver.refresh()
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.List_Null))
        )
        assert self.driver.find_element_by_xpath(WebsiteBlacklistLocators.List_Null).is_displayed()







    #@unittest.skip("跳过")
    def test_G_limitWebsiteBlacklist_4(self):
        """【检验】用例-4836:开关开启，设备A删除一个网址黑名单a，设备A可以访问网址a（设备a不可以访问www.baidu.com，删除设备a的网址黑名单www.baidu.com）"""

        # 前提条件1：www.baidu.com被删除（判断列表为空即可）
        try:
            WebDriverWait(self.driver, const.FAST_WAIT).until(
                EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.List_Null))
            )
            assert self.driver.find_element_by_xpath(WebsiteBlacklistLocators.List_Null).is_displayed()
        except:
            print("【备注】该用例无法验证，原因：www.baidu.com未删除")
            assert False

        # 前提条件2：开关开启
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
        )
        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        if Statu_class == "switch switch-animation checked":
            Result = Test_website_blacklist.test_website_blacklist_4()
            print(Result)
            if Result == 1:
                print("【成功】设备A限制的网址a，但被网址a删除后，可正常访问")
                assert True
            else:
                print("【失败】设备A限制的网址a，但被网址a删除后，也不能正常访问")
                assert False
        else:
            print("【备注】该用例无法验证，原因：开关未开启")
            assert False




    #@unittest.skip("跳过")
    def test_H_limitWebsiteBlacklist_add(self):
        """操作步骤：新增网址：baidu"""

        # 点击黑名单 新增 按钮
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Add))
        ).click()
        # 输入：WWW.BAIDU.COM
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Website))
        ).send_keys("baidu")
        # 完成添加
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Save))
        ).click()
        # 断言:toast提示：添加成功
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
        )
        assert self.driver.find_element_by_xpath(CommonLocators.Success_Toast).text == "Successful operation"

        # 断言：用例-1980 : 新增网址框-输入正确网址，点击“保存”，关闭弹框，新增成功，显示在列表
        # 断言：用例-1969 : 网址列表-网址为大写字母，保存成功后，配置都存为小写字母
        self.driver.refresh()
        List_Website = WebsiteBlacklistLocators.List_Website.format(num="last()")
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, List_Website))
        )
        assert self.driver.find_element_by_xpath(List_Website).text == "baidu"





    #@unittest.skip("跳过")
    def test_I_limitWebsiteBlacklist_5(self):
        """【备注】用例-7215:开关开启，设备A添加一个主域名的网址黑名单，设备A无法访问主域名相关的所有网址（设备a不可以访问主域名baidu，那么设备a就不能访问www.baidu.com,news.baidu.com,tieba.baidu.com,jingyan.baidu.com）"""

        # 前提条件1：网址为：baidu
        List_Website = WebsiteBlacklistLocators.List_Website.format(num="last()")
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, List_Website))
        )
        Website_Text = self.driver.find_element_by_xpath(List_Website).text
        if Website_Text != "baidu":
            print("【备注】该用例无法验证，原因：网址不为：baidu")
            assert False

        # 前提条件2：开关开启
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
        )
        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        if Statu_class == "switch switch-animation checked":
            Result = Test_website_blacklist.test_website_blacklist_5()
            print(Result)
            if Result == 1:
                print("【成功】设备A限制主域名baidu，baidu相关的所有网址均被限制")
                assert True
            else:
                print("【失败】设备A限制主域名baidu，baidu相关的所有网址均不被限制")
                assert False
        else:
            print("【备注】该用例无法验证，原因：开关未开启")
            assert False





    #@unittest.skip("跳过")
    def test_J_limitWebsiteBlacklist_delete(self):
        """操作步骤：删除网址：baidu"""
        flag = False
        while flag == False:
            try:
                assert self.driver.find_element_by_xpath(WebsiteBlacklistLocators.List_Null).is_displayed()
                flag = True
            except:
                Delete = WebsiteBlacklistLocators.Delete.format(num="last()")
                WebDriverWait(self.driver, const.SLOW_WAIT).until(
                    EC.element_to_be_clickable((By.XPATH, Delete))
                ).click()
                # 断言:toast提示：成功
                WebDriverWait(self.driver, const.SLOW_WAIT).until(
                    EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
                )
                time.sleep(2)
        # 断言：删除成功
        self.driver.refresh()
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.List_Null))
        )
        assert self.driver.find_element_by_xpath(WebsiteBlacklistLocators.List_Null).is_displayed()





    #@unittest.skip("跳过")
    def test_K_limitWebsiteBlacklist_add_four_website(self):
        """操作步骤：新增网址：www.baidu.com"""
        Website = ["www.baidu.com", "news.baidu.com", "www.jd.com", "jiadian.jd.com"]
        i = 1
        while i <= 4:
            # 点击黑名单 新增 按钮
            WebDriverWait(self.driver, const.SLOW_WAIT).until(
                EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Add))
            )
            time.sleep(0.5)
            self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Add).click()
            # 输入 网址
            WebDriverWait(self.driver, const.SLOW_WAIT).until(
                EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Website))
            ).send_keys(Website[i-1])
            # 完成添加
            WebDriverWait(self.driver, const.SLOW_WAIT).until(
                EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Save))
            ).click()
            # 断言:toast提示：添加成功
            WebDriverWait(self.driver, const.SLOW_WAIT).until(
                EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
            )
            assert self.driver.find_element_by_xpath(CommonLocators.Success_Toast).text == "Successful operation"
            i += 1
            time.sleep(0.5)





    #@unittest.skip("跳过")
    def test_L_limitWebsiteBlacklist_6(self):
        """【备注】用例-5240:开关开启，设备A添加多个网址黑名单，设备A不可以访问黑名单网址(设备a不可以访问www.baidu.com)"""

        # 前提条件1：存在4个网址为：www.baidu.com、news.baidu.com、www.jd.com、jiadian.jd.com
        List_Website_1 = WebsiteBlacklistLocators.List_Website.format(num=1)
        List_Website_2 = WebsiteBlacklistLocators.List_Website.format(num=2)
        List_Website_3 = WebsiteBlacklistLocators.List_Website.format(num=3)
        List_Website_4 = WebsiteBlacklistLocators.List_Website.format(num=4)
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.presence_of_element_located((By.XPATH, List_Website_1))
        )
        time.sleep(1)
        Website_1_Text = self.driver.find_element_by_xpath(List_Website_1).text
        Website_2_Text = self.driver.find_element_by_xpath(List_Website_2).text
        Website_3_Text = self.driver.find_element_by_xpath(List_Website_3).text
        Website_4_Text = self.driver.find_element_by_xpath(List_Website_4).text
        if Website_1_Text != "jiadian.jd.com" and Website_2_Text != "news.baidu.com" and Website_3_Text != "www.baidu.com" and Website_4_Text != "www.jd.com":
            print("【备注】该用例无法验证，原因：存在的网址不为4个网址：www.baidu.com、news.baidu.com、www.jd.com、jiadian.jd.com")
            assert False

        # 前提条件2：开关开启
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
        )
        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        if Statu_class == "switch switch-animation checked":
            Result = Test_website_blacklist.test_website_blacklist_6()
            print(Result)
            if Result == 1:
                print("【成功】设备A限制多个网址，多个网址均被限制")
                assert True
            else:
                print("【失败】设备A限制多个网址，多个网址不被限制或不全被限制")
                assert False
        else:
            print("【备注】该用例无法验证，原因：开关未开启")
            assert False




    #@unittest.skip("跳过")
    def test_M_limitWebsiteBlacklist_delete(self):
        """操作步骤：删除所有网址"""
        flag = False
        while flag == False:
            try:
                assert self.driver.find_element_by_xpath(WebsiteBlacklistLocators.List_Null).is_displayed()
                flag = True
            except:
                Delete = WebsiteBlacklistLocators.Delete.format(num="last()")
                WebDriverWait(self.driver, const.SLOW_WAIT).until(
                    EC.element_to_be_clickable((By.XPATH, Delete))
                ).click()
                # 断言:toast提示：成功
                WebDriverWait(self.driver, const.SLOW_WAIT).until(
                    EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
                )
                time.sleep(2)
        # 断言：删除成功
        self.driver.refresh()
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.List_Null))
        )
        assert self.driver.find_element_by_xpath(WebsiteBlacklistLocators.List_Null).is_displayed()






    #@unittest.skip("跳过")
    def test_N_limitWebsiteBlacklist_A_add(self):
        """操作步骤：有线新增网址：www.baidu.com、无线新增网址：www.jd.com"""

        # 有线新增网址：www.baidu.com
        # 点击黑名单 新增 按钮
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Add))
        ).click()
        # 输入：www.baidu.com
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Website))
        ).send_keys("www.baidu.com")
        # 完成添加
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Save))
        ).click()
        # 断言:toast提示：添加成功
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
        )
        assert self.driver.find_element_by_xpath(CommonLocators.Success_Toast).text == "Successful operation"
        self.driver.refresh()
        List_Website = WebsiteBlacklistLocators.List_Website.format(num="last()")
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, List_Website))
        )
        assert self.driver.find_element_by_xpath(List_Website).text == "www.baidu.com"
        #判断：需要开关开启
        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        if Statu_class == "switch switch-animation":
            # 打开网址黑名单开关
            time.sleep(1)
            WebDriverWait(self.driver, const.SLOW_WAIT).until(
                EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
            ).click()
            # 断言:toast提示：打开开关成功
            WebDriverWait(self.driver, const.SLOW_WAIT).until(
                EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
            )
            assert self.driver.find_element_by_xpath(CommonLocators.Success_Toast).text == "Successful operation"


        # 无线新增网址：www.jd.com
        # 鼠标移动到切换“我的WiFi”按钮上
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.presence_of_element_located((By.XPATH, CommonLocators.LEVEL_1_MyWifi))
        )
        mouse = self.driver.find_element_by_xpath(CommonLocators.LEVEL_1_MyWifi)
        ActionChains(self.driver).move_to_element(mouse).perform()
        # 点击 接入设备
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, CommonLocators.Devices))
        ).click()
        self.driver.refresh()
        # 点击主网-设置
        Set = DevicesLocators.Set.format(num=2)
        WebDriverWait(self.driver, const.SLOW_WAIT + 10).until(
            EC.element_to_be_clickable((By.XPATH, Set))
        )
        time.sleep(0.5)
        self.driver.find_element_by_xpath(Set).click()
        # 切换到网址黑名单页
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Page_WebsiteBlacklist))
        ).click()
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Add))
        ).click()
        # 输入：www.jd.com
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Website))
        ).send_keys("www.jd.com")
        # 完成添加
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Save))
        ).click()
        # 断言:toast提示：添加成功
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
        )
        assert self.driver.find_element_by_xpath(CommonLocators.Success_Toast).text == "Successful operation"
        self.driver.refresh()
        List_Website = WebsiteBlacklistLocators.List_Website.format(num="last()")
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, List_Website))
        )
        assert self.driver.find_element_by_xpath(List_Website).text == "www.jd.com"
        # 判断：需要开关开启
        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        if Statu_class == "switch switch-animation":
            # 打开网址黑名单开关
            time.sleep(1)
            WebDriverWait(self.driver, const.SLOW_WAIT).until(
                EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
            ).click()
            # 断言:toast提示：打开开关成功
            WebDriverWait(self.driver, const.SLOW_WAIT).until(
                EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
            )
            assert self.driver.find_element_by_xpath(CommonLocators.Success_Toast).text == "Successful operation"




    #@unittest.skip("跳过")
    def test_O_limitWebsiteBlacklist_7(self):
        """【备注】用例-7217:设备A的网址黑名单关闭，设备A可以访问任何网址，设备B的网址黑名单开启，设备B不可以访问网址黑名单中的网址"""

        # 前提条件：有线网址为：www.baidu.com、无线网址为：www.jd.com，并且开关均开启
        # 判断无线
        # 鼠标移动到切换“我的WiFi”按钮上
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.presence_of_element_located((By.XPATH, CommonLocators.LEVEL_1_MyWifi))
        )
        mouse = self.driver.find_element_by_xpath(CommonLocators.LEVEL_1_MyWifi)
        ActionChains(self.driver).move_to_element(mouse).perform()
        # 点击 接入设备
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, CommonLocators.Devices))
        ).click()
        self.driver.refresh()
        # 点击主网-设置
        Set = DevicesLocators.Set.format(num=2)
        WebDriverWait(self.driver, const.SLOW_WAIT + 10).until(
            EC.element_to_be_clickable((By.XPATH, Set))
        )
        time.sleep(0.5)
        self.driver.find_element_by_xpath(Set).click()
        # 切换到网址黑名单页
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Page_WebsiteBlacklist))
        ).click()
        List_Website = WebsiteBlacklistLocators.List_Website.format(num="last()")
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, List_Website))
        )
        List_Website_Text = self.driver.find_element_by_xpath(List_Website).text
        if List_Website_Text != "www.jd.com":
            print("【备注】该用例无法验证，原因：无线设备网址不为：www.jd.com")
            assert False
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
        )
        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        if Statu_class != "switch switch-animation checked":
            print("【备注】该用例无法验证，原因：无线设备网址黑名单开关为关")
            assert False

        # 判断有线
        # 鼠标移动到切换“我的WiFi”按钮上
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.presence_of_element_located((By.XPATH, CommonLocators.LEVEL_1_MyWifi))
        )
        mouse = self.driver.find_element_by_xpath(CommonLocators.LEVEL_1_MyWifi)
        ActionChains(self.driver).move_to_element(mouse).perform()
        # 点击 接入设备
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, CommonLocators.Devices))
        ).click()
        self.driver.refresh()
        # 点击主网-设置
        Set = DevicesLocators.Set.format(num=1)
        WebDriverWait(self.driver, const.SLOW_WAIT + 10).until(
            EC.element_to_be_clickable((By.XPATH, Set))
        )
        time.sleep(0.5)
        self.driver.find_element_by_xpath(Set).click()
        # 切换到网址黑名单页
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Page_WebsiteBlacklist))
        ).click()
        List_Website = WebsiteBlacklistLocators.List_Website.format(num="last()")
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, List_Website))
        )
        List_Website_Text = self.driver.find_element_by_xpath(List_Website).text
        if List_Website_Text != "www.baidu.com":
            print("【备注】该用例无法验证，原因：有线设备网址不为：www.baidu.com")
            assert False
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
        )
        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        if Statu_class != "switch switch-animation checked":
            print("【备注】该用例无法验证，原因：有线设备网址黑名单开关为关")
            assert False


        # 有线设备关闭黑名单开关，而无线设备保持黑名单开关打开
        time.sleep(0.5)
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
        )
        time.sleep(0.5)
        self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).click()
        # 断言:toast提示：关闭开关成功
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
        )
        assert self.driver.find_element_by_xpath(CommonLocators.Success_Toast).text == "Successful operation"
        self.driver.refresh()
        # 断言：判断开关是否关闭成功
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
        )
        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        if Statu_class != "switch switch-animation":
            print("【备注】该用例无法验证，原因：有线设备的黑名单开关没有成功关闭")
            assert False

        # 前提已完成，开始检验用例
        Result = Test_website_blacklist.test_website_blacklist_7()
        print(Result)
        if Result == 1:
            print("【成功】设备A黑名单开关关闭，不会影响设备B")
            assert True
        else:
            print("【失败】设备A黑名单开关关闭，会影响设备B")
            assert False





    #@unittest.skip("跳过")
    def test_P_limitWebsiteBlacklist_A_add(self):
        """操作步骤：有线新增网址：news.baidu.com、无线新增网址：jiadian.jd.com"""

        # 有线新增网址：news.baidu.com
        # 点击黑名单 新增 按钮
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Add))
        ).click()
        # 输入：www.jd.com
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Website))
        ).send_keys("news.baidu.com")
        # 完成添加
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Save))
        ).click()
        # 断言:toast提示：添加成功
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
        )
        assert self.driver.find_element_by_xpath(CommonLocators.Success_Toast).text == "Successful operation"
        self.driver.refresh()
        List_Website = WebsiteBlacklistLocators.List_Website.format(num=1)
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, List_Website))
        )
        assert self.driver.find_element_by_xpath(List_Website).text == "news.baidu.com"
        # 判断：需要开关开启
        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        if Statu_class == "switch switch-animation":
            # 打开网址黑名单开关
            time.sleep(1)
            WebDriverWait(self.driver, const.SLOW_WAIT).until(
                EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
            ).click()
            # 断言:toast提示：打开开关成功
            WebDriverWait(self.driver, const.SLOW_WAIT).until(
                EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
            )
            assert self.driver.find_element_by_xpath(CommonLocators.Success_Toast).text == "Successful operation"

        # 无线新增网址：jiadian.jd.com
        # 鼠标移动到切换“我的WiFi”按钮上
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.presence_of_element_located((By.XPATH, CommonLocators.LEVEL_1_MyWifi))
        )
        mouse = self.driver.find_element_by_xpath(CommonLocators.LEVEL_1_MyWifi)
        ActionChains(self.driver).move_to_element(mouse).perform()
        # 点击 接入设备
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, CommonLocators.Devices))
        ).click()
        self.driver.refresh()
        # 点击主网-设置
        Set = DevicesLocators.Set.format(num=2)
        WebDriverWait(self.driver, const.SLOW_WAIT + 10).until(
            EC.element_to_be_clickable((By.XPATH, Set))
        )
        time.sleep(0.5)
        self.driver.find_element_by_xpath(Set).click()
        # 切换到网址黑名单页
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Page_WebsiteBlacklist))
        ).click()
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Add))
        ).click()
        # 输入：jiadian.jd.com
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Website))
        ).send_keys("jiadian.jd.com")
        # 完成添加
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Save))
        ).click()
        # 断言:toast提示：添加成功
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
        )
        assert self.driver.find_element_by_xpath(CommonLocators.Success_Toast).text == "Successful operation"
        self.driver.refresh()
        List_Website = WebsiteBlacklistLocators.List_Website.format(num=1)
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, List_Website))
        )
        assert self.driver.find_element_by_xpath(List_Website).text == "jiadian.jd.com"
        # 判断：需要开关开启
        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        if Statu_class == "switch switch-animation":
            # 打开网址黑名单开关
            time.sleep(1)
            WebDriverWait(self.driver, const.SLOW_WAIT).until(
                EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
            ).click()
            # 断言:toast提示：打开开关成功
            WebDriverWait(self.driver, const.SLOW_WAIT).until(
                EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
            )
            assert self.driver.find_element_by_xpath(CommonLocators.Success_Toast).text == "Successful operation"




    #@unittest.skip("跳过")
    def test_Q_limitWebsiteBlacklist_8(self):
        """【备注】用例-4835:开关开启，多个设备添加多个网址黑名单，功能生效"""

        # 前提条件：有线网址为：www.baidu.com、news.baidu.com； 无线网址为：jiadian.jd.com、www.jd.com。并且开关均开启

        # 判断有线
        # 鼠标移动到切换“我的WiFi”按钮上
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.presence_of_element_located((By.XPATH, CommonLocators.LEVEL_1_MyWifi))
        )
        mouse = self.driver.find_element_by_xpath(CommonLocators.LEVEL_1_MyWifi)
        ActionChains(self.driver).move_to_element(mouse).perform()
        # 点击 接入设备
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, CommonLocators.Devices))
        ).click()
        self.driver.refresh()
        # 点击主网-设置
        Set = DevicesLocators.Set.format(num=1)
        WebDriverWait(self.driver, const.SLOW_WAIT + 10).until(
            EC.element_to_be_clickable((By.XPATH, Set))
        )
        time.sleep(0.5)
        self.driver.find_element_by_xpath(Set).click()
        # 切换到网址黑名单页
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Page_WebsiteBlacklist))
        ).click()
        List_Website_1 = WebsiteBlacklistLocators.List_Website.format(num=1)
        List_Website_2 = WebsiteBlacklistLocators.List_Website.format(num=2)
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, List_Website_1))
        )
        time.sleep(0.5)
        List_Website_1_Text = self.driver.find_element_by_xpath(List_Website_1).text
        List_Website_2_Text = self.driver.find_element_by_xpath(List_Website_2).text
        if List_Website_1_Text != "news.baidu.com" and List_Website_2_Text != "www.baidu.com":
            print("【备注】该用例无法验证，原因：有线设备没有2个网址：www.baidu.com、news.baidu.com")
            assert False
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
        )
        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        if Statu_class != "switch switch-animation checked":
            print("【备注】该用例无法验证，原因：有线设备网址黑名单开关为关")
            assert False

        # 判断无线
        # 鼠标移动到切换“我的WiFi”按钮上
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.presence_of_element_located((By.XPATH, CommonLocators.LEVEL_1_MyWifi))
        )
        mouse = self.driver.find_element_by_xpath(CommonLocators.LEVEL_1_MyWifi)
        ActionChains(self.driver).move_to_element(mouse).perform()
        # 点击 接入设备
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, CommonLocators.Devices))
        ).click()
        self.driver.refresh()
        # 点击主网-设置
        Set = DevicesLocators.Set.format(num=2)
        WebDriverWait(self.driver, const.SLOW_WAIT + 10).until(
            EC.element_to_be_clickable((By.XPATH, Set))
        )
        time.sleep(0.5)
        self.driver.find_element_by_xpath(Set).click()
        # 切换到网址黑名单页
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Page_WebsiteBlacklist))
        ).click()
        List_Website_1 = WebsiteBlacklistLocators.List_Website.format(num=1)
        List_Website_2 = WebsiteBlacklistLocators.List_Website.format(num=2)
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, List_Website_1))
        )
        time.sleep(0.5)
        List_Website_1_Text = self.driver.find_element_by_xpath(List_Website_1).text
        List_Website_2_Text = self.driver.find_element_by_xpath(List_Website_2).text
        if List_Website_1_Text != "jiadian.jd.com" and List_Website_2_Text != "www.jd.com":
            print("【备注】该用例无法验证，原因：无线设备没有2个网址：jiadian.jd.com、www.jd.com")
            assert False
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
        )
        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        if Statu_class != "switch switch-animation checked":
            print("【备注】该用例无法验证，原因：无线设备网址黑名单开关为关")
            assert False


        # 前提已完成，开始检验用例
        Result = Test_website_blacklist.test_website_blacklist_8()
        print(Result)
        if Result == 1:
            print("【成功】开关开启，多个设备添加多个网址黑名单，功能生效")
            assert True
        else:
            print("【失败】开关开启，多个设备添加多个网址黑名单，功能不生效")
            assert False





    #@unittest.skip("跳过")
    def test_R_limitWebsiteBlacklist_delete(self):
        """操作步骤：无线删除所有网址，有线只有网址www.baidu.com。并且将开关关闭"""

        # 无线：删除所有网址
        # 鼠标移动到切换“我的WiFi”按钮上
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.presence_of_element_located((By.XPATH, CommonLocators.LEVEL_1_MyWifi))
        )
        mouse = self.driver.find_element_by_xpath(CommonLocators.LEVEL_1_MyWifi)
        ActionChains(self.driver).move_to_element(mouse).perform()
        # 点击 接入设备
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, CommonLocators.Devices))
        ).click()
        self.driver.refresh()
        # 点击主网-设置
        Set = DevicesLocators.Set.format(num=2)
        WebDriverWait(self.driver, const.SLOW_WAIT + 10).until(
            EC.element_to_be_clickable((By.XPATH, Set))
        )
        time.sleep(0.5)
        self.driver.find_element_by_xpath(Set).click()
        # 切换到网址黑名单页
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Page_WebsiteBlacklist))
        ).click()
        flag = False
        while flag == False:
            try:
                assert self.driver.find_element_by_xpath(WebsiteBlacklistLocators.List_Null).is_displayed()
                flag = True
            except:
                Delete = WebsiteBlacklistLocators.Delete.format(num="last()")
                WebDriverWait(self.driver, const.SLOW_WAIT).until(
                    EC.element_to_be_clickable((By.XPATH, Delete))
                ).click()
                # 断言:toast提示：成功
                WebDriverWait(self.driver, const.SLOW_WAIT).until(
                    EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
                )
                time.sleep(2)
        # 断言：删除成功
        self.driver.refresh()
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.List_Null))
        )
        assert self.driver.find_element_by_xpath(WebsiteBlacklistLocators.List_Null).is_displayed()

        # 有线：只保留网址www.baidu.com
        # 鼠标移动到切换“我的WiFi”按钮上
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.presence_of_element_located((By.XPATH, CommonLocators.LEVEL_1_MyWifi))
        )
        mouse = self.driver.find_element_by_xpath(CommonLocators.LEVEL_1_MyWifi)
        ActionChains(self.driver).move_to_element(mouse).perform()
        # 点击 接入设备
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, CommonLocators.Devices))
        ).click()
        self.driver.refresh()
        # 点击主网-设置
        Set = DevicesLocators.Set.format(num=1)
        WebDriverWait(self.driver, const.SLOW_WAIT + 10).until(
            EC.element_to_be_clickable((By.XPATH, Set))
        )
        time.sleep(0.5)
        self.driver.find_element_by_xpath(Set).click()
        # 切换到网址黑名单页
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Page_WebsiteBlacklist))
        ).click()
        Delete = WebsiteBlacklistLocators.Delete.format(num=1)
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, Delete))
        ).click()
        # 断言:toast提示：成功
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
        )
        # 关闭开关
        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        if Statu_class == "switch switch-animation checked":
            # 关闭网址黑名单开关
            time.sleep(1)
            WebDriverWait(self.driver, const.SLOW_WAIT).until(
                EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
            ).click()
            # 断言:toast提示：关闭开关成功
            WebDriverWait(self.driver, const.SLOW_WAIT).until(
                EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
            )
            assert self.driver.find_element_by_xpath(CommonLocators.Success_Toast).text == "Successful operation"





    #@unittest.skip("跳过")
    def test_S_limitWebsiteBlacklist_9(self):
        """【备注】用例-4838: 开关关闭，设备A添加一个网址黑名单a，设备A可以访问网址a，设备B可以访问网址a"""

        # 前提条件：有线网址为：www.baidu.com； 无线没有网址。并且使有线黑名单开关关闭

        # 判断无线
        # 鼠标移动到切换“我的WiFi”按钮上
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.presence_of_element_located((By.XPATH, CommonLocators.LEVEL_1_MyWifi))
        )
        mouse = self.driver.find_element_by_xpath(CommonLocators.LEVEL_1_MyWifi)
        ActionChains(self.driver).move_to_element(mouse).perform()
        # 点击 接入设备
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, CommonLocators.Devices))
        ).click()
        self.driver.refresh()
        # 点击主网-设置
        Set = DevicesLocators.Set.format(num=2)
        WebDriverWait(self.driver, const.SLOW_WAIT + 10).until(
            EC.element_to_be_clickable((By.XPATH, Set))
        )
        time.sleep(0.5)
        self.driver.find_element_by_xpath(Set).click()
        # 切换到网址黑名单页
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Page_WebsiteBlacklist))
        ).click()

        try:
            WebDriverWait(self.driver, const.SLOW_WAIT).until(
                EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.List_Null))
            )
            assert self.driver.find_element_by_xpath(WebsiteBlacklistLocators.List_Null).is_displayed()
        except:
            print("【备注】该用例无法验证，原因：无线设备网址不为空")
            assert False

        # 判断有线
        # 鼠标移动到切换“我的WiFi”按钮上
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.presence_of_element_located((By.XPATH, CommonLocators.LEVEL_1_MyWifi))
        )
        mouse = self.driver.find_element_by_xpath(CommonLocators.LEVEL_1_MyWifi)
        ActionChains(self.driver).move_to_element(mouse).perform()
        # 点击 接入设备
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, CommonLocators.Devices))
        )
        time.sleep(0.5)
        self.driver.find_element_by_xpath(CommonLocators.Devices).click()
        self.driver.refresh()
        # 点击主网-设置
        Set = DevicesLocators.Set.format(num=1)
        WebDriverWait(self.driver, const.SLOW_WAIT + 10).until(
            EC.element_to_be_clickable((By.XPATH, Set))
        )
        time.sleep(0.5)
        self.driver.find_element_by_xpath(Set).click()
        # 切换到网址黑名单页
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Page_WebsiteBlacklist))
        ).click()
        List_Website_1 = WebsiteBlacklistLocators.List_Website.format(num=1)
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, List_Website_1))
        )
        time.sleep(0.5)
        List_Website_1_Text = self.driver.find_element_by_xpath(List_Website_1).text
        if List_Website_1_Text != "www.baidu.com":
            print("【备注】该用例无法验证，原因：有线设备没有网址：www.baidu.com")
            assert False
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
        )
        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        if Statu_class != "switch switch-animation":
            print("【备注】该用例无法验证，原因：有线设备网址黑名单开关为开")
            assert False



        # 前提已完成，开始检验用例
        Result = Test_website_blacklist.test_website_blacklist_9()
        print(Result)
        if Result == 1:
            print("【成功】设备A添加网址a，开关关闭，设备A和设备B均可访问网址a")
            assert True
        else:
            print("【失败】设备A添加网址a，开关关闭，设备A和设备B不可访问网址a")
            assert False






    #@unittest.skip("跳过")
    def test_T_limitWebsiteBlacklist_delete(self):
        """操作步骤：将黑名单恢复到初始配置"""
        # 有线
        flag = False
        while flag == False:
            try:
                assert self.driver.find_element_by_xpath(WebsiteBlacklistLocators.List_Null).is_displayed()
                flag = True
            except:
                Delete = WebsiteBlacklistLocators.Delete.format(num="last()")
                WebDriverWait(self.driver, const.SLOW_WAIT).until(
                    EC.element_to_be_clickable((By.XPATH, Delete))
                ).click()
                # 断言:toast提示：成功
                WebDriverWait(self.driver, const.SLOW_WAIT).until(
                    EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
                )
                time.sleep(2)

        # 断言：用例-1987 : 删除一个网址，删除成功，从列表消失
        self.driver.refresh()
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.List_Null))
        )
        assert self.driver.find_element_by_xpath(WebsiteBlacklistLocators.List_Null).is_displayed()

        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        if Statu_class == "switch switch-animation checked":
            # 关闭网址黑名单开关
            time.sleep(1)
            WebDriverWait(self.driver, const.SLOW_WAIT).until(
                EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
            ).click()
            # 断言:toast提示：关闭开关成功
            WebDriverWait(self.driver, const.SLOW_WAIT).until(
                EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
            )
            assert self.driver.find_element_by_xpath(CommonLocators.Success_Toast).text == "Successful operation"

        self.driver.refresh()
        # 断言：判断开关是否关闭
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
        )
        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        assert Statu_class == "switch switch-animation", Statu_class


        # 无线
        # 鼠标移动到切换“我的WiFi”按钮上
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.presence_of_element_located((By.XPATH, CommonLocators.LEVEL_1_MyWifi))
        )
        mouse = self.driver.find_element_by_xpath(CommonLocators.LEVEL_1_MyWifi)
        ActionChains(self.driver).move_to_element(mouse).perform()
        # 点击 接入设备
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, CommonLocators.Devices))
        ).click()
        self.driver.refresh()
        # 点击主网-设置
        Set = DevicesLocators.Set.format(num=2)
        WebDriverWait(self.driver, const.SLOW_WAIT + 10).until(
            EC.element_to_be_clickable((By.XPATH, Set))
        )
        time.sleep(0.5)
        self.driver.find_element_by_xpath(Set).click()
        # 切换到网址黑名单页
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Page_WebsiteBlacklist))
        ).click()
        flag = False
        while flag == False:
            try:
                assert self.driver.find_element_by_xpath(WebsiteBlacklistLocators.List_Null).is_displayed()
                flag = True
            except:
                Delete = WebsiteBlacklistLocators.Delete.format(num="last()")
                WebDriverWait(self.driver, const.SLOW_WAIT).until(
                    EC.element_to_be_clickable((By.XPATH, Delete))
                ).click()
                # 断言:toast提示：成功
                WebDriverWait(self.driver, const.SLOW_WAIT).until(
                    EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
                )
                time.sleep(2)

        # 断言：用例-1987 : 删除一个网址，删除成功，从列表消失
        self.driver.refresh()
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.List_Null))
        )
        assert self.driver.find_element_by_xpath(WebsiteBlacklistLocators.List_Null).is_displayed()

        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        if Statu_class == "switch switch-animation checked":
            # 关闭网址黑名单开关
            time.sleep(1)
            WebDriverWait(self.driver, const.SLOW_WAIT).until(
                EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
            ).click()
            # 断言:toast提示：关闭开关成功
            WebDriverWait(self.driver, const.SLOW_WAIT).until(
                EC.presence_of_element_located((By.XPATH, CommonLocators.Success_Toast))
            )
            assert self.driver.find_element_by_xpath(CommonLocators.Success_Toast).text == "Successful operation"

        self.driver.refresh()
        # 断言：判断开关是否关闭
        WebDriverWait(self.driver, const.SLOW_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, WebsiteBlacklistLocators.Statu))
        )
        Statu_class = self.driver.find_element_by_xpath(WebsiteBlacklistLocators.Statu).get_attribute('class')
        assert Statu_class == "switch switch-animation", Statu_class



def core():
    s = []
    class_tests = [
        # 建议执行顺序（倒序排如下）：
        # 管理路由器、管理密码、工作方式、限时（？如果被限制住未删掉情况怎么处理）
        LimitWebsiteBlacklist
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
    result.report(filename="路由器功能自动化测试",
                  description="路由器功能自动化测试报告",
                  log_path=log_path)