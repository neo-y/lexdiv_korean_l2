"""
민수가 학교에 갔습니다.
==> [민수, 학교, 가다]
==> 조사 제외
==> 동사는 stemming
"""
import os
import random
from konlpy.tag import Okt

STOPWORDS_POS = ['URL', 'Email', 'ScreenName', 'Hashtag', 'KoreanParticle', 'Punctuation', 'Foreign', 'Alpha', 'Number',
                 'Unknown']
CONTENT_POS = ['Noun', 'Verb', 'Adjective', 'Adverb']


# PUNCTUATION = "`` '' ' . , ? ! ) ( % / - _ -LRB- -RRB- SYM : ;".split(" ")
# def remove_special_char(raw_text):
#     for x in PUNCTUATION:
#         raw_text = raw_text.replace(x, "")
#     punc_removed = re.sub('\s+', ' ', raw_text)
#     return punc_removed


def remove_stop_words(token_pos_tuple, content_only=False):
    """
    :param content_only: boolean, if True, only content words (verb, noun, adjective, adverb) are included in the output.
    :param token_pos_tuple: list of tuple consisting of token and POS [('열심히', 'Adverb'), ('코딩', 'Noun')...]
    :return: list of tokens without stopwords
    """
    tokenized = []

    if content_only:  # include only content words:
        for index, pair in enumerate(token_pos_tuple):
            if pair[1] in CONTENT_POS:  # tuple[1] = POS
                tokenized.append(pair[0])

    else:  # include all words (function words + content words)
        for index, pair in enumerate(token_pos_tuple):
            if pair[1] not in STOPWORDS_POS:
                tokenized.append(pair[0])

    return tokenized


def tokenize(data, content_only=False):
    """
    tokenize sequences using okt tokenizer from konlpy.
    :param data: str, raw text
    :param content_only: boolean, if True, only content words (verb, noun, adjective, adverb) are included in the output.
    :return:
    """
    okt = Okt()

    # tokenize (verb stemmer included)
    pos_tuple = okt.pos(data, norm=True, stem=True)

    # remove stopwords
    tokenized = remove_stop_words(pos_tuple, content_only=content_only)

    return pos_tuple, tokenized


def write_tokenized_output(number_of_files=5):
    """
    TODO move this function to separate script
    :param number_of_files:
    :return:
    """
    random.seed(1)

    while number_of_files > 0:
        number_of_files -= 1
        file = random.choice(os.listdir("../data/selected"))
        file_dir = "../data/selected/" + file
        with open(file_dir, encoding='utf-8') as f:
            lines = f.read()
            pos, tokenized = tokenize(lines)
            # print(lines)
            # print(pos)
            # print(tokenized)
            output_dir = "../data/output/" + file[:-4] + "_Output.txt"
            with open(output_dir, "w", encoding='utf-8') as output_file:
                output_file.write(lines)
                output_file.write('\n\n')
                output_file.write(str(pos))
                output_file.write('\n\n')
                output_file.write(str(tokenized))


if __name__ == '__main__':
    pass
