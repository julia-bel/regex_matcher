from typing import Optional

import re
import json
import math
import pandas as pd
import matplotlib.pyplot as plt

from src.matcher.constants import MATCHING_PARAMS


def read_jsons(path: str, encoding: str = 'utf-8') -> pd.DataFrame:
    """
    Getting of aggregate information about regex matching.

    Args:
        path (str): path to .txt file that contains json strings.
        encoding (str): Defaults to 'utf-8'.

    Returns:
        pd.DataFrame: aggregate information
    """
    with open(path, 'r', encoding=encoding) as file:
        jsons = [json.loads(x) for x in file.readlines()]
    df = pd.DataFrame(data={col: [js[col] for js in jsons] for col in MATCHING_PARAMS})
    return df


def plot_dependance(
        path: str,
        target: Optional[str] = None,
        show: bool = False,
        encoding: str = 'utf-8',
        linestyle: str = '-o',
        multiplot: bool = False,
        columns: int = 3) -> None:
    """Plotting and saving visualization of length-time dependance.

    Args:
        path (str): path to .txt file that contains json strings.
        target (Optional[str], optional): path to save image. Defaults to None.
        show (bool, optional): plotting image. Defaults to False.
        encoding (str): Defaults to 'utf-8'.
        linestyle (str): matplotlib linestyle. Defaults to '-o'.
        multiplot (bool): whether to plot several images. Defaults to False.
        columns (int): number of columns to plot in multiplot. Defaults to 3.
    """ 
    df = read_jsons(path, encoding)
    regex = df.iloc[0]['regex']
    title = regex[1:-1] if re.match('^(.*)$', regex) else regex
    plt.figure(dpi=300)
    langs = df['language'].unique()
    if multiplot and len(langs) > 1:
        columns = min(columns, len(langs))
        rows = max(math.ceil(len(langs) / columns), 1)
        fig, axs = plt.subplots(rows, columns, figsize=(40,20))
        fig.suptitle(title, fontsize=25)
        axs = axs.flatten()
        for i, lang in enumerate(langs):
            sub_df = df[(df['language'] == lang) & df['valid']].sort_values(by='length')
            axs[i].plot(sub_df['length'], sub_df['time'], linestyle)
            axs[i].set(xlabel='Length, chars', ylabel='Time, seconds')
            axs[i].set_title(lang)
    else:
        legends = []
        for lang in langs:
            sub_df = df[(df['language'] == lang) & df['valid']].sort_values(by='length')
            plt.plot(sub_df['length'], sub_df['time'], linestyle)
            legends.append(lang)    
        plt.legend(legends, loc='upper left')
        plt.xlabel('Length, chars')
        plt.ylabel('Time, seconds')
        plt.title(title)
    if show:
        plt.show()
    if target is not None:
        plt.savefig(target)
