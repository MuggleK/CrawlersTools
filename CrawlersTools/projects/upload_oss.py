# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/8/12 20:20
# @Author  : MuggleK
# @File    : upload_oss.py

import base64
import hashlib
import re

import httpx
from loguru import logger

from CrawlersTools import base_requests
from CrawlersTools.requests.proxy import get_proxies


class UploadOss(object):
    """
    A Class for QZD Upload file to oss

    Usage:

    ```python
    >>> upload = UploadOss('(pdf|txt|doc|docx|xlsx|xls|csv|wps|hlp|rtf|ppt|pptx|zip|rar|jar|gz|jpg|jpeg|png|tif|gif|bmp)', "https://***")
    >>> oss_url, oss_uuid = upload.download("http://xxgk.haiyan.gov.cn/gov/jcms_files/jcms1/web7/site/zfxxgk/download/downfile.jsp?classid=0&filename=140901165845693.xls", '附件')
    ```
    """

    def __init__(self, oss_url, suffix_reg, oss_code=None, client_code=None):
        self.suffix_reg = suffix_reg
        self.oss_url = oss_url
        self.oss_code = oss_code
        self.client_code = client_code

    def download(self, file_url, file_name, headers=None, verify=True):
        """

        :param file_url:
        :param file_name:
        :param headers:
        :param verify:
        :return:
        """
        location = global_uuid = ""
        proxy = None
        headers = headers if headers else {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
        for _ in range(3):
            try:
                if ";base64," in file_url:
                    suffix = "png"
                    logger.debug(f"正在上传base64图片: {file_name}: {file_url}")
                    hl = hashlib.md5()
                    hl.update(file_url.encode(encoding='utf-8'))
                    file_name = hl.hexdigest() + f".{suffix}"
                    a = file_url.split(";base64,")[-1]
                    a = a + '=' * (4 - len(a) % 4) if len(a) % 4 != 0 else a
                    base64str = base64.b64decode(a)
                    upload_result = self.post_file(file_name, base64str)
                    location = upload_result.get("downloadLocation")
                    global_uuid = upload_result.get("globalUuid")
                    logger.debug(f"文件上传成功: {file_name}: {file_url}")
                else:
                    suffix = self.complete_name(file_url, file_name, self.suffix_reg)
                    if not file_url.startswith("http") and not suffix:
                        return location, global_uuid
                    file_name = f"{file_name}.{suffix}"
                    logger.debug(f"正在上传文件: {file_name}: {file_url}")
                    res = base_requests(file_url, timeout=60, headers=headers, verify=verify, proxies=proxy)
                    if 200 <= res.status_code < 400:
                        upload_result = self.post_file(file_name, res)
                        location = upload_result.get("downloadLocation")
                        global_uuid = upload_result.get("globalUuid")
                        logger.debug(f"文件上传成功: {file_name}: {file_url}")
                        break
                    elif res.status_code == 404 or res.status_code == 500:
                        logger.debug(f"文件地址无效: {file_name}: {file_url}")
                        break
            except Exception as e:
                logger.warning(f"文件上传异常: {file_name}: {e}")
                proxy = get_proxies(http2=True)
                continue
        else:
            logger.error(f"文件上传失败: {file_name}: {file_url}")

        return location, global_uuid

    def post_file(self, name, resp):
        params_json = {
            "name": name,
            "appCode": self.oss_code,
            "appClientCode": self.client_code,
            "appOrgCode": "",
            "appUserId": "",
            "ownCatalogUuid": ""
        }
        json_data = httpx.post(self.oss_url, json=params_json).json()
        if json_data.get("msg") == "SUCCESS":
            token_data = json_data.get("data", {})

            str_dic = {
                "key": token_data.get("dir") + token_data.get("name"),
                "policy": token_data.get("policy"),
                "OSSAccessKeyId": token_data.get("accessid"),
                "success_action_status": 200,
                "callback": token_data.get("callback"),
                "signature": token_data.get("signature"),
            }

            files = {'file': resp.content}
            response = httpx.post(token_data.get("host"), data=str_dic, files=files)
            if response.status_code == 200:
                res_data = response.json()
                if res_data.get("msg") == "SUCCESS":
                    return res_data["data"]

        raise ValueError(f"文件上传oss失败：{name}")

    @staticmethod
    def complete_name(url, name, suffix_reg):
        """
        附件.xls.doc 可上传, 接口会默认取最后一个
        优先取 file_url 后缀
        """
        is_name_suffix = re.search(suffix_reg, name, re.I)
        is_url_suffix = re.search(suffix_reg, url, re.I)
        name_suffix = is_name_suffix.group(1) if is_name_suffix else ""
        url_suffix = is_url_suffix.group(1) if is_url_suffix else ""
        if url_suffix:
            suffix = url_suffix
        elif name_suffix:
            suffix = name_suffix
        else:
            suffix = ""

        return suffix
