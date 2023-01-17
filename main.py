import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import streamlit as st
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import numpy as np
import PIL.Image
import random

df = pd.read_csv('Family_guy_dialog.csv')

words = {}
garbage = ['!', ',', '.', '"', "'"]

def count_words(sentance):
    sentance = sentance.replace(u'\xa0', u' ')
    lst = sentance.strip().lower().split(' ')

    for i in range(len(lst)):
        for x in lst[i]:
            if len(lst[i]) > 3:
                if x in garbage:
                    for y in garbage:
                        lst[i] = lst[i].replace(y, "")
        if len(lst[i]) > 3:
            words.setdefault(lst[i], 0)
            words[lst[i]] += 1
    
    return lst

for i in df.dialog: count_words(i)

sort = dict(sorted(words.items(), key=lambda x: x[1], reverse=True)[:10])

top5words = list(sort.keys())
top5count = list(sort.values())

df2 = pd.DataFrame(
    {'word': top5words,
    'count': top5count}
)

st.subheader("Top 10 Family Guy Words of Dialog")
st.bar_chart(df2, x="word", y="count")

def create_cloud(mask, text, color_set, stopwords = []):
    sw = set(STOPWORDS)
    for word in stopwords: sw.add(word)

    return WordCloud(
        stopwords=sw,
        # max_words=1000,
        mask=mask,
        background_color='#0E1117',
        color_func=lambda *args, **kwargs: random.choice(color_set), # list of tuples (3)
        min_font_size=8,
        width=800,
        height=800,
    ).generate(text)

# Texts
def dialog(person):
    cdf = df.loc[df.character == person]
    return ''.join(cdf.dialog)

# Colors
colors = {
    'stewie': [(255, 59, 59), (71, 195, 252), (255, 229, 145)],
    'peter': [(39, 64, 37), (255, 255, 255), (92, 70, 60)],
    'quagmire': [(249, 255, 82), (255, 36, 36), (41, 41, 94)],
    'brian': [(255, 255, 255), (237, 178, 0), (255, 37, 8)],
}

# Creation
def draw_cloud(character):
    return create_cloud(
                        eval(f"np.array(PIL.Image.open(\'./assets/{character.lower()}head.png\'))"),
                        dialog(character.title()), 
                        colors[character.lower()], 
                        ['s', 'oh', 'well', 'hey', 'uh', 'yeah', 'im', 'know', 'gonna', 'wait', 'say', 'one', 'look', 'see', 'thats', 'got', 'back']
    )

col1, col2, col3, col4 = st.columns(4)

for i, char in enumerate(colors.keys()):
    with eval(f"col{i+1}"):
        st.subheader(char.title())
        st.image(draw_cloud(char).to_array(), use_column_width=True)