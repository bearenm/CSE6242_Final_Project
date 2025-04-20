import pandas as pd
import numpy as np
import os

import re

def get_topic(text):
    match = re.search(r'\d+$', text)
    if match:
        return int(match.group())
    return None

df_dt=pd.read_csv('LDA_100_doc_topic_norm_augmented.csv')
df_tw=pd.read_csv('LDA_100_topic_word_norm_with_4_with_subclusters.csv')

df_dt=df_dt.drop('date',axis=1)


id_vars = ['company name', 'ticker', 'sector','industry','year','quarter']
var_name='topic'
value_name='size'

df=pd.melt(df_dt,id_vars=id_vars,var_name=var_name,value_name=value_name)

df=df.groupby(['sector','year','topic'],as_index=False).mean(numeric_only=True)

df['topic_id']=df['topic'].apply(get_topic)
df=df.drop('topic',axis=1)
df=pd.merge(df, df_tw, on='topic_id', how='left')[['sector_x','year','cluster_name','subcluster_name','topic_name','size']]
df.to_csv('melted_df2.csv')

