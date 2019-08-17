#! /usr/bin/env python3
try: 
    import pandas as pd
except:
    print("Fehler: Pandas ist nicht installiert. Bitte installieren")

import time
from datetime import datetime

import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory

def load_data(): 
    """
    Get filename via user request and load the CSV file as a pandas DataFrame. Returns Pandas DataFrame
    """
    tk.Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename()
    # das Obige ist 1:1 aus Stack Overflow kopiert: https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog
    with open(filename, "r") as infile: 
        data = pd.DataFrame.from_csv(infile, sep=";",index_col = None)
        return data

def transform_data(df):
    """ Take DataFrame and return new Dataframe with adjusted formatting"""
    try:
        df = df.rename(columns={' Time':'Time', ' Temp °C': 'Temp °C'})
    except:
        pass
    df['Datetime'] = df['Date'] + df['Time']
    print(df.dtypes)
    df['Datetime'].map(lambda x: datetime.strptime(x, '%d.%m.%Y %H:%M:%S'))
    new_df = df[['Datetime', 'Temp °C']]
    print(new_df)
    return new_df

def write_to_file(df):
    ''' write DataFrame to CSV file in directory chosen by the user '''
    filename = askdirectory()
    outfile_name = filename + "sensordata_transformed_{}.csv".format(datetime.now().date())
    outstring = df.to_csv(index=False, sep=';')
    with open(outfile_name, 'w') as outfile:
        outfile.write(outstring)

if __name__ == "__main__":
    df = load_data()
    new_df = transform_data(df)
    del df
    write_to_file(new_df)
    