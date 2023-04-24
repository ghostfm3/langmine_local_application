from wordcloud import WordCloud
from janome.tokenizer import Tokenizer
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import matplotlib.pyplot as plt
import pandas as pd
import japanize_matplotlib
import torch
import matplotlib as plt
import sys
import matplotlib.pyplot as plt
import japanize_matplotlib
import ginza
import spacy
import json
import plotly.express as px
import plotly.io as pio
import seaborn as sns
import numpy as np

label_list = ['安らぎ', '楽しさ', '親しみ', '尊敬・尊さ', '感謝', '気持ちが良い', '誇らしい', '感動', '喜び', 
                  '悲しさ', '寂しさ', '不満', '切なさ', '苦しさ', '不安', '憂鬱', '辛さ', '好き', '嫌悪', '恥ずかしい', 
                  '焦り', '驚き', '怒り', '幸福感', '恨み', '恐れ', '恐怖', '悔しさ', '祝う気持ち', '困惑', 'きまずさ', 
                  '興奮', '悩み', '願望', '失望', 'あわれみ', '見下し', '謝罪', 'ためらい', '不快', '怠さ', 'あきれ', '心配', 
                  '緊張', '妬み', '憎い', '残念', '情けない', '穏やか']

def janome_token(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()  # ファイルからテキストを読み込み
    t = Tokenizer()
    result = []
    for token in t.tokenize(text):
        pos = token.part_of_speech.split(',')[0]
        if pos == "名詞":
            result.append(token.surface)
    return result

def remove_stop_word(word_list, stop_word):
    return [word for word in word_list if word not in stop_word]

def wordcloud_result(color,path_1,width,height,text):
    wordcloud = WordCloud(background_color=color, font_path=path_1, width=width, height=height).generate(text)    
    wordcloud.to_file("./output/wordcloud/result1.png")

def plt_counter(count):
    for word, num in count.most_common(5):
        plt.bar(word, num)
    
    plt.grid(axis='y')
    plt.xlabel('単語')
    plt.ylabel('頻度')
    plt.savefig('./output/freq/count_result.png')

def sentiment_analysis(words):
    result_dict = {}
    save_directory = "./model/20230420_more_sentiment_word_model"
    tokenizer = AutoTokenizer.from_pretrained(save_directory)
    model = AutoModelForSequenceClassification.from_pretrained(save_directory)
    sentiment_analyzer = pipeline("sentiment-analysis", model=model.to("cpu"), tokenizer=tokenizer)
    
    label_count = [0] * len(label_list)

    for token in words:
        result = sentiment_analyzer(token)
        result_dict[token] = result[0]['label']
        for i, label in enumerate(label_list):
            if result[0]['label'] == label:
                label_count[i] += 1
    
    return label_count,  result_dict

def draw_graph(count):
    labels = list(count.keys())
    sizes = list(count.values())

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.pie(sizes, labels=labels, startangle=90, radius=1.12, autopct='%1.1f%%', pctdistance=0.75,
           wedgeprops=dict(width=0.7, edgecolor='w'), textprops=dict(color='w', fontsize=14))
    ax.set_title('Emotional rate', fontsize=20, pad=50)
    ax.legend(labels, loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=14)

    # 中心に円を描画してドーナツ型にする
    centre_circle = plt.Circle((0, 0), 0.001, fc='white')
    ax.add_artist(centre_circle)

    plt.savefig('./output/emotion/result.png')