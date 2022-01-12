"""
This script generate vocabulary list with its frequency based on the set of tokenized texts
"""
from src.data_reader import read_texts_into_lists
import pandas as pd
from src.korean_l2_tokenizer import tokenize, STOPWORDS_POS
from collections import Counter


def flatten_list(txts):
    """
    input: list of texts
    output: flattend string (list concatenated)
    :param txts:
    :return:
    """
    flatten = str()
    for txt in txts:
        flatten = flatten + txt
    return flatten


if __name__ == '__main__':
    PATH = '../data'
    vocab_df = pd.DataFrame(columns=['vocab', 'pos', 'frequency'])

    # read data
    txt_id, txt_list = read_texts_into_lists(PATH)

    # flatten list of tokenized texts
    raw_flatten = flatten_list(txt_list)

    # tokenize
    pos_tuple_all, _, _ = tokenize(raw_flatten, content_only=False, remove_typo=False)

    # clean pos_tuple (exclude stopwords from pos_tuple)
    pos_tuple_clean = [pos for pos in pos_tuple_all if pos[
        1] not in STOPWORDS_POS]  # TODO this is not necessary as func tokenize changed. (you can use second output from tokenize)

    # calculate frequency
    pos_with_frequency = Counter(pos_tuple_clean)
    pos_with_frequency = pos_with_frequency.most_common()  # sort by frequency

    # put in df
    vocab_df['vocab'] = [item[0][0] for item in pos_with_frequency]
    vocab_df['pos'] = [item[0][1] for item in pos_with_frequency]
    vocab_df['frequency'] = [item[1] for item in pos_with_frequency]

    # to excel
    vocab_df.to_excel("vocab_list.xlsx", encoding='utf-8')
