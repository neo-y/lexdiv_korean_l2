from data_processor import typodelete
from data_reader import read_texts_into_lists
import argparse
import logging
from ld_analyser import tokenize_n_make_ld_matrix
import warnings
import numpy as np

from util import current_time_as_str

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    log_file = current_time_as_str() + "_logfile.log"
    logging.basicConfig(filename=log_file, filemode='w', level=logging.INFO)

    parser = argparse.ArgumentParser()  # todo make argument optional and set default param (most impt, best performing)
    parser.add_argument("-i", "--inputdir", required=True,
                        help="Path to the directory which includes plain text files to be analysed")
    parser.add_argument("-t", "--tokenizer", nargs='+', required=True,
                        help="Tokenizers: (okt, komoran, mecab, kkma, hannanum, stanza). You can give multiple tokenizers ex) -t kkma komoran")
    parser.add_argument("-a", "--all", action="store_true",
                        help="Do analysis on all possible combinations on the given tokenizer sets (function word T&F x parallel T&F)")
    parser.add_argument("-f", "--functionwords", action='store_true',
                        help="Do analysis on both function and content words. If this argument not given, do analysis only on content words.")
    parser.add_argument("-p", "--parallel", action='store_true', help="do parallel analysis.")
    args = parser.parse_args()

    # configuration information
    logging.info("-----------Configuration----------")
    logging.info("Selected Tokenizer = %s", args.tokenizer)
    if args.all:
        logging.info("Four different analysis will be done.")
        logging.info("(functionword True, False) x (Prallel analysis True, False)")
    else:
        logging.info("Include Function Words = %s", args.functionwords)
        logging.info("Parallel Analysis = %s", args.parallel)
    logging.info("----------------------------------")

    # read and process text
    txt_id, text_list = read_texts_into_lists(args.inputdir)
    typo_deleted_df = typodelete(txt_id, text_list)

    # tokenize and analyse
    if args.all:
        f_options = [True, False]
        p_options = [True, False]
        for tokenizer in args.tokenizer:
            for f in f_options:
                for p in p_options:
                    config = "Tokenizer: {}, Include Function Words: {}, Parallel Analysis: {}".format(tokenizer, f, p)
                    logging.info("\n\n\n================ %s =================", config)
                    tokenize_n_make_ld_matrix(data=typo_deleted_df, tokenizer=tokenizer,
                                              include_function_words=f,
                                              parallel_analysis=p)


    else:
        for tokenizer in args.tokenizer:
            logging.info("\n\n\n================ tokenizer %s =================", tokenizer)
            tokenize_n_make_ld_matrix(data=typo_deleted_df, tokenizer=tokenizer,
                                      include_function_words=args.functionwords, parallel_analysis=args.parallel)

    logging.info("FINISHED")

    # todo enable log to stdoutput and file