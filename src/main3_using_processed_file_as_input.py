from data_processor import typodelete
from data_reader import read_texts_into_lists
import argparse
import logging
from ld_analyser import tokenize_n_make_ld_matrix, tokenize_n_make_ld_matrix_all_combi
import warnings
import numpy as np
import sys
import pandas as pd

from util import current_time_as_str

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)
logging.basicConfig(level=logging.INFO)
logging.getLogger("tensorflow").setLevel(logging.CRITICAL)
logging.getLogger("stanza").setLevel(logging.WARNING)

if __name__ == '__main__':
    a_logger = logging.getLogger()
    a_logger.setLevel(logging.DEBUG)
    log_file = current_time_as_str() + "_logfile.log"
    output_file_handler = logging.FileHandler(log_file)
    stdout_handler = logging.StreamHandler(sys.stdout)

    a_logger.addHandler(output_file_handler)
    a_logger.addHandler(stdout_handler)


    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputfile", required=True,
                        help="input file consisting of typo corrected processed text data in each row")
    parser.add_argument("-t", "--tokenizer", nargs='+', required=True,
                        help="Tokenizers: (okt, komoran, mecab, kkma, hannanum, stanza). You can give multiple tokenizers ex) -t kkma komoran")
    parser.add_argument("-a", "--all", action="store_true",
                        help="""Do analysis on all possible combinations on the given tokenizer sets (function word T&F x parallel T&F)
                             Note that functionwords=false is not provided in stanza.
                             Argument --functionwords and --parallel are ignored if given. """)
    parser.add_argument("-f", "--functionwords", action='store_true',
                        help="""Do analysis on both function and content words. If this argument not given, do analysis only on content words.
                                Note that functionwords=false in not provided in stanza. """)
    parser.add_argument("-p", "--parallel", action='store_true', help="do parallel analysis.")
    args = parser.parse_args()


    if "stanza" in args.tokenizer and not args.functionwords: # if the user wants to exclude functionwords in stanza
        if not args.all:
            raise ValueError("Stanza does not provide functionwords=False. Please give functionwords argument for stanza tokenizer. ")

    # configuration information
    logging.info("-----------Configuration----------")
    logging.info("Selected Tokenizer = %s", args.tokenizer)
    if args.all:
        logging.info("Four different analysis will be done.")
        logging.info("(functionword True, False) x (Parallel analysis True, False)")
    else:
        logging.info("Include Function Words = %s", args.functionwords)
        logging.info("Parallel Analysis = %s", args.parallel)
    logging.info("----------------------------------")

    # read input file as df
    typo_deleted_df = pd.read_csv(args.inputfile, sep='\t', index_col=0)

    # tokenize and analyse
    if args.all:
        for tokenizer in args.tokenizer:
            tokenize_n_make_ld_matrix_all_combi(data=typo_deleted_df, tokenizer=tokenizer)


    else:
        for tokenizer in args.tokenizer:
            logging.info("\n\n\n================ tokenizer %s =================", tokenizer)
            tokenize_n_make_ld_matrix(data=typo_deleted_df, tokenizer=tokenizer,
                                      include_function_words=args.functionwords, parallel_analysis=args.parallel)

    logging.info("FINISHED")
