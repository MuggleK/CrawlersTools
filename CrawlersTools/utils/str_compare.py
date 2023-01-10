#!/usr/bin/env python
# -*- coding: utf-8 -*-


def str_compare(str1: str, str2: str, half_compare=False) -> bool:
    """
    比较两个字符串是否相等，当half_compare为True时会把字符串转为半角字符串之后在比较
    适用：比较两个公司名，原则上 特斯拉（上海）有限公司 和 特斯拉(上海)有限公司 这两个公司是同一个，但是因为一个是全角括号，一个是半角括号，
        直接比较会导致两个公司名不相等，这时候转换为半角在进行比较则不会出现这个问题.
    """
    str1 = full_str_to_half_str(str1) if half_compare else str1
    str2 = full_str_to_half_str(str2) if half_compare else str2
    if str1 == str2:
        return True
    return False


def full_str_to_half_str(full_str: str) -> str:
    # 全角字符串转半角字符串
    half_str = ""
    for _str in full_str:
        _str_code = ord(_str)
        if _str_code == 12288:  # 全角空格转半角空格
            _str_code = 32
        elif 65281 <= _str_code <= 65374:
            _str_code -= 65248
        half_str += chr(_str_code)
    return half_str


if __name__ == '__main__':
    print(str_compare('特斯拉（上海）有限公司', '特斯拉(上海)有限公司'))
    print(str_compare('特斯拉（上海）有限公司', '特斯拉(上海)有限公司', half_compare=True)) # 全角括号转半角括号
    print(str_compare('　特斯拉(上海)有限公司', ' 特斯拉(上海)有限公司'))
    print(str_compare('　特斯拉(上海)有限公司', ' 特斯拉(上海)有限公司', half_compare=True))  # 全角空格转半角空格
