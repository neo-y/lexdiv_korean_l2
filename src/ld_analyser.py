from src.korean_l2_tokenizer import tokenize
from src.data_reader import read_texts_into_lists
import pandas as pd
from src.ld_calculator import calculate_all_ld

# todo 1: include content_only=true
# todo 2: param context_window usw. add (now default setting)


if __name__ == '__main__':
    PATH = '../data'
    ld_index = ['ttr', 'root_ttr', 'log_ttr', 'maas_ttr', 'mattr', 'msttr', 'hdd', 'mtld', 'mtld_ma_bid', 'mtld_ma_wrap']


    # read data
    txt_id, txt_list = read_texts_into_lists(PATH)
    output_df = pd.DataFrame(index=txt_id, columns=ld_index)

    # tokenize and calculate the LDs per text
    for index, txt in enumerate(txt_list):
        pos_tuple, tokenized = tokenize(txt, content_only=False)
        # print to see output (TODO make it as argument)
        print(index)
        print(txt_id[index])
        print(txt)
        print(tokenized)
        print(pos_tuple)
        _, ld_scores = calculate_all_ld(tokenized)  # calculate LDs for this text
        output_df.loc[txt_id[index]] = ld_scores


    # write dataframe to excel
    output_df.to_excel("ld_output.xlsx", encoding='utf-8')  # output saved in data dir