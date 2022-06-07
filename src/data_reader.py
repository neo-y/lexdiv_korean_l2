import os
import pandas as pd
import logging
import string
from string import digits


def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        txt = f.read()
        txt = txt.replace("\n", " ")
    return txt


# def read_vocabulary(vocab_path, print_result=True):
#     """
#     read excel vocabulary and exclude typos
#     :param file_path:
#     :return:
#     """
#     df = pd.read_excel(vocab_path)
#     df_clean = df[df['Error'] != 'o']
#
#     if print_result:
#         print('[')
#         for index, row in df_clean.iterrows():
#             print("(" + "'" + row['vocab'] + "'" + "," + "'" + row['pos'] + "'" + ")", ",")
#         print(']')
#
#     return df_clean


def read_texts_into_lists(path, remove_punc_num=True):
    """
    read all plain text files (.txt) in the path and return text id (file name) and text contents as list
    :param remove_punc_num: bool, if set True, remove punctuation including special character and number in the text.
    :param path: str, directory to the input files
    :return: tuple (txt_id, text_list)
                where (txt_id) is a list of file names
                      (text_list) is a list of file contents as string
    """
    owd = os.getcwd()
    os.chdir(path)
    text_list = list()
    txt_id = list()
    for file in os.listdir():
        if file.endswith(".txt"):
            txt = read_text_file(file)
            if len(txt) < 1:
                logging.info("%s is empty file. Skipped", file)
                continue
            txt_id.append(file)
            txt = read_text_file(file)
            text_list.append(txt)

    os.chdir(owd)

    if remove_punc_num:
        #text_list = [txt.translate(str.maketrans('', '', string.punctuation)) for txt in text_list] # remove punctuation
        text_list = [txt.translate(str.maketrans('', '', digits)) for txt in text_list] # remove number

    logging.info("%s files read successfully.", len(txt_id))

    return txt_id, text_list


if __name__ == '__main__':
    _, text_list1 = read_texts_into_lists("../data/testset-4", remove_punc_num=True)
    _, text_list2 = read_texts_into_lists("../data/testset-4", remove_punc_num=False)

    print(text_list1)
    print(text_list2)