# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/6/21 16:44
# @Author  : MuggleK
# @File    : random_ua.py

import random


class UserAgent(object):
    __PC_USER_AGENTS = (
        # chrome
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
        # opera
        "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
        "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
        "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
        "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
        "Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00",
        "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00",
        "Opera/12.0(Windows NT 5.2;U;en)Presto/22.9.168 Version/12.00",
        "Opera/12.0(Windows NT 5.1;U;en)Presto/22.9.168 Version/12.00",
        "Mozilla/5.0 (Windows NT 5.1) Gecko/20100101 Firefox/14.0 Opera/12.0",
        # firefox
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
        "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",
        "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/29.0",
        "Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0",
        # safari
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
        "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10",
        "Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko ) Version/5.1 Mobile/9B176 Safari/7534.48.3",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; da-dk) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; tr-TR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; ko-KR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; fr-FR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    )

    __MOBILE_USER_AGENTS = (
        # QQ浏览器
        "Mozilla/5.0 (Linux; Android 6.0; Le X620 Build/HEXCNFN5902012151S; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043015 Safari/537.36 V1_AND_SQ_6.6.9_482_YYB_D QQ/6.6.9.3060 NetType/2G WebP/0.3.0 Pixel/1080",
        "Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; LG-D859 Build/KVT49L.D85910d) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.4 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 6.0.1; ONEPLUS A3000 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043405 Safari/537.36 V1_AND_SQ_7.1.0_692_YYB_D QQ/7.1.0.3175 NetType/WIFI WebP/0.3.0 Pixel/1080",
        "Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; SM-N9006 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.5 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 7.0; EVA-AL00 Build/HUAWEIEVA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36 MQQBrowser/6.6",
        "Mozilla/5.0 (Linux; Android 5.0.2; Redmi Note 2 Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1920",
        "Mozilla/5.0 (Linux; Android 7.1.2; Redmi Note 3 Build/NJH47F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043602 Safari/537.36 V1_AND_SQ_7.2.5_744_YYB_D QQ/7.2.5.3305 NetType/WIFI WebP/0.3.0 Pixel/1080",
        "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; 1505-A02 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MI 5s Plus Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.2 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 6.0.1; SM-A8000 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043305 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080",
        # UC浏览器
        "Mozilla/5.0 (Linux; U; Android 8.0.0; zh-CN) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.9.5.975 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; MI 5 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.5.943 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; MHA-AL00 Build/HUAWEIMHA-AL00) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.6.1) WindVane/8.0.0 1080X1830 GCanvas/1.4.2.21",
        "Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; DUK-AL20 Build/HUAWEIDUK-AL20) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.6.4.950 UCBS/2.11.1.27 Mobile Safari/537.36 AliApp(TB/7.2.3) WindVane/8.0.0 1080X1812",
        "Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; M681C Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.1.939 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 5.0.2; zh-cn; vivo Y31 Build/LRX22G) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.6.0) WindVane/8.0.0 540X960 GCanvas/1.4.2.21",
        "Mozilla/5.0 (Linux; U; Android 7.1.1; zh-CN; MI MAX 2 Build/NMF26F) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.7.2.954 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; R7Plusm Build/LMY47V) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.5.2) WindVane/8.0.0 1080X1800 GCanvas/1.4.2.21",
        "Mozilla/5.0 (Linux; U; Android 6.0; zh-CN; HUAWEI MT7-TL10 Build/HuaweiMT7-TL10) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.3.0.907 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; KNT-AL20 Build/HUAWEIKNT-AL20) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.8.952 Mobile Safari/537.36",
        # MIUI浏览器
        "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; Coolpad 8675-A Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/46.0.2490.85 Mobile Safari/537.36 XiaoMi/MiuiBrowser/2.1.1",
        "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; MI 5 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.2.7",
        "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; MI 5 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/8.8.3",
        "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MI NOTE LTE Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.1.3",
        "Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; HM NOTE 1TD Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/8.5.14",
        "Mozilla/5.0 (Linux; U; Android 6.0; zh-cn; Redmi Note 4 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.2.8",
        "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; Mi Note 2 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.2.8",
        "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; HM NOTE 1LTE Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.3.2",
        "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MI 4W Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/46.0.2490.85 Mobile Safari/537.36 XiaoMi/MiuiBrowser/8.2.15",
        "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MI MAX Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/8.6.5",
        # 傲游浏览器
        "Mozilla/5.0 (Linux; U; Android 2.3.5; zh-cn; U8800 Build/HuaweiU8800) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 4.0.3; zh-cn; M031 Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/537.4 Maxthon/%s",
        "Mozilla/5.0 (Android 5.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.9.4.1000 Chrome/39.0.2146.0 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Mobile Safari/537.36 Maxthon/3047",
        "Mozilla/5.0 (Windows NT 6.1; Android) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.9.2.1000",
        "Mozilla/5.0 (Linux; U; Android 4.2.1; zh-cn; M040 Build/JOP40D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 Maxthon/4.1.3.2000",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a",
        "Mozilla/5.0 (Linux; Android 7.0; MI 5 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36 Maxthon/3047",
        "Mozilla/5.0 (Linux; Android 7.0; MI 5 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36 Maxthon/3048",
        # 百度浏览器
        "Mozilla/5.0 (Linux; Android 5.1.1; vivo X6SPlus D Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.1 baidubrowser/7.15.15.0 (Baidu; P1 5.1.1)",
        "Mozilla/5.0 (Linux; Android 7.0; HUAWEI NXT-AL10 Build/HUAWEINXT-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 baidubrowser/7.9.12.0 (Baidu; P1 7.0)",
        "Mozilla/5.0 (Linux; Android 6.0.1; SM-C7000 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 baidubrowser/7.13.13.0 (Baidu; P1 6.0.1)",
        "Mozilla/5.0 (Linux; Android 6.0; HUAWEI NXT-AL10 Build/HUAWEINXT-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 baidubrowser/7.9.12.0 (Baidu; P1 6.0)",
        "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; H2 Build/KTU84P) AppleWebKit/534.24 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.24 T5/2.0 baidubrowser/5.6.4.7 (Baidu; P1 4.4.4)",
        "Mozilla/5.0 (Linux; Android 4.4.4; SM-N935F Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36 baidubrowser/7.13.13.0 (Baidu; P1 4.4.4)",
        "Mozilla/5.0 (Linux; Android 4.2.2; NX403A Build/JDQ39; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 baidubrowser/7.10.12.0 (Baidu; P1 4.2.2)",
        "Mozilla/5.0 (Linux; U; Android 4.0.3; zh-cn; M031 Build/IML74K) AppleWebKit/530.17 (KHTML, like Gecko) FlyFlow/2.3 Version/4.0 Mobile Safari/530.17 baidubrowser/023_1.41.3.2_diordna_069_046/uzieM_51_3.0.4_130M/1200a/963E77C7DAC3FA587DF3A7798517939D%7C408994110686468/1",
        "Mozilla/5.0 (Linux; Android 6.0; HUAWEI VNS-DL00 Build/HUAWEIVNS-DL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 baidubrowser/7.9.12.0 (Baidu; P1 6.0)",
        "Mozilla/5.0 (Linux; Android 6.0.1; MI 5s Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 baidubrowser/7.9.12.0 (Baidu; P1 6.0.1)",
    )

    ua_name = 'User-Agent'

    def __new__(cls, mobile_ua=False, default=False):
        if default:
            return cls.default_ua()

        if mobile_ua:
            return {cls.ua_name: random.choice(cls.__MOBILE_USER_AGENTS)}
        else:
            return {cls.ua_name: random.choice(cls.__PC_USER_AGENTS)}

    @staticmethod
    def random_ua():
        s_ver = [str(random.randint(10, 99)), '0', str(random.randint(1000, 9999)), str(random.randint(100, 999))]
        version = '.'.join(s_ver)
        webkit = 'AppleWebKit/537.36 (KHTML, like Gecko)'
        mac = '_'.join([str(random.randint(8, 12)) for _ in range(2)] + [str(random.randint(1, 10))])
        typeid = random.randint(1, 6)
        if typeid == 1:
            ua_ua = 'Mozilla/5.0 (Windows NT 7.1; WOW64) %s Chrome/%s Safari/537.36' % (webkit, version)
        elif typeid == 2:
            ua_ua = 'Mozilla/5.0 (Windows NT 10.1; WOW64) %s Chrome/%s Safari/537.36' % (webkit, version)
        elif typeid == 3:
            ua_ua = 'Mozilla/5.0 (Windows NT 8.1; WOW64) %s Chrome/%s Safari/537.36' % (webkit, version)
        else:
            ua_ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X %s) %s Chrome/%s Safari/537.36' % (mac, webkit, version)
        return ua_ua

    @classmethod
    def default_ua(cls):
        return {cls.ua_name: cls.random_ua()}
