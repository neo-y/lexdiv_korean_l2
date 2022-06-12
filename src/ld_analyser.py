from korean_tokenizer import tokenize, remove_function_words
from data_reader import read_texts_into_lists
import pandas as pd
from taaled import parallel, lexdiv
import logging
from util import current_time_as_str


def tokenize_n_make_ld_matrix(data, tokenizer, include_function_words, parallel_analysis, mx=200):
    """
    Tokenize and calculate all files in the df data and write output as tsv
    (This code includes partial modification of TAALED package source code)
    :param data: df, dataframe with three columns: text id, raw text, processed (typo removed) text, where df index is text file name
    :param tokenizer: str, possible options: (okt, komoran, mecab, kkma, hannanum, stanza)
    :param include_function_words: bool
                                    if set True: tokenize content + function words
                                    if set False: tokenize only content words
    :param parallel_analysis: bool
                        if set True: do parallel analysis
                        if set False: no parallel analysis
    :param mx: int, minimum length of a text for parallel analysis
    :return: none
    """

    # filter out stanza with include_function_words=False
    if tokenizer == 'stanza' and not include_function_words:
        return

    logging.info("Start LD analysis . . .")
    # indexes
    loi = ["ntokens", "ntypes", "mtld", "mtldo", "mattr", "ttr", "rttr", "lttr", "maas", "msttr", "hdd"]

    # set file name
    current_time = current_time_as_str()
    if include_function_words:
        file_name = current_time + "_" + tokenizer + "_all_words.tsv"
        if parallel_analysis:
            file_name = current_time + "_" + tokenizer + "_all_words_prll.tsv"
    else:
        file_name = current_time + "_" + tokenizer + "_content_only.tsv"
        if parallel_analysis:
            file_name = current_time + "_" + tokenizer + "_content_only_prll.tsv"

    outf = open(file_name, "w", encoding='utf-8')
    if parallel_analysis:
        outf.write("filename" + '\t' + "length" + '\t' + '\t'.join(loi))
    else:
        outf.write("filename" + '\t' + '\t'.join(loi))

    text_id = data.index
    text_processed = data['processed']
    skipped = 0
    skippedl = []

    for i, text in enumerate(text_processed):
        _, pos_tuple, tokens_cleaned = tokenize(tokenizer, text)
        if not include_function_words:
            _, tokens_cleaned = remove_function_words(pos_tuple, tokenizer)
        if len(tokens_cleaned) < 1:  # nothing to analysis
            logging.info("%s has no analysable tokens. Skipping", text_id[i])
            skipped += 1
            skippedl.append(text_id[i])
            continue
        if parallel_analysis:
            if len(tokens_cleaned) < mx:  # in case the text is too short for parallel analysis
                skipped += 1
                skippedl.append(text_id[i])
                continue
            ld_lists = parallel(text=tokens_cleaned, clss=True, functd=None, funct=lexdiv, loi=loi, mx=mx).ldvals
            for length in ld_lists:  # iterate through text slices
                outl = [text_id[i], str(length)]  # list of items to write, will add each index below
                for index in loi:  # iterate through index list:
                    outl.append(str(ld_lists[length][index]))  # add index to outr list (in same order as loi list)
                outf.write("\n" + '\t'.join(outl))  # write row to file
        else:  # no parallel analysis
            ldout = lexdiv(tokens_cleaned).vald  # get dictionary version of lexical diversity output
            outl = [text_id[i]]  # list of items to write, will add each index below
            for index in loi:  # iterate through index list:
                outl.append(str(ldout[index]))  # add index to outr list (in same order as loi list)
            outf.write("\n" + '\t'.join(outl))  # write row to file

    outf.flush()
    outf.close()

    logging.info("Analysis on %s files completed successfully", len(text_id) - skipped)
    logging.info("The result is saved as: %s", file_name)

    if skipped:
        logging.info("%s files are skipped due to length problem", skipped)
        logging.info("List of skipped files: ")
        logging.info("%s", skippedl)


