from absl import logging
import tensorflow as tfy
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
import docx


def initialize_model(text, sentences):
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    model = hub.load(module_url)
    print("module %s loaded" % module_url)

    def embed(input_):
        print(input_)
        return model(input_)

    def plot_similarity(textlabels, textfeatures, sentencelabels, sentencefeatures, rotation):
        corr = np.inner(textfeatures,sentencefeatures)
        print(corr)
        corr.view('i8,i8,i8').sort(order=['f1'], axis=0)
        print(corr)
        sns.set(font_scale=0.8)
        g = sns.heatmap(
            corr,
            xticklabels=sentencelabels,
            yticklabels=textlabels,
            vmin=0,
            vmax=1,
            cmap="YlOrRd",
            square=True)
        g.set_xticklabels(sentencelabels, rotation=rotation)
        g.set_title("Semantic Textual Similarity")
        plt.tight_layout()
        plt.subplots_adjust(left=0.6)
        plt.show()

    def run_and_plot(text_, sentences_):
        text_embeddings_ = embed(text_)
        sentence_embeddings_ = embed(sentences_)
        plot_similarity(text_, text_embeddings_, sentences_,sentence_embeddings_, 0)

    run_and_plot(text, sentences)



class FileError(Exception):
    """Exception raised for errors when attempting to open a word file.
    """
    pass


# TODO: split sentence at every ellipses, period, exclamation mark, and question mark
def process_file(file, sentences_to_compare, start_symbol=None):
    try:
        doc = docx.Document(file)
    except docx.opc.exceptions.PackageNotFoundError:
        raise FileError

    all_paras = doc.paragraphs
    filtered_paras = []

    # Remove the part of the sentence before the given symbol
    for para in all_paras:
        if start_symbol is not None:
            for i in range(len(para.text)):
                if para.text[i] == start_symbol:
                    para.text = para.text[i+2:]
                    filtered_paras.append(para)
                    break

    list_of_text = []
    for parax in filtered_paras:
        list_of_text.append(parax.text)
        print(parax.text)

    initialize_model(list_of_text, sentences_to_compare)


initialize_model(['Hello, how are you?', "I'm not sure how that works.", "Hi, how's it going?"], ["Hey, what's up?"])