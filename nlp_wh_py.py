import numpy as np
import nltk
import pandas as pd
from math import *

nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

import torch
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny")
model = AutoModel.from_pretrained("cointegrated/rubert-tiny")
import string

q = ['цена билета']

stop_words = set(stopwords.words('russian'))

from sklearn.metrics.pairwise import cosine_similarity


def cosine_sim(a, b):
    return cosine_similarity(a.reshape(1, -1), b.reshape(1, -1))


def remove_punctuation(text):
    return "".join([ch if ch not in string.punctuation + '«' + '»' + '—' else ' ' for ch in text])


def embed_bert_cls(text, model, tokenizer):  # clean, lemm, embend
    text = remove_punctuation(text)
    t = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**{k: v.to(model.device) for k, v in t.items()})
    embeddings = model_output.last_hidden_state[:, 0, :]
    embeddings = torch.nn.functional.normalize(embeddings)
    return embeddings[0].cpu().numpy()


def get_point(sentense):  # get embend list
    return embed_bert_cls(sentense, model, tokenizer)[0:100]


def get_distance(point_1, point_2):  # get embend distance
    distance = np.sqrt(sum(pow(a - b, 2) for a, b in zip(point_1, point_2)))
    return distance


def get_base_and_embend(path='вопросы.xlsx'):  # get base of q/a
    q_a = pd.read_excel(path, sheet_name='свободные вопросы', header=0, names=None, index_col=None, converters=None,
                        true_values=None, false_values=None,
                        skiprows=None, nrows=None, na_values=None, keep_default_na=True, usecols='B,C')
    q_a = q_a.dropna(subset=['вопросы'])
    q_a = q_a.reset_index(drop=True)
    q_a['embendings'] = q_a['вопросы'].apply(lambda x: get_point(x))
    q_a.fillna(method='ffill', inplace=True)
    return q_a


# нужен здесь, для объявления q_a
q_a = get_base_and_embend()


def get_closest_question(q=q, q_a=q_a):
    minimum = -100
    closest = None
    q_emb = get_point(q)
    for i in range(len(q_a['embendings'])):
        act_dist = cosine_sim(q_a.loc[i]['embendings'], q_emb)
        if act_dist > minimum:
            minimum = act_dist
            closest = q_a.loc[i]
    return closest['ответы']
