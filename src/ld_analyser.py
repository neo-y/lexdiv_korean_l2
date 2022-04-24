from src.korean_tokenizer import tokenize
from src.data_reader import read_texts_into_lists
import pandas as pd
from src.ld_calculator import calculate_all_ld

# todo 2: param context_window usw. add (now default setting)

"""
This script makes excel file with all lexical diversity scores for each text
"""


def make_ld_matrix(path='../data', tokenizer='okt'):
    """
    using a tokenizer (argument), tokenize and calculate all files in the path (argument), write output as excel
    :param path: str, path where texts exist
    :param tokenizer: str, possible options: (okt, komoran, mecab, kkma, hannanum)
    :return:
    """
    # CONTENT_ONLY = False
    # REMOVE_TYPO = True
    df_index = ['ttr', 'root_ttr', 'log_ttr', 'maas_ttr', 'mattr', 'msttr', 'hdd', 'mtld', 'mtld_ma_bid',
                'mtld_ma_wrap', 'token', 'type', 'raw', 'tokenized']

    # read data
    txt_id, txt_list = read_texts_into_lists(path)
    output_df = pd.DataFrame(index=txt_id, columns=df_index)

    # tokenize and calculate the LDs per text
    for index, txt in enumerate(txt_list):
        pos_tuple_all, _, tokenized = tokenize(tokenizer=tokenizer, data=txt)
        # print to see output (TODO make it as argument)
        print(index)
        print(txt_id[index])
        print(txt)
        print(tokenized)
        print(pos_tuple_all)
        _, ld_scores = calculate_all_ld(tokenized)  # calculate LDs for this text
        # add additional columns (token, type, raw, tokenized)
        ld_scores.append(len(tokenized))  # token
        ld_scores.append(len(set(tokenized)))  # type
        ld_scores.append(txt)  # raw text
        ld_scores.append(tokenized)  # tokenized
        output_df.loc[txt_id[index]] = ld_scores

    # write dataframe to excel
    output_path = PATH + '/' + tokenizer + "_" + "ld_output.xlsx"
    output_df.to_excel(output_path, encoding='utf-8')  # output saved in data dir


if __name__ == '__main__':
    PATH = '/Users/hakyungsung/Documents/GitHub/lexdiv_korean_l2/NIKL'
    # make_ld_matrix(path=PATH, tokenizer='okt')
    # make_ld_matrix(path=PATH, tokenizer='komoran')
    # make_ld_matrix(path=PATH, tokenizer='mecab')
    # make_ld_matrix(path=PATH, tokenizer='kkma')
    make_ld_matrix(path=PATH, tokenizer='hannanum')