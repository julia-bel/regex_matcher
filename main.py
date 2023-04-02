import sys
import json
import os
import subprocess

from src.visualization.utils import plot_dependance


SRC_DIR = os.environ['REGEX_MATCHER_ROOT'] + '/src'


def execute(paths, word, regex, target, timeout=3):
    for path in paths:
        try:
            if target == '':
                subprocess.run(f'{path} "{word}" "{regex}"', timeout=timeout, shell=True)
            else:
                subprocess.run(f'{path} "{word}" "{regex}" >> {target}', timeout=timeout, shell=True)
        except:
            print(f'Timeout: {path}')


def main():
    """
    sys.argv[1]: path to jsonfile
    
    {
        'languages': List[str] | '' | str, 
        'target_file': str, -- optipnal
        'regex': str,
        'word': str,
        'attack_group': {   -- optional 
            'prefix': str,
            'pump': str,
            'suffix': str,
            'limit': int (max iteration of pumping)
        }
        'visual_file': str, -- optional  
    }
    """    
    json_path = sys.argv[1]
    lang_map = {
        'javascript': f'{SRC_DIR}/javascript/query-node.js',
        'python': f'{SRC_DIR}/python/query-python.py',
        'rust': f'{SRC_DIR}/rust/target/release/query-rust',
        'go': f'{SRC_DIR}/go/query-go',
        'java': f'{SRC_DIR}/java/query-java.pl',
    }

    json_file = json.load(open(json_path, 'r'))
    target_file = json_file['target_file'] if 'target_file' in json_file else ''
    regex = json_file['regex']
    
    lang_paths = []
    if isinstance(json_file['languages'], list):
        lang_paths += [lang_map[lang] for lang in lang_map if lang in json_file['languages']]
    elif json_file['languages'] == '': 
        lang_paths += lang_map.values()
    else:
        lang_paths.append(lang_map[json_file['languages']])

    if 'attack_group' in json_file:
        prefix = json_file['attack_group']['prefix']
        pump = json_file['attack_group']['pump']
        suffix = json_file['attack_group']['suffix']
        limit = json_file['attack_group']['limit']
        for word in [prefix + pump * (n + 1) + suffix for n in range(limit)]:
            execute(lang_paths, word, regex, target_file)
        if 'visual_file' in json_file:
            plot_dependance(target_file, json_file['visual_file'])
    else:
        execute(lang_paths, json_file['word'], regex, target_file)

main()
