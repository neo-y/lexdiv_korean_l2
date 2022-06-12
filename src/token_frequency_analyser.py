"""
This script generates token frequency list of all text files in a path based on a tokenizer or space split.
"""
from src.util import flatten_list
from src.korean_tokenizer import tokenize
from src.util import current_time_as_str
from src.data_reader import read_texts_into_lists
import pandas as pd
from collections import Counter
import re
import string


def analyse_frequency_tokenized(path, tokenizer, save=True):
    """
    Generates token frequency list with POS using a tokenizer.
    Input is a list of .txt files, which will be tokenized using a tokenizer of a choice.
    :param path: str, a path to a list of .txt files
    :param tokenizer: str, tokenizer of a choice: possible options: (okt, kkma, hannanum, mecab, stanza, komoran)
    :param save: boolean, if True, save the result
    :return: dataframe, token frequency table
    """
    vocab_df = pd.DataFrame(columns=['token', 'pos', 'frequency'])

    # read data
    _, txt_list = read_texts_into_lists(path)

    # flatten list of tokenized texts
    raw_flatten = flatten_list(txt_list)

    # tokenize
    _, pos_tuple_clean, _ = tokenize(tokenizer=tokenizer, text=raw_flatten) # function word not removed

    # calculate frequency
    pos_with_frequency = Counter(pos_tuple_clean)
    pos_with_frequency = pos_with_frequency.most_common()  # sort by frequency

    # put in df
    vocab_df['token'] = [item[0][0] for item in pos_with_frequency]
    vocab_df['pos'] = [item[0][1] for item in pos_with_frequency]
    vocab_df['frequency'] = [item[1] for item in pos_with_frequency]

    if save:
        current_time = current_time_as_str()
        output_path = tokenizer + "_frequency_" + current_time + ".tsv"
        vocab_df.to_csv(output_path, encoding='utf-8', sep='\t')

    return vocab_df


def analyse_frequency_space_split(path, save=True):
    """
    Generates token frequency list.
    Token in this function is defined as "space split" word
    Input is a list of .txt files, which will be tokenized using a tokenizer of a choice.
    :param path: str, a path to a list of .txt files
    :param save: boolean, if True, save the result as excel file
    :return: dataframe, token frequency table
    """

    vocab_df = pd.DataFrame(columns=['token', 'frequency'])
    _, text_list = read_texts_into_lists(path)
    text_all = flatten_list(text_list)

    # delete basic punctuation #TODO examine more about punctuation
    punc = string.punctuation
    pattern = r"[{}]".format(punc)
    text_all = re.sub(pattern, '', text_all)
    text_all = text_all.strip()

    # split into words
    token_list = text_all.split(' ')

    # calculate frequency
    word_with_frequency = Counter(token_list)
    word_with_frequency = word_with_frequency.most_common()  # sort by frequency

    vocab_df['token'] = [item[0] for item in word_with_frequency]
    vocab_df['frequency'] = [item[1] for item in word_with_frequency]

    if save:
        current_time = current_time_as_str()
        output_path = "space_split_frequency_" + current_time + ".xlsx"
        vocab_df.to_excel(output_path, encoding='utf-8')

    return vocab_df


if __name__ == '__main__':
    """
    Example usage below
    """
    PATH = '../data/4208-data-total'
    tokenizer_list = ['okt', 'kkma','hannanum','komoran', 'stanza']

    for tokenizer in tokenizer_list:
        _ = analyse_frequency_tokenized(PATH, tokenizer, save=True)
        print("saved result of ", tokenizer)