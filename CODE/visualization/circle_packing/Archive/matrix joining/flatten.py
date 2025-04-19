import pandas as pd
import numpy as np
import json
from collections import defaultdict
import pickle
import os

os.chdir('C:/Users/gigar/OneDrive - Georgia Institute of Technology/Documents/CSE6242/Project/cluster_flat_tonest/')
df_dt=pd.read_csv('doc_topic_matrix.csv')
df_tw=pd.read_csv('topic_word_matrix.csv')

id_vars = ['company name', 'ticker', 'sector','year']
var_name='topic'
value_name='size'

df=pd.melt(df_dt,id_vars=id_vars,var_name=var_name,value_name=value_name)

df=pd.merge(df, df_tw, on='topic', how='left')[['company name','ticker','sector_x','year','C_1','C_2','C_3','C_4','topic','size']]
df.to_csv('melted_df.csv')
