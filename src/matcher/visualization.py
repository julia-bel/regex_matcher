from typing import Optional

import json
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
    jsons = [json.loads(x) for x in open(path, 'r', encoding=encoding).readlines()]
    df = pd.DataFrame(data={col: [js[col] for js in jsons] for col in MATCHING_PARAMS})
    return df


def plot_dependance(
        path: str, 
        target: Optional[str] = None, 
        show: bool = False,
        encoding: str = 'utf-8') -> None:
    """Plotting and saving visualization of length-time dependance.

    Args:
        path (str): path to .txt file that contains json strings.
        target (Optional[str], optional): path to save image. Defaults to None.
        show (bool, optional): plotting image. Defaults to False.
        encoding (str): Defaults to 'utf-8'.
    """    
    legends = []
    df = read_jsons(path, encoding)
    plt.figure(dpi=300) 
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
