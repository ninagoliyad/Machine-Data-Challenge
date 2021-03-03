# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 09:25:50 2021

@author: goliyn
"""

from pathlib import Path
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
plt.close("all")
from sqlalchemy import create_engine

#Directory to get all saved datafiles
input_dir = Path('./MachineData')

#Iterate over all files and save data to dataFrame
eqp_data = pd.DataFrame()
for filename in input_dir.iterdir():
    eqp_data = eqp_data.append(pd.read_csv(filename), ignore_index=True)

#Remove column with timestamps
eqp_data.drop(['Unnamed: 0'], axis=1, inplace=True)

#Remove outliers using z-score
z_scores = stats.zscore(eqp_data)
abs_z_scores = np.abs(z_scores)
filtered_entries = (abs_z_scores < 3).all(axis=1)
eqp_data = eqp_data[filtered_entries]

#Generate descriptive statistics
print(eqp_data.describe())
eqp_data.plot()

#Initialize DB connection and save dataframe to DB table
engine = create_engine('sqlite:///save_pandas.db', echo=False)
sqlite_connection = engine.connect()
sqlite_table = "Machine data"
eqp_data.to_sql(sqlite_table, sqlite_connection, if_exists='replace')
sqlite_connection.close()

#input()