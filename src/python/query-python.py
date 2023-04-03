#!/usr/bin/env python3

import sys
import json
import re
import time


def main():
    assert len(sys.argv) == 3, f'usage: {sys.argv[0]} input regex'

    result = {
        'input': sys.argv[1],
        'regex': sys.argv[2],
        'language': 'python',
        'valid': False,
        'length': len(sys.argv[1]),
        'matched': False,
        'time': 0,
    }

    try:
        regexp = re.compile("^" + result['regex'] + "$")
        result['valid'] = True
        start = time.perf_counter()
        match_result = regexp.match(result['input'])
        final = time.perf_counter()
        result['matched'] = bool(match_result)
        result['time'] = final - start
    except BaseException as error:
        result['valid'] = False
        log('Exception: ' + str(error))
    
    sys.stdout.write(json.dumps(result) + '\n')


def log(msg: str):
    sys.stderr.write(msg + '\n')


main()
