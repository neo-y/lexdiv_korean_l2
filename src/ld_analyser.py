from src.korean_l2_tokenizer import tokenize
from src.data_reader import read_texts_into_lists
import pandas as pd
from src.ld_calculator import calculate_all_ld

# todo 2: param context_window usw. add (now default setting)

"""
This script makes excel file with all lexical diversity scores for each text
Before running this script!
1. change PATH variable to the directory where texts exist
2. change CONTENT_ONLY variable (boolean) - if true, only take content words, if false, analyse all words
"""

if __name__ == '__main__':
    PATH = '../data'
    CONTENT_ONLY = False
    REMOVE_TYPO = True
    df_index = ['ttr', 'root_ttr', 'log_ttr', 'maas_ttr', 'mattr', 'msttr', 'hdd', 'mtld', 'mtld_ma_bid',
                'mtld_ma_wrap', 'token', 'type', 'raw', 'tokenized']

    # read data
    txt_id, txt_list = read_texts_into_lists(PATH)
    output_df = pd.DataFrame(index=txt_id, columns=df_index)

    # tokenize and calculate the LDs per text
    for index, txt in enumerate(txt_list):
        pos_tuple_all, _, tokenized = tokenize(txt, content_only=CONTENT_ONLY, remove_typo=REMOVE_TYPO)
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
    output_df.to_excel("ld_output.xlsx", encoding='utf-8')  # output saved in data dir
