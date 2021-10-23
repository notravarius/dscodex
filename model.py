import os
import openai
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from IPython.core.display import display

import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random

def write_code(text):

    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
    engine="davinci-codex",
    prompt=f"<|endoftext|>/* I have a dataframe called df in pandas. Written for python. */\n/* Command: Remove NaN values from the dataframe */\ndf = df.dropna() \n\n/* Command: {text} */\n",
    temperature=0,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop= "/* Command:")

    return response.choices[0].text


def run_code(user_input):

    filename = listdir("static/files")
    df = pd.read_csv(f'static/files/{filename[0]}')

    text = write_code(user_input)
    text = text[:len(text) - 2]
    count = text.count("\n")

    for i in range(0,count+1):
        exec(f"res_{i} = " +  text.split("\n")[i])
        eval(f"res_{i}")
        df.to_csv(f'static/files/{filename[0]}', index=False)

        return eval(f"res_{i}")

def show_df():
    pd.options.display.width = 0
    filename = listdir("static/files")
    df = pd.read_csv(f'static/files/{filename[0]}')
    text = write_code("Show the first 10 rows")
    exec(f"res = " +  text)
    return eval(f"res")

def show_plot():
    filename = listdir("static/files")
    df = pd.read_csv(f'static/files/{filename[0]}')
    display(plt.scatter(df['Sales'], df['Profit']))
