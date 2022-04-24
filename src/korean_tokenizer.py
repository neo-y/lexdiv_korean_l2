"""
Do not change argument value content_only in func remove_stop_words.
Do not change argument value remove_typo, content_only in func tokenize.
"""
import os
import random
from konlpy.tag import Okt, Komoran, Mecab, Kkma, Hannanum
from vocabulary.vocab_clean import clean_vocab

OKT_STOPWORDS = ['URL', 'Email', 'ScreenName', 'Hashtag', 'KoreanParticle', 'Punctuation', 'Foreign', 'Alpha', 'Number',
                 'Unknown', 'PreEomi', 'Eomi']

KOMORAN_STOPWORDS = ['EP', 'EF', 'EC', 'ETN', 'ETM', 'SF', 'SE', 'SS', 'SP', 'SO', 'SW', 'SH', 'SL', 'SN', 'NF', 'NV',
                     'NA']
MECAB_STOPWORDS = ['EP', 'EF', 'EC', 'ETN', 'ETM', 'SF', 'SE', 'SSO', 'SSC', 'SC', 'SY', 'SH', 'SL', 'SN']
KKMA_STOPWORDS = ['EPH', 'EPT', 'EPP', 'EFN', 'EFQ', 'EFO', 'EFA', 'EFI', 'EFR', 'ECE', 'ECS', 'ECD', 'ETN', 'ETD',
                  'SF', 'SE', 'SS', 'SP', 'SO', 'SW', 'OH', 'OL', 'ON', 'UN']

HANNANUM_STOPWORDS = ['E','S','F']

CONTENT_POS = ['Noun', 'Verb', 'Adjective', 'Adverb']

# CLEAN_VOCAB = clean_vocab

def remove_stop_words(token_pos_tuple, tokenizer, content_only=False):
    """
    :param tokenizer: str, possible options: (okt, komoran, mecab, kkma, hannanum)
    :param content_only: boolean, if True, only content words (verb, noun, adjective, adverb) are included in the output.
    :param token_pos_tuple: list of tuple consisting of token and POS [('열심히', 'Adverb'), ('코딩', 'Noun')...]
    :return: list of tokens without stopwords
    """
    pos_tuple_cleaned = []

    if tokenizer == 'okt':
        stopwords = OKT_STOPWORDS
    elif tokenizer == 'komoran':
        stopwords = KOMORAN_STOPWORDS
    elif tokenizer == 'mecab':
        stopwords = MECAB_STOPWORDS
    elif tokenizer == 'kkma':
        stopwords = KKMA_STOPWORDS
    elif tokenizer == 'hannanum':
        stopwords = HANNANUM_STOPWORDS
    else:
        raise ValueError("tokenizer must be one of these options: (okt, komoran, mecab, kkma, hannanum)")

    if content_only:  # include only content words:
        for index, pair in enumerate(token_pos_tuple):
            if pair[1] in CONTENT_POS:  # tuple[1] = POS
                pos_tuple_cleaned.append(pair)

    else:  # include all words (function words + content words)
        for index, pair in enumerate(token_pos_tuple):
            if pair[1] not in stopwords:
                pos_tuple_cleaned.append(pair)

    return pos_tuple_cleaned


def tokenize(tokenizer, data, content_only=False, remove_typo=False):
    """
    tokenize sequences using konlpy tokenizer.
    :param tokenizer: str, possible options: (okt, komoran, mecab, kkma, hannanum)
    :param remove_typo: boolean if True, remove typo tokens using dictionary
    :param data: str, raw text
    :param content_only: boolean, if True, only content words (verb, noun, adjective, adverb) are included in the output.
    :return:
    """
    if tokenizer == 'okt':
        tagger = Okt()
    elif tokenizer == 'komoran':
        tagger = Komoran()
    elif tokenizer == 'mecab':
        tagger = Mecab()  # todo Mecab not available in Windows. Do error handling.
    elif tokenizer == 'kkma':
        tagger = Kkma()
    elif tokenizer == 'hannanum':
        tagger = Hannanum()
    else:
        raise ValueError("tokenizer must be one of these options: (okt, komoran, mecab, kkma, hannanum)")

    # tokenize
    if tokenizer == 'okt':
        pos_tuple_all = tagger.pos(data, stem=True)
    else:
        pos_tuple_all = tagger.pos(data)

    # remove stopwords
    pos_tuple_cleaned = remove_stop_words(pos_tuple_all, tokenizer=tokenizer, content_only=False)

    # remove typos
    # if remove_typo:
    #     pos_tuple_cleaned = [item for item in pos_tuple_cleaned if item in CLEAN_VOCAB]

    # separate lists for tokens
    tokens_cleaned = [item[0] for item in pos_tuple_cleaned]

    return pos_tuple_all, pos_tuple_cleaned, tokens_cleaned


# def write_tokenized_output(number_of_files=5):
#     """
#     TODO move this function to separate script
#     :param number_of_files:
#     :return:
#     """
#     random.seed(1)
#
#     while number_of_files > 0:
#         number_of_files -= 1
#         file = random.choice(os.listdir("../data/selected"))
#         file_dir = "../data/selected/" + file
#         with open(file_dir, encoding='utf-8') as f:
#             lines = f.read()
#             pos_all, _, tokenized = tokenize(lines)
#             output_dir = "../data/output/" + file[:-4] + "_Output.txt"
#             with open(output_dir, "w", encoding='utf-8') as output_file:
#                 output_file.write(lines)
#                 output_file.write('\n\n')
#                 output_file.write(str(pos_all))
#                 output_file.write('\n\n')
#                 output_file.write(str(tokenized))


if __name__ == '__main__':
    txt = "안녕 이건 텍스트야! 예시 텍스트인데 나 어떄? 예뻐? 3000만큼 사랑해 ㅎㅎ"
    pos_tuple_all, pos_tuple_cleaned, tokens_cleaned = tokenize(tokenizer='okt', data=txt, remove_typo=True,
                                                                content_only=False)
    print(pos_tuple_all)
    print(pos_tuple_cleaned)
    print(tokens_cleaned)
