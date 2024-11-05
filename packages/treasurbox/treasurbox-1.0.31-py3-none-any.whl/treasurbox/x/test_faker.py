#!/usr/bin/env Python
# _*_coding:utf-8 _*_
# @Time: 2024-09-30 15:43:18
# @Author: Alan
# @File: test_faker.py
# @Describe:

"""
pip install faker
and test faker
"""

import datetime
import time
from faker import Factory, Faker
from fake_useragent import UserAgent
import numpy as np


fake = Faker(locale="zh_CN")    # 创建Faker对象 并设置本地化为中国


class FakerMaker:
    "use Faker make data"

    def username(self, count):
        """
        用户名
        """
        user_name = [fake.user_name() for i in range(count)]
        return user_name

    def password(self, count):
        """
        密码
        """
        pass_word = [fake.password(special_chars=False) for i in range(count)]
        return pass_word

    def date_time(self, count=1):
        """
        随机日期时间
        fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)  本年内的某个日期
        fake.date_time_this_month  本月内的某个日期 参数同上
        fake.date_time_this_decad  本年代内的某个日期 参数同上
        fake.date_time_this_century  本世界内的某个日期 参数同上
        fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None)    两个时间间的某个日期
        """
        my_list = []
        get_date = [fake.date_time_this_year(
            before_now=True, after_now=False, tzinfo=None) for i in range(count)]
        # get_date的列表是datetime.datetime(2018, 2, 13, 21, 52, 30)的格式 需要调用datetime 并用strftime修改输出格式
        for i in get_date:
            get_datetime = i.strftime('%Y-%m-%d %X')
            my_list.append(get_datetime)
        return my_list

    def datetime_before_days(self, count):
        """以当前日期时间为准 获取几天前的日期时间 如2018-03-22 15:22:31
        这不是随机的
        """
        datebefore = (datetime.datetime.now() -
                      datetime.timedelta(days=count)).strftime("%Y-%m-%d %X")
        return f'{count}天前的日期时间是: {datebefore}'

    def datetime_before_hours(self, count):
        """以当前日期时间为准 获取几小时前的日期时间 如2018-03-22 15:22:31
        这不是随机的
        """
        datebefore = (datetime.datetime.now() -
                      datetime.timedelta(hours=count)).strftime("%Y-%m-%d %X")
        return f'{count}小时前的日期时间是: {datebefore}'

    def datetime_before_minutes(self, count):
        """以当前日期时间为准 获取几分钟前的日期时间 如2018-03-22 15:22:31
        这不是随机的
        """
        datebefore = (datetime.datetime.now() -
                      datetime.timedelta(minutes=count)).strftime("%Y-%m-%d %X")
        return f'{count}分钟前的日期时间是: {datebefore}'

    def datetime_before_seconds(self, count):
        """以当前日期时间为准 获取几秒钟前的日期时间 如2018-03-22 15:22:31
        这不是随机的
        """
        datebefore = (datetime.datetime.now() -
                      datetime.timedelta(seconds=count)).strftime("%Y-%m-%d %X")
        return f'{count}秒前的日期时间是: {datebefore}'

    def datetime_today(self):
        """输出当前的日期时间 如2018-03-22 15:22:31
        这不是随机的
        """
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        my_today = time.strftime(ISOTIMEFORMAT, time.localtime())
        return f'当前日期时间是: {my_today}'

    def date_before(self, count):
        """以当前的日期为准 获取几天前的日期 如 2018-03-22"""
        my_datebefore = (datetime.date.today() +
                         datetime.timedelta(days=-count)).strftime('%Y-%m-%d')
        return f'{count}天前的日期是: {my_datebefore}'

    def date_today(self):
        """输出当前的日期 如2018-03-22 """
        my_today = datetime.date.today()
        return f'当前的日期是: {my_today}'

    def date(self, count):
        """
        日期
        fake.iso8601(tzinfo=None)   # 以iso8601标准输出的日期  '1973-11-16T22:58:37'
        fake.timezone()    # 时区   'America/Guatemala'
        fake.year()    # 随机年   '1974'
        fake.month()   # 随机月份  '02'
        fake.month_name()    # 随机月份名字    'August'
        fake.day_of_week()    # 随机星期几    Sunday'
        fake.day_of_month()   # 随机月中某一天
        fake.date(pattern="%Y-%m-%d")     # 随机日期（可自定义格式）    '1984-04-20'
        fake.date_object()    # 随机日期对象     datetime.date(1983, 1, 26)
        fake.date_time_ad(tzinfo=None)    # 公元后随机日期    datetime.datetime(341, 9, 11, 8, 6, 9)
        """
        pass

    def time(self, count):
        """
        时间
        fake.time(pattern="%H:%M:%S")    # 时间（可自定义格式）   '11:21:52'
        fake.am_pm() # 随机上午下午   'PM'
        fake.time_object()    # 随机时间对象     datetime.time(17, 8, 56)
        fake.unix_time()      # 随机unix时间（时间戳）    1223246848

        """
        pass

    def ipv4(self, count):
        """
        ip地址 ipv4
        """
        ip_addr = [fake.ipv4(network=False) for i in range(count)]
        return ip_addr

    def ipv6(self, count):
        """
        ip地址 ipv6
        """
        ip_addr = [fake.ipv6(network=False) for i in range(count)]
        return ip_addr

    def url(self, count):
        """
        url
        """
        my_url = [fake.url() for i in range(count)]
        return my_url

    def mac(self, count):
        """
        mac地址
        """
        my_mac = [fake.mac_address() for i in range(count)]
        return my_mac

    def email_addr(self, count=1):
        """
        普通邮箱
        fake.safe_email()   安全邮箱
        fake.company_email()   公司邮箱
        fake.free_email()    免费邮箱
        """
        # email = [fake.email() for i in range(count)]
        if count > 1:
            email = [fake.free_email() for i in range(count)]
        else:
            email = fake.free_email()
        return email

    def phonenumber(self, count):
        """
        手机号
        """
        my_phone = [fake.phone_number() for i in range(count)]
        return my_phone

    def idcard(self, count):
        """
        身份证号
        """
        my_id = [fake.ssn(min_age=18, max_age=90) for i in range(count)]
        return my_id

    def en_name(self, count):
        """
        英文名
        """
        my_enname = [fake.romanized_name() for i in range(count)]
        return my_enname

    def cn_name(self, count):
        """
        中文名
        fake.first_name_male()   男性姓名
        fake.name_male()    女性姓名
        """
        my_cnname = [fake.name() for i in range(count)]
        return my_cnname

    def random_int(self, count):
        """
        随机整数
        """
        my_int = [fake.pyint() for i in range(count)]
        return my_int

    def random_str(self, count):
        """
        随机字符串
        fake.pystr(min_chars=None, max_chars=20)：自定义长度的随机字符串
        """
        my_str = [fake.pystr() for i in range(count)]
        return my_str

    def postcode(self, count):
        """
        邮编
        """
        my_postcode = [fake.postcode() for i in range(count)]
        return my_postcode

    def addrss(self, count):
        """
        地址
        """
        my_addr = [fake.address() for i in range(count)]
        return my_addr

    def iban(self, count):
        """
        条形码
        """
        my_iban = [fake.iban() for i in range(count)]
        return my_iban

    def credit_card(self, count):
        """
        贷记卡
        """
        my_credit = [fake.credit_card_number() for i in range(count)]
        return my_credit

    def company(self, count):
        """
        公司名称
        """
        my_company = [fake.company() for i in range(count)]
        return my_company

    def sentences(self, count):
        """
        句子
        """
        my_sentences = [fake.sentences(nb=3, ext_word_list=None)
                        for i in range(count)]
        return my_sentences

    def paragraph(self, count):
        """一个段落"""
        my_paragraph = [fake.paragraph(
            nb_sentences=3, variable_nb_sentences=True, ext_word_list=None) for i in range(count)]
        return my_paragraph

    def paragraphs(self, count):
        """
        由几个段落组成的段落
        """
        my_paragraphs = [fake.paragraphs(
            nb=3, ext_word_list=None) for i in range(count)]
        return my_paragraphs

    def len_int(self, len, count):
        """
        固定位数的整数  len只能是8或13

        """
        my_randomint = [fake.ean(length=len) for i in range(count)]
        return my_randomint

    def time_stamp(self, count):
        """
        时间戳
        """
        my_timestamp = [fake.unix_time(
            end_datetime=None, start_datetime=None) for i in range(count)]
        return my_timestamp

    def money(self, count):
        """钱 float 小数点后2位有效数字"""
        ran = np.random.RandomState()    # RandomState生成随机数种子
        # ran.uniform(-0.1, 100.1)    # 设置金额范围
        # my_price = round(r, 2)    # 保留小数点后2位
        return [round(ran.uniform(-0.1, 100.1), 2) for i in range(count)]

    def country(self, count):
        """国家"""
        my_country = [fake.country() for i in range(count)]
        return my_country

    def user_agent(self):
        my_user_agent = UserAgent()
        return my_user_agent.random


