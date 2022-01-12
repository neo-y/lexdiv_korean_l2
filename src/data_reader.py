import os
import pandas as pd

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        txt = f.read()
        txt = txt.replace("\n", " ")
    return txt



def read_vocabulary(vocab_path, print_result=True):
    """
    read excel vocabulary and exclude typos
    :param file_path:
    :return:
    """
    df = pd.read_excel(vocab_path)
    df_clean = df[df['Error'] != 'o']

    if print_result:
        print('[')
        for index, row in df_clean.iterrows():
            print("(" + "'" + row['vocab'] + "'" + "," + "'" + row['pos'] + "'" + ")", ",")
        print(']')

    return df_clean


def read_texts_into_lists(path):
    """
    TODO mark source https://www.geeksforgeeks.org/how-to-read-multiple-text-files-from-folder-in-python/
    :param path:
    :return:
    """
    os.chdir(path)
    text_list = list()
    txt_id = list()
    for file in os.listdir():
        # Check whether file is in text format or not
        if file.endswith(".txt"):
            file_path = f"{path}/{file}"
            txt_id.append(file)
            # call read text file function
            txt = read_text_file(file)
            text_list.append(txt)

    return txt_id, text_list


if __name__ == '__main__':
    read_vocabulary("../data/vocab/vocab_list(processed).xlsx")