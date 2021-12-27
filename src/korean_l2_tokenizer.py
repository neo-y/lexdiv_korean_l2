"""
민수가 학교에 갔습니다.
==> [민수, 학교, 가다]
==> 조사 제외
==> 동사는 stemming
"""

import re
from konlpy.tag import Okt

PUNCTUATION = "`` '' ' . , ? ! ) ( % / - _ -LRB- -RRB- SYM : ;".split(" ")
FUNCTION_POS = ['Josa']

def remove_special_char(raw_text):
    for x in PUNCTUATION:
        raw_text = raw_text.replace(x, "")
    punc_removed = re.sub('\s+', ' ', raw_text)
    return punc_removed


def remove_function_words(token_pos_tuple):
    """
    :param token_pos_tuple: list of tuple consisting of token and POS [('열심히', 'Adverb'), ('코딩', 'Noun')...]
    :return: list of tokens without function words
    """
    tokenized = []
    for index, tuple in enumerate(token_pos_tuple):
        if tuple[1] not in FUNCTION_POS: # tuple[1] = POS
            tokenized.append(tuple[0])

    return tokenized

def okt_tokenizer(data):
    okt = Okt()
    # remove special characters
    data = remove_special_char(data)

    # tokenize (verb stemmer included)
    pos_tuple = okt.pos(data, norm=True, stem=True)

    # remove function words
    tokenized = remove_function_words(pos_tuple)

    return pos_tuple, tokenized

if __name__ == '__main__':
    data = """
    특히 늦은 시간에 잠을 자는 것과 행야 할 일을 뒤로 미루는 것이 고치고 싶은 생활 습관이다. """

    print("RAW DATA")
    print(data)

    pos, tokenized = okt_tokenizer(data)
    print("INTERMEDIATE RESULT: Part-Of-Speech ")
    print(pos)

    print("FINAL RESULT: FUNCTION WORDS DELETED")
    print(tokenized)