def main():
    faker_maker = FakerMaker()
    # res = faker_maker.paragraphs(10)
    # print(res)
    # for _ in range(120):
    #     print('hello', end='')
    # res = faker_maker.user_agent()
    # print(res)
    # user_name = faker_maker.username(10)   # 10个用户名
    # print(user_name)

    # pass_word = faker_maker.password(10)   # 10个密码 没有特殊符号
    # print(pass_word)

    # date_time = faker_maker.date_time(10)    # 10个日期时间
    # print(date_time)

    # ipv4_addr = faker_maker.ipv4(10)    # 10个ipv4的地址
    # print(ipv4_addr)

    # ipv6_addr = faker_maker.ipv6(10)    # 10个ipv4的地址
    # print(ipv6_addr)

    # my_url = faker_maker.url(10)    # 10个url
    # print(my_url)

    # my_mac = faker_maker.mac(10)    # 10个mac地址
    # print(my_mac)

    # my_mailaddr = faker_maker.email_addr(10)     # 10个邮箱
    # print(my_mailaddr)

    # my_phone = faker_maker.phonenumber(10)    # 10个手机号
    # print(my_phone)

    # my_idcard = faker_maker.idcard(10)    # 10个身份证号
    # print(my_idcard)

    # my_enname = faker_maker.en_name(10)    # 10个 英文格式的名字 类似拼音
    # print(my_enname)

    # my_cnname = faker_maker.cn_name(10)    # 10个中文名
    # print(my_cnname)

    # my_int = faker_maker.random_int(10)   # 10个随机整数
    # print(my_int)

    # my_str = faker_maker.random_str(10)     # 10个随机字符串
    # print(my_str)

    # my_postcode = faker_maker.postcode(10)    # 10个邮编
    # print(my_postcode)

    # my_addr = faker_maker.addrss(10)     # 10个住宅地址
    # print(my_addr)

    # my_cr = faker_maker.credit_card(10)    # 10个贷记卡
    # print(my_cr)

    # my_lenint = faker_maker.len_int(8, 2)   # 长度为8的随机数字  2个
    # print(my_lenint)

    my_timestamp = faker_maker.time_stamp(1)    # 1个时间戳
    print(my_timestamp[0])

    # my_country = faker_maker.country(1)   # 1个国家
    # print(my_country[0])

    # my_price = faker_maker.money(9)   # 9个金额
    # print(my_price)

    # my_datetime_today = faker_maker.datetime_today()  # 当前日期时间
    # print(my_datetime_today)

    # my_date_befor_days = faker_maker.datetime_before_days(5)   # 当前日期时间 前n天的日期时间
    # print(my_date_befor_days)
    #
    # my_date_befor_hours = faker_maker.datetime_before_hours(10)    # n小时前的日期时间
    # print(my_date_befor_hours)
    #
    # my_date_befor_minutes = faker_maker.datetime_before_minutes(2)   # n分钟前的日期时间
    # print(my_date_befor_minutes)
    #
    # my_date_befor_seconds = faker_maker.datetime_before_seconds(14)    # n秒前的日期时间
    # print(my_date_befor_seconds)
    #
    # my_today = faker_maker.date_today()    # 当前日期
    # print(my_today)
    #
    # my_today_before_days = faker_maker.date_before(10)    #n天前的日期
    # print(my_today_before_days)

    # 不重复的邮箱
    # 创建一个集合存储生成的邮箱地址，确保无重复
    # email_addresses = set()

    # 设置生成邮箱的数量
    # number_of_emails = 10

    # 循环生成邮箱地址，直到满足数量需求
    # while len(email_addresses) < number_of_emails:
    #     email = faker_maker.email_addr()
    #     email_addresses.add(email)

    # 打印生成的邮箱地址列表
    # print(list(email_addresses))


if __name__ == '__main__':
    main()


# print(fake.name())
# print(fake.address())
# print(fake.email())
# print(fake.phone_number())
# print(fake.ipv4())
# print(fake.pystr(min_chars=0, max_chars=10))
# print(fake.text())
# print(fake.country())
# print(fake.postcode())
# print(fake.city())
# print(fake.city_name())
# print(fake.company())
# print(fake.credit_card_number())
# print(fake.currency_name())
# print(fake.date(pattern="%Y-%m-%d", end_datetime=None))
# print(fake.day_of_week())
# print(fake.file_name(category=None, extension=None))
