"""
민수가 학교에 갔습니다.
==> [민수, 학교, 가다]
==> 조사 제외
==> 동사는 stemming
"""
import os
import random
from konlpy.tag import Okt
from vocabulary.vocab_clean import clean_vocab

STOPWORDS_POS = ['URL', 'Email', 'ScreenName', 'Hashtag', 'KoreanParticle', 'Punctuation', 'Foreign', 'Alpha', 'Number',
                 'Unknown']
CONTENT_POS = ['Noun', 'Verb', 'Adjective', 'Adverb']

CLEAN_VOCAB = clean_vocab


def remove_stop_words(token_pos_tuple, content_only=False):
    """
    :param content_only: boolean, if True, only content words (verb, noun, adjective, adverb) are included in the output.
    :param token_pos_tuple: list of tuple consisting of token and POS [('열심히', 'Adverb'), ('코딩', 'Noun')...]
    :return: list of tokens without stopwords
    """
    pos_tuple_cleaned = []

    if content_only:  # include only content words:
        for index, pair in enumerate(token_pos_tuple):
            if pair[1] in CONTENT_POS:  # tuple[1] = POS
                pos_tuple_cleaned.append(pair)

    else:  # include all words (function words + content words)
        for index, pair in enumerate(token_pos_tuple):
            if pair[1] not in STOPWORDS_POS:
                pos_tuple_cleaned.append(pair)

    return pos_tuple_cleaned


def tokenize(data, content_only=False, remove_typo=True):
    """
    tokenize sequences using okt tokenizer from konlpy.
    :param remove_typo: boolean if True, remove typo tokens using dictionary
    :param data: str, raw text
    :param content_only: boolean, if True, only content words (verb, noun, adjective, adverb) are included in the output.
    :return:
    """
    okt = Okt()

    # tokenize (verb stemmer included)
    pos_tuple_all = okt.pos(data, norm=True, stem=True)

    # remove stopwords
    pos_tuple_cleaned = remove_stop_words(pos_tuple_all, content_only=content_only)

    # remove typos
    if remove_typo:
        pos_tuple_cleaned = [item for item in pos_tuple_cleaned if item in CLEAN_VOCAB]

    # separate lists for tokens
    tokens_cleaned = [item[0] for item in pos_tuple_cleaned]

    return pos_tuple_all, pos_tuple_cleaned, tokens_cleaned


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
            pos_all, _, tokenized = tokenize(lines)
            output_dir = "../data/output/" + file[:-4] + "_Output.txt"
            with open(output_dir, "w", encoding='utf-8') as output_file:
                output_file.write(lines)
                output_file.write('\n\n')
                output_file.write(str(pos_all))
                output_file.write('\n\n')
                output_file.write(str(tokenized))


if __name__ == '__main__':
    txt = "안녕 이건 텍스트야! 예시 텍스트인데 나 어떄? 예뻐? 3000만큼 사랑해 ㅎㅎ"
    pos_tuple_all, pos_tuple_cleaned, tokens_cleaned = tokenize(txt, remove_typo=True, content_only=True)
    print(pos_tuple_all)
    print(pos_tuple_cleaned)
    print(tokens_cleaned)
