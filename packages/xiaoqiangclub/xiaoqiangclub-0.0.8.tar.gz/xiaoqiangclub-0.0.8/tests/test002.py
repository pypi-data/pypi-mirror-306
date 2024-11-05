import re
from typing import List


def split_string(s, symbols_regex: str = None, keep_symbols=False) -> List[str]:
    """
    分割字符串函数。

    :param s: 要分割的字符串。
    :param symbols_regex:要分割的字符串。
    :param keep_symbols:：是否保留符号。如果为 True，则保留符号；如果为 False，则去除符号。
    :return: 分割后的列表。
    """
    symbols_regex = symbols_regex or r'[ ，。？！、…\n,.?!~]+'

    if keep_symbols:
        result_text = []
        symbols = []
        words = []
        for char in s:
            if re.match(symbols_regex, char):
                symbols.append(char)
            else:
                if symbols:
                    words.extend(symbols)
                    result_text.append(''.join(words))
                    symbols.clear()
                    words.clear()
                words.append(char)
        if words:
            words.extend(symbols)
            result_text.append(''.join(words))
        return [text for text in result_text if text.strip()]
    else:
        return [re.sub(r'\s+', '', item) for item in re.split(symbols_regex, s) if item.strip()]


# 示例使用
text = "这是一个测试...还有其他标点！例如，,.。,或者。"
print(split_string(text, keep_symbols=False))
print(split_string(text, keep_symbols=True))
