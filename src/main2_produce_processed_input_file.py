from data_processor import typodelete
from data_reader import read_texts_into_lists
import argparse
import logging
import warnings
import numpy as np


warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)
logging.basicConfig(level=logging.INFO)
logging.getLogger("tensorflow").setLevel(logging.CRITICAL)
logging.getLogger("stanza").setLevel(logging.WARNING)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputdir", required=True,
                        help="Path to the directory which includes plain text files to be analysed")
    args = parser.parse_args()


    # read and process text
    txt_id, text_list = read_texts_into_lists(args.inputdir)
    typodelete(txt_id, text_list)


    logging.info("FINISHED")
