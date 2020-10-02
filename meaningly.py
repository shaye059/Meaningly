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

# TODO: Restructure this so that the model is initialized once on the first run and then embed is simply called for
#  any further comparisons. Right now the model is set up every time it is run.


def initialize_model(text, sentences, thresh):
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    model = hub.load(module_url)
    print("module %s loaded" % module_url)

    def embed(input_):
        return model(input_)

    # TODO: Join corresponding labels and features together in a tuple so that features can be sorted by correlation and
    #  the labels will be sorted with them.
    def plot_similarity(textlabels, textfeatures, sentencelabels, sentencefeatures, threshold, rotation):
        plt.figure()
        corr = np.inner(textfeatures,sentencefeatures)
        #print(corr)
        x_labels = []
        inds = np.where(abs(corr) >= abs(threshold))[0]
        inds = list(set(inds))
        #print(inds)
        for x in sorted(inds, reverse=True):
            x_labels.append(textlabels.pop(x))
        x_labels.reverse()
        arr = corr[np.any(abs(corr) >= abs(threshold), axis=1)]
        sns.set(font_scale=0.8)
        g = sns.heatmap(
            arr,
            xticklabels=sentencelabels,
            yticklabels=x_labels,
            vmin=0,
            vmax=1,
            cmap="YlOrRd",
            square=True)
        g.set_xticklabels(sentencelabels, rotation=rotation)
        g.set_title("Semantic Textual Similarity")
        plt.tight_layout()
        plt.subplots_adjust(left=0.5)
        plt.show()

    def run_and_plot(text_, sentences_, threshold_):
        text_embeddings_ = embed(text_)
        sentence_embeddings_ = embed(sentences_)
        plot_similarity(text_, text_embeddings_, sentences_,sentence_embeddings_,threshold_, 0)

    run_and_plot(text, sentences, thresh)



class FileError(Exception):
    """Exception raised for errors when attempting to open a word file.
    """
    pass


# TODO: split sentence at every ellipses, period, exclamation mark, and question mark
def process_file(file, sentences_to_compare, user_threshold, start_symbol=None):
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

    initialize_model(list_of_text, sentences_to_compare, user_threshold)

# For quick testing without the GUI:
#initialize_model(['Hello, how are you?', "I'm not sure how that works.", "Hi, how's it going?"], ["Hey, what's up?","I don't know"], 0)