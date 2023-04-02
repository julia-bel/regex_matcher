import json
import pandas as pd
import matplotlib.pyplot as plt


COLUMNS = ['valid', 'length', 'input', 'matched', 'time', 'regex', 'language']


def read_jsons(path):
    jsons = [json.loads(x) for x in open(path, 'r').readlines()]
    df = pd.DataFrame(data={col: [js[col] for js in jsons] for col in COLUMNS})
    return df


def plot_dependance(path, target=None, show=False):
    legends = []
    df = read_jsons(path)
    for lang in df['language'].unique():
        sub_df = df[(df['language'] == lang) & df['valid']].sort_values(by='length')
        plt.plot(sub_df['length'], sub_df['time'])
        legends.append(lang)    
    plt.legend(legends, loc='upper left')
    plt.xlabel('Length, chars')
    plt.ylabel('Time, seconds')
    plt.title(df.loc[0]['regex'])
    if show:
        plt.show()
    if target is not None:
        plt.savefig(target)
