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
import nltk.data


def plot_similarity(textlabels, textfeatures, sentencelabels, sentencefeatures, threshold):
    plt.figure()
    corr = np.inner(textfeatures, sentencefeatures)
    x_labels = []
    inds = np.where(abs(corr) >= abs(threshold))[0]
    inds = list(set(inds))
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
    g.set_xticklabels(sentencelabels, rotation=45, ha='right')
    g.set_title("Semantic Textual Similarity")
    plt.tight_layout()
    plt.subplots_adjust(left=0.5, bottom=0.3)
    plt.show()


# TODO: add input paramter split_sen. Should be a boolean that determines whether or not paragraphs are split into
#  sentences
def process_file(file, start_symbol):
    try:
        doc = docx.Document(file)
    except docx.opc.exceptions.PackageNotFoundError:
        raise FileError

    all_paras = doc.paragraphs
    filtered_paras = []
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    # Remove the part of the sentence before the given symbol
    for para in all_paras:
        if start_symbol is not None:
            for i in range(len(para.text)):
                if para.text[i] == start_symbol:
                    filtered_text = para.text[i + 2:]
                    filtered_text = tokenizer.tokenize(filtered_text)
                    filtered_paras += filtered_text
                    break
        else:
            filtered_paras += tokenizer.tokenize(para.text)

    return filtered_paras


class FileError(Exception):
    """Exception raised for errors when attempting to open a word file.
    """
    pass


class Meaningly:
    def __init__(self):
        os.environ['TFHUB_CACHE_DIR'] = '/TensorFlowCache'
        module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
        self.model = hub.load(module_url)
        print("module %s loaded" % module_url)

    def embed(self, input_):
        return self.model(input_)

    # TODO: Join corresponding labels and features together in a tuple so that features can be sorted by correlation and
    #  the labels will be sorted with them.
    def run_and_plot(self, text_, sentences_, threshold_):
        text_embeddings_ = self.embed(text_)
        sentence_embeddings_ = self.embed(sentences_)
        plot_similarity(text_, text_embeddings_, sentences_, sentence_embeddings_, threshold_)

    def process_run_plot(self, file, sentences_to_compare, user_threshold, start_symbol=':'):
        text = process_file(file, start_symbol)
        self.run_and_plot(text, sentences_to_compare, user_threshold)


# For quick testing without the GUI:
"""meaningly = Meaningly()
meaningly.process_run_plot(r'C:/Users/spenc/Documents/Transcript.docx', ["No, you didn't", "I don't know"], 0)"""
