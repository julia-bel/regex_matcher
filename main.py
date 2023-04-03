import sys
import json

from src.matcher.regex_matcher import RegexMatcher


def main(encoding: str = 'utf-8'):
    """
    sys.argv[1]: path to json file of the format:
    {
        'regex': str, (target_file regex)
        'word': str,  (optional, input to match)
        'attack_group': Dict[str, Any], (optional, dictionary of the format
            {
                'prefix': str,
                'pump': str,
                'suffix': str,
                'steps': List[int], ([start, end, step], interval: [start, end))
            })
        'languages': List[str], (optional, languages to use, None means all)
        'target_file': str, (optional, file to save matching results)
        'visual_file': str, (optional, file to save visualization results)
        'encoding': str, (optional, global encoding, defaults to 'utf-8')
    }
    """
    assert len(sys.argv) == 2, f'usage: python {sys.argv[0]} jsonfile'
    matcher_params = json.load(open(sys.argv[1], 'r', encoding=encoding))
    matcher = RegexMatcher(**matcher_params)
    matcher.match()

main()
