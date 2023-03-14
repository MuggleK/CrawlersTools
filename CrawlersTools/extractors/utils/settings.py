# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/8/19 20:00
# @Author  : MuggleK
# @File    : settings.py

# list settings
LIST_MIN_NUMBER = 5
LIST_MIN_LENGTH = 8
LIST_MAX_LENGTH = 50
SIMILARITY_THRESHOLD = 0.8

LIST_AVG_LENGTH = 9
ADDTION_RIGHT_NUM = 10000

HIGH_WEIGHT_ERROR_KEYWORD = ["ICP备", "公网安备", "网公安备", "备案序号：", "网站地图"]
DIRECTORY_ERROR_TITLE = ["首页", "下一页", "解读", "图解", "详细", "阅读全文", "标题", "[详细]"]


# common settings
SPECIAL_SYMBOL_MAP = {
    "&quot;": '"',
    "&amp;": "&",
    "&lt;": "<",
    "&gt;": ">",
    "&nbsp;": " ",
    "&#34;": '"',
    "&#38;": "&",
    "&#60;": "<",
    "&#62;": ">",
    "&#160;": " ",
    '<script type="text/xml">': "",
    "<script type='text/xml'>": "",
}

ERROR_NAV_LIST = ['Copyright', 'ICP备', 'QQ空间', '上一篇', '下一篇', '专题专栏', '主题分类', '主题词：', '二维码', '互动交流', '人人网', '优质工程评审',
                  '使用帮助', '依申请公开', '信息公开', '信息公开制度', '信息公开年报', '信息公开指南', '信息发布', '免责声明', '党建专栏', '党建工作', '党组织概况',
                  '公示公告', '公网安备', '关闭窗口', '分享到', '分类：', '办事服务', '加入收藏', '区政府文件', '协会文件', '协会章程', '协会简介', '协会领导', '发布日期',
                  '发布日期', '发布时间', '发布机构', '发文日期', '名称：', '基层政务公开标准化规范化', '备案序号', '字体', '安全人员培训', '市场信用评价', '当前位置',
                  '您当前的位置', '您现在所在的位置', '您的位置', '意见征集', '成文日期', '手机阅读', '打印', '打印本页', '打印此页', '扫一扫', '收藏本站', '政务公开',
                  '政务服务', '政府信息公开', '政府信息公开制度', '政府信息公开年报+', '政府信息公开指南', '政府信息公开申请表', '政府公报', '政府动态', '政府网站工作报表',
                  '政策文件', '政策法规', '新浪微博', '新闻公告', '无障碍浏览', '机构概况', '机构职能', '机构设置', '来源:', '来源：', '标题', '法定主动公开内容',
                  '法定主动公开内容+', '法定主动公开目录', '法规文件', '浏览器版本过低', '浏览次数', '浏览统计', '浏览量', '浏览量', '点击次数', '点击量', '版权所有',
                  '生成时间', '电子期刊', '科技动态', '科技资讯', '简繁', '索 引 号', '索引号', '组织机构', '网公安备', '网站地图', '网站建设', '网站标识码', '联系我们',
                  '联系我们', '腾讯微博', '行政规范性文件', '责任编辑', '返回顶部', '进度查询', '通知公告', '部门规章', '重大决策预公开', '门户网站', '预决算公开', '领导介绍',
                  '领导信箱', '首页']

# title settings
TITLE_EXTRACTOR_USELESS_TAGS = ["br", "BR", "script", "style"]

PUNCTUATION_ALPHA_PATTERN = '[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'

TITLE_HTAG_XPATH = '(//h1//text() | //h2//text() | //h3//text() | //h4//text() | //h5//text() | //title//text() | //*[contains(@class, "title")]/text() | //*[contains(@class, "Title")]/text() | //*[contains(@id, "title")]/text() | //*[contains(@id, "Title")]/text())'

TITLE_META_XPATH = '//meta[contains(@name, "Title")]/@content'

TITLE_META_XPATH_BAK = '//meta[contains(@name, "title")]/@content'

# time settings
DATETIME_PATTERN = [
    r"(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
    r"(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
    r"(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9])",
    r"(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9])",
    r"(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
    r"(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
    r"(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
    r"(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9])",
    r"(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9])",
    r"(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
    r"(\d{4}年\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
    r"(\d{4}年\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
    r"(\d{4}年\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9])",
    r"(\d{4}年\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9])",
    r"(\d{4}年\d{1,2}月\d{1,2}日\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
    r"(\d{2}年\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
    r"(\d{2}年\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
    r"(\d{2}年\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9])",
    r"(\d{2}年\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9])",
    r"(\d{2}年\d{1,2}月\d{1,2}日\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
    r"(\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
    r"(\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
    r"(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2})",  # TODO 年月日与符号优先级
    r"(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2})",
    r"(\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9])",
    r"(\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9])",
    r"(\d{1,2}月\d{1,2}日\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
    r"(\d{4}年\d{1,2}月\d{1,2}日)",
    r"(\d{2}年\d{1,2}月\d{1,2}日)",
    r"(\d{1,2}月\d{1,2}日)",
]

PUBLISH_TIME_META = [  # 部分特别规范的网站，可以直接从 HTML 的 meta 数据中获得发布时间
    '//meta[starts-with(@property, "rnews:datePublished")]/@content',
    '//meta[starts-with(@property, "article:published_time")]/@content',
    '//meta[starts-with(@property, "og:published_time")]/@content',
    '//meta[starts-with(@property, "og:release_date")]/@content',
    '//meta[starts-with(@itemprop, "datePublished")]/@content',
    '//meta[starts-with(@itemprop, "dateUpdate")]/@content',
    '//meta[starts-with(@name, "OriginalPublicationDate")]/@content',
    '//meta[starts-with(@name, "article_date_original")]/@content',
    '//meta[starts-with(@name, "og:time")]/@content',
    '//meta[starts-with(@name, "apub:time")]/@content',
    '//meta[starts-with(@name, "publication_date")]/@content',
    '//meta[starts-with(@name, "sailthru.date")]/@content',
    '//meta[starts-with(@name, "PublishDate")]/@content',
    '//meta[starts-with(@name, "publishdate")]/@content',
    '//meta[starts-with(@name, "PubDate")]/@content',
    '//meta[starts-with(@name, "pubDate")]/@content',
    '//meta[starts-with(@name, "pubdate")]/@content',
    '//meta[starts-with(@name, "pubtime")]/@content',
    '//meta[starts-with(@name, "_pubtime")]/@content',
    '//meta[starts-with(@name, "weibo: article:create_at")]/@content',
    '//meta[starts-with(@pubdate, "pubdate")]/@content',
    '//meta[starts-with(@name, "firstpublishedtime")]/@content',
    '//*[contains(text(), "发布日期")]//text()',
    '//*[contains(text(), "发布时间")]//text()',
    '//*[contains(text(), "发布日期")]/..//text()',
    '//*[contains(text(), "发布时间")]/..//text()',
    '//*[contains(text(), "发布日期")]/../..//text()',
    '//*[contains(text(), "发布时间")]/../..//text()',
]

# attachments settings
ATTACHMENT_REGX = "(pdf|txt|doc|docx|xlsx|xls|csv|wps|hlp|rtf|ppt|pptx|zip|rar|jar|gz|jpg|jpeg|png|tif|gif|bmp|pic|mac|avi|mpg|mov|swf|wav|aif|au|mp3|ram|wma|mmf|amr|aac|flac|et|ofd|webp|jfif)(?:&classid=\\-?[0-9]+|\?docid=[0-9]+)?$"
