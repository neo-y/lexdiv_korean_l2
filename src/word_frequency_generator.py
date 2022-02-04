"""
This script generates word (space split) list with frequency from all text files in a given directory
and write output to excel
"""
from src.data_reader import read_texts_into_lists
from src.vocab_list_generator import flatten_list
import pandas as pd
from collections import Counter
import re
import string

if __name__ == '__main__':
    PATH = "../data"

    word_df = pd.DataFrame(columns=['word', 'frequency'])
    _, text_list = read_texts_into_lists(PATH)
    text_all = flatten_list(text_list)

    # delete basic punctuation
    punc = string.punctuation
    pattern = r"[{}]".format(punc)
    text_all = re.sub(pattern, '', text_all)
    text_all = text_all.strip()

    # split into words
    token_list = text_all.split(' ')

    # calculate frequency
    word_with_frequency = Counter(token_list)
    word_with_frequency = word_with_frequency.most_common()  # sort by frequency

    word_df['word'] = [item[0] for item in word_with_frequency]
    word_df['frequency'] = [item[1] for item in word_with_frequency]

    output_path = PATH + '/word_frequency_list.xlsx'
    word_df.to_excel(output_path, encoding='utf-8')
