from subprocess import PIPE, Popen, TimeoutExpired
from typing import List, Optional, Any, Dict, Iterator
from dataclasses import dataclass

from src.matcher.constants import LANGUAGE_MAP


@dataclass
class RegexMatcher:
    """
    Matcher for regex on different regex machines.

    Args:
        regex (str): target_file regex.
        word (Optional[str], optional): input to match. Defaults to None.
        pump (Optional[Dict[str, Any]], optional): dictionary of the format:
            {
                'attack': List[List[str]|str], (e.g. [["a", "1"], "b", ["a", "1"]])
                'steps': Dict[str, List[int]], (e.g. {"1": [start, end, step]}, [start, end))
            }. Defaults to None.
        languages (Optional[List[str]], optional): languages to use, None means all. Defaults to None.
        target_file (Optional[str], optional): file to save matching results. Defaults to None.
        encoding (str, optional): global encoding. Defaults to 'utf-8'.
    """
    regex: str
    word: Optional[str] = None
    pump: Optional[Dict[str, List[Any]]] = None
    languages: Optional[List[str]] = None
    target_file: Optional[str] = None
    encoding: str = 'utf-8'

    def __post_init__(self):
        self.regex = self._format_regex(self.regex)
    
    def match(self, timeout: int = 1) -> None:

        def step_iterator(steps: Dict[str, List[int]]) -> Iterator[Dict[str, int]]:
            min_length = None
            iterable_steps = {}
            for k, v in steps.items():
                step_range = range(*v)
                if min_length is not None:
                    min_length = min(min_length, len(step_range))
                else:
                    min_length = len(step_range)
                iterable_steps[k] = iter(step_range)

            for _ in range(min_length):
                yield {k: next(v) for k, v in iterable_steps.items()}

        if isinstance(self.languages, list):
            paths = [LANGUAGE_MAP[lang] for lang in LANGUAGE_MAP if lang in self.languages]
        else:
            paths = LANGUAGE_MAP.values()
        write_file = None if self.target_file is None \
            else open(self.target_file, 'w', encoding=self.encoding)
        if self.pump is not None:
            attack = self.pump['attack']
            for step in step_iterator(self.pump['steps']):
                word = ''.join([a if isinstance(a, str) else a[0] * step[a[1]] for a in attack])
                self._match_word(paths, word, write_file, timeout)
        else:
            assert self.word is not None, 'define word or attack_group'
            self._match_word(paths, self.word, write_file, timeout)
        if write_file is not None:
            write_file.close()

    def _format_regex(self, regex: str) -> str:
        return regex

    def _match_word(
            self,
            paths: List[str],
            word: str,
            target_file: Optional[str] = None,
            timeout: int = 1) -> None:
        """
        Args:
            paths (List[str]): paths to executable files.
            word (str): input to match.
            target_file (Optional[str]): file to save matching results. Defaults to None.
            timeout (int, optional): matching timeout in seconds. Defaults to 1.
        """

        def execute(proc: Popen, timeout: int, path: str) -> Optional[bytes]:
            try:
                outs, _ = proc.communicate(timeout=timeout)
                return outs
            except TimeoutExpired:
                proc.kill()
                print(f'Timeout in {path}')

        for path in paths:
            if target_file is None:
                proc = Popen([path, word, self.regex])
                execute(proc, timeout, path)
            else:
                proc = Popen([path, word, self.regex], stdout=PIPE)
                outs = execute(proc, timeout, path)
                if outs is not None:
                    target_file.write(outs.decode(self.encoding))
