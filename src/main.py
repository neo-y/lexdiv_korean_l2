# todo change to parsearg, add log info
from src.data_processor import typodelete
from src.data_reader import read_texts_into_lists

if __name__ == '__main__':
    path = "../data"
    txt_id, text_list = read_texts_into_lists(path)
    typo_deleted_df = typodelete(txt_id, text_list)
    # todo next: korean_tokenizer.py
    # todo next: ld_analyser.py