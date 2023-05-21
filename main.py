import json
import argparse

from src.matcher.regex_matcher import RegexMatcher
from src.matcher.visualization import plot_dependance


def main(encoding: str = 'utf-8'):
    parser = argparse.ArgumentParser(
        description='''Matching regular expressions with words or groups 
        of pumping words in Java, Python, Javascript, C++, Go, Rust 
        and measuring time consuming.''')
    parser.add_argument(
        'filename',
        help='''path to json file for matching\n{
        'regex': str, (target_file regex),
        'word': str,  (optional, input to match),
        'pump': Dict[str, Any], (optional, dictionary of the format:
        {
            'attack': List[List[str]|str], (e.g. [["a", "1"], "b", ["a", "1"]])
            'steps': Dict[str, List[int]], (e.g. {"1": [start, end, step]}, [start, end))
        }),
        'languages': List[str], (optional, languages to use, None means all),
        'target_file': str, (optional, file to save matching results),
        'encoding': str, (optional, global encoding, defaults to 'utf-8')\n}''')
    parser.add_argument(
        '-v', '--visualize',
        action='store',
        help='path to file for dependency visualization')
    parser.add_argument(
        '-m', '--multiplot',
        action='store_true',
        help='whether to plot several dependency images')
    
    args = parser.parse_args()
    matcher_params = json.load(open(args.filename, 'r', encoding=encoding))
    matcher = RegexMatcher(**matcher_params)
    matcher.match()
    if args.visualize is not None and matcher.target_file is not None:
        plot_dependance(
                matcher.target_file, args.visualize,
                encoding=encoding, multiplot=args.multiplot)


if __name__ == '__main__':
    main()
