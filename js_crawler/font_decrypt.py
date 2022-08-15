# -*- coding: utf-8 -*-
# @Project : qzd_crawler_tools
# @Time    : 2022/8/12 16:11
# @Author  : Changchuan.Pei
# @File    : font_decrypt.py

from io import BytesIO

import ddddocr
import requests
from fontTools.ttLib import TTFont
from loguru import logger
from PIL import ImageFont, ImageDraw, Image


class FontDecrypt(object):
    """
    Usage::

        # >>>
        # >>> # 字体base64加密
        # >>> str_base64_ = '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 '
        # >>> font = FontDecrypt(str_base64=str_base64_)
        # >>> font.decrypt('𤵼𥙌腐进𤵝防护𥪵𤹩腐蚀𧒄𥉥𥪵𥌙测试𢺔𦰤𤵢𤵩𥤣𥎧𤹩𥤣𥎧')
        # 2022-01-20 17:01:47.932 | SUCCESS  | __main__:decrypt:89 - Out Decrypted Strings：中国腐进与防护学会腐蚀电化学及测试方法专业委员会委员
        # >>>
        # >>> # 字体链接
        # >>> font_url_ = 'https://ss.cods.org.cn/css/woff/791831.woff'
        # >>> font = FontDecrypt(font_url=font_url_)
        # >>> font.decrypt('┗┐┑┕┏┓┐┐┤┘┑┛┣┢┏┨┐┢')
        # 2022-01-20 17:01:48.519 | SUCCESS  | __main__:decrypt:89 - Out Decrypted Strings：92371522mA3dlk1q2k
        # >>>

    """

    ocr = ddddocr.DdddOcr()

    def __init__(self, font_url=None, str_base64=None, fontsize=30):
        """
        :param font_url: 仅支持woff和ttf格式字体
        :param str_base64: 字体base64
        :param fontsize:
        """
        self.img_mode = 'RGB'
        self.bg_color = (255, 255, 255)
        self.fg_color = (0, 0, 0)
        self.fontsize = fontsize
        self.font_url = font_url
        self.str_base64 = str_base64
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/93.0.4577.63 Safari/537.36'
        }
        self.encrypt_str = None
        self.font = None
        self.font_process()

    def font_base64(self):
        url = 'https://www.motobit.com/util/base64-decoder-encoder.asp?charset=iso-8859-1&acharset='
        data = {
            'tobase64text': self.str_base64,
            'tobase64': 'Convert the source data',
            'tobase64file': '(binary)',
            'maxLineChars': '76',
            'todo': 'decode',
            'output': 'file',
            # 'filename1': '1.ttf'
        }
        r = requests.post(url=url, headers=self.headers, data=data)
        return r.content

    def font_process(self):
        """
        TODO 修改FreeTypeFont对象源码支持字体bytes类型

        ***
        def load_from_bytes(f):
            if isinstance(f, bytes):    # 直接传入bytes
                self.font_bytes = f
            else:
                self.font_bytes = f.read()
            self.font = core.getfont(
                "", size, index, encoding, self.font_bytes, layout_engine
            )

        if isinstance(font, bytes): # 直接传入bytes
            load_from_bytes(font)
        elif isPath(font):
            ***
        """
        if self.font_url:
            font_content = requests.get(self.font_url, headers=self.headers).content
        else:
            font_content = self.font_base64()
        self.font = ImageFont.FreeTypeFont(font_content, self.fontsize)
        ttf = TTFont(BytesIO(font_content))
        # 混淆后字体列表
        self.encrypt_str = [chr(string) for string in ttf.getBestCmap().keys()]
        logger.debug(f'Encrypted Words List：{self.encrypt_str}')

    def draw_img(self, letters: str):
        letter_width, letter_height = self.font.getsize(letters)
        img_size = (letter_width + 10, letter_height + 10)
        img_width, img_height = img_size
        img = Image.new(self.img_mode, img_size, self.bg_color)
        draw_brush = ImageDraw.Draw(img)
        text_y = (img_height - letter_height + 1) / 2
        text_y = int(text_y)
        text_x = int((img_width - letter_width + 1) / 2)
        draw_brush.text((text_x, text_y), letters, fill=self.fg_color, font=self.font)
        return img

    def orc(self, word: str):
        img = self.draw_img(word)
        img_object = BytesIO()
        img.save(img_object, 'JPEG')
        res = self.ocr.classification(img_object.getvalue())
        return res

    def decrypt(self, word: str):
        logger.debug(f'In Encrypted Strings：{word}')
        string = ''
        for letter in word:
            if letter in self.encrypt_str:
                ocr_str = self.orc(letter)
                if ocr_str:
                    string += self.orc(letter)
                else:
                    string += letter
            else:
                string += letter
        logger.success(f'Out Decrypted Strings：{string}')
        return string