def tokenize_n_make_ld_matrix_all_combi(data, tokenizer, mx=200):
    """ #todo docstring
    Tokenize and calculate all files in the df data and write output as tsv
    (This code includes partial modification of TAALED package source code)
    :param data: df, dataframe with three columns: text id, raw text, processed (typo removed) text, where df index is text file name
    :param tokenizer: str, possible options: (okt, komoran, mecab, kkma, hannanum, stanza)
    :param mx: int, minimum length of a text for parallel analysis
    :return: none
    """

    logging.info("Start LD analysis . . .")
    # indexes
    loi = ["ntokens", "ntypes", "mtld", "mtldo", "mattr", "ttr", "rttr", "lttr", "maas", "msttr", "hdd"]

    text_id = data.index
    text_processed = data['processed']

    # tokenize
    pos_tuple_list = []
    tokens_cleaned_list = []
    for i, text in enumerate(text_processed):
        _, pos_tuple, tokens_cleaned = tokenize(tokenizer, text)
        pos_tuple_list.append(pos_tuple)
        tokens_cleaned_list.append(tokens_cleaned)

    f_options = [True, False]
    p_options = [True, False]

    # loop through all combination with tokenized data
    for f in f_options:
        for p in p_options:
            if tokenizer == 'stanza' and not f: # no function word exclude option in stanza
                continue
            # set file name and configuration
            current_time = current_time_as_str()
            if f:
                file_name = current_time + "_" + tokenizer + "_all_words.tsv"
                if p:
                    file_name = current_time + "_" + tokenizer + "_all_words_prll.tsv"
            else:
                file_name = current_time + "_" + tokenizer + "_content_only.tsv"
                if p:
                    file_name = current_time + "_" + tokenizer + "_content_only_prll.tsv"

            outf = open(file_name, "w", encoding='utf-8')
            if p:
                outf.write("filename" + '\t' + "length" + '\t' + '\t'.join(loi))
            else:
                outf.write("filename" + '\t' + '\t'.join(loi))

            if not f: # remove function words
                tokens_cleaned_list = [remove_function_words(pos_tuple, tokenizer)[1] for pos_tuple in pos_tuple_list]

            skipped = 0
            skippedl = []

            config = "Tokenizer: {}, Include Function Words: {}, Parallel Analysis: {}".format(tokenizer, f, p)
            logging.info("\n\n\n================ %s =================", config)

            for i, tokens_cleaned in enumerate(tokens_cleaned_list):

                if len(tokens_cleaned) < 1:  # nothing to analysis
                    logging.info("%s has no analysable tokens. Skipping", text_id[i])
                    skipped += 1
                    skippedl.append(text_id[i])
                    continue
                if p:
                    if len(tokens_cleaned) < mx:  # in case the text is too short for parallel analysis
                        skipped += 1
                        skippedl.append(text_id[i])
                        continue
                    ld_lists = parallel(text=tokens_cleaned, clss=True, functd=None, funct=lexdiv, loi=loi,
                                        mx=mx).ldvals
                    for length in ld_lists:  # iterate through text slices
                        outl = [text_id[i], str(length)]  # list of items to write, will add each index below
                        for index in loi:  # iterate through index list:
                            outl.append(
                                str(ld_lists[length][index]))  # add index to outr list (in same order as loi list)
                        outf.write("\n" + '\t'.join(outl))  # write row to file
                else:  # no parallel analysis
                    ldout = lexdiv(tokens_cleaned).vald  # get dictionary version of lexical diversity output
                    outl = [text_id[i]]  # list of items to write, will add each index below
                    for index in loi:  # iterate through index list:
                        outl.append(str(ldout[index]))  # add index to outr list (in same order as loi list)
                    outf.write("\n" + '\t'.join(outl))  # write row to file

            outf.flush()
            outf.close()

            logging.info("Analysis on %s files completed successfully", len(text_id) - skipped)
            logging.info("The result is saved as: %s", file_name)

            if skipped:
                logging.info("%s files are skipped due to length problem", skipped)
                logging.info("List of skipped files: ")
                logging.info("%s", skippedl)


# if __name__ == '__main__':
#     from data_processor import typodelete
#     txt_id, text_list = read_texts_into_lists("../data/testset-4")
#     typo_deleted_df = typodelete(txt_id, text_list, save=False)
#     # print("\n\n\n\n1")
#     # tokenize_n_make_ld_matrix(data=typo_deleted_df, tokenizer='okt', include_function_words=True, parallel_analysis=True)
#     # print("\n\n\n\n2")
#     # tokenize_n_make_ld_matrix(data=typo_deleted_df, tokenizer='okt', include_function_words=False, parallel_analysis=True)
#     print("\n\n\n\n3")
#     tokenize_n_make_ld_matrix(data=typo_deleted_df, tokenizer='mecab', include_function_words=True, parallel_analysis=True)
#     print("\n\n\n\n4")
#     tokenize_n_make_ld_matrix(data=typo_deleted_df, tokenizer='mecab', include_function_words=True, parallel_analysis=False)
#     # print("\n\n\n\n5")
#     # tokenize_n_make_ld_matrix(data=typo_deleted_df, tokenizer='hannanum', include_function_words=False, parallel_analysis=False)

#
# if __name__ == '__main__':
#     from taaled import ld, params
#     import glob
#     df_column = ['raw', 'typo', 'processed']
#     path = '../data/testset-eng'
#     files = glob.glob(path + "/*.txt")
#     output_df = pd.DataFrame(index=['a','b','c'], columns=df_column)
#     normed_text = []
#     for file in files:
#         normed = open(file, errors="ignore").read().lower().split(" ")
#         normed_text.append(normed)
#
#     # make output df
#     for i, t in enumerate(normed_text):
#         item = []
#         item.append('raw')
#         item.append('typo')
#         item.append(normed_text[i])
#         index = output_df.index[i]
#         output_df.loc[index] = item
#
#     tokenize_n_make_ld_matrix(data=output_df, tokenizer='tmp', include_function_words=True, parallel_analysis=True)
#     tokenize_n_make_ld_matrix(data=output_df, tokenizer='tmp', include_function_words=True, parallel_analysis=False)
#
#     #write this in the firt for loop to run this main
#     # if tokenizer != "tmp":  # todo delete
#     #     _, _, tokens_cleaned = tokenize(tokenizer, text, include_function_words=include_function_words)
#     # if tokenizer == "tmp":  # todo delete
#     #     tokens_cleaned = text  # todo delete


if __name__ == '__main__':
    from taaled import ld
    import glob

    path = '../data/testset-eng'
    files = glob.glob(path + "/*.txt")
    # ld.ldwrite(files, "(nodelete)_prll_tmp_result_from_orig_to_compare.tsv", mx=200, prll=True)
    # ld.ldwrite(files, "(nodelete)noprll_tmp_result_from_orig_to_compare.tsv", mx=200, prll=False)
    ld.ldwrite(files, "tmp.tsv", mx=200, prll=True)
