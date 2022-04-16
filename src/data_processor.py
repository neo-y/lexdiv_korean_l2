import win32com.client
import os
import codecs
import re
import pandas as pd

from src.data_reader import read_texts_into_lists
from src.util import current_time_as_str


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


def typodelete(txt_id, txt_list, save=True):
    """
    Detect typo in a list of texts using MSword and delete the typos
    :param txt_id: unique id of texts
    :param txt_list: list of texts
    :param save: boolean, if True, save the result file to excel
    :return: dataframe with raw text, typos, and typo deleted text
    """

    # make df to store results
    df_column = ['raw', 'typo', 'processed']
    output_df = pd.DataFrame(index=txt_id, columns=df_column)

    # save the raw text into ms word form to use ms word typo corrector
    current_time = current_time_as_str()
    file_path = os.path.abspath(current_time + ".txt")
    with codecs.open(file_path, 'w', encoding='utf-8') as f:
        index = 0
        for text in txt_list:
            index += 1
            f.write(text)
            if len(txt_list) > index:  # do not add \n at the end of the file
                f.write('\n')

    # open the ms word document
    msword = win32com.client.DispatchEx('Word.Application')
    doc = msword.Documents.Open(file_path)
    assert int(doc.Paragraphs.Count) == len(txt_list)

    # for each text(Paragraph in word), detect error
    for i, p in enumerate(doc.Paragraphs):  # process per text
        typos = p.Range.SpellingErrors
        item = []
        typo_list = []

        for typo in typos:  # make typo list
            typo_list.append(str(typo))

        # delete typos in text
        pattern = re.compile(r'\b(?:%s)\b' % '|'.join(typo_list))
        processed = re.sub(pattern, '', txt_list[i])

        item.append(txt_list[i])
        item.append(typo_list)
        item.append(processed)
        output_df.loc[txt_id[i]] = item

    # close and delete temporary files
    doc.Close(0)
    msword.Quit(0)
    os.remove(file_path)

    if save:
        file_path = file_path + ".xlsx"
        output_df.to_excel(file_path, encoding='utf-8')

    return output_df


if __name__ == '__main__':
    path = "../data"
    # read data
    txt_id, txt_list = read_texts_into_lists(path)
    output_df = typodelete(txt_id, txt_list, save=True)
