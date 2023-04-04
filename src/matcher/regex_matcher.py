from subprocess import PIPE, Popen, TimeoutExpired
from typing import List, Optional, Any, Dict
from dataclasses import dataclass

from src.matcher.visualization import plot_dependance
from src.matcher.constants import LANGUAGE_MAP


@dataclass
class RegexMatcher:
    """
    Matcher for regex on different regex machines.

    Args:
        regex (str): target_file regex.
        word (Optional[str], optional): input to match. Defaults to None.
        attack_group (Optional[Dict[str, Any]], optional): dictionary of the format:
            {
                'prefix': str,
                'pump': str,
                'suffix': str,
                'steps': List[int], ([start, end, step], interval: [start, end))
            }. Defaults to None.
        languages (Optional[List[str]], optional): languages to use, None means all. Defaults to None.
        target_file (Optional[str], optional): file to save matching results. Defaults to None.
        visual_file (Optional[str], optional): file to save visualization results. Defaults to None.
        encoding (str, optional): global encoding. Defaults to 'utf-8'.
    """
    regex: str
    word: Optional[str] = None
    attack_group: Optional[Dict[str, Any]] = None
    languages: Optional[List[str]] = None
    target_file: Optional[str] = None
    visual_file: Optional[str] = None
    encoding: str = 'utf-8'
    
    def match(self, timeout: int = 3) -> None:
        if isinstance(self.languages, list):
            paths = [LANGUAGE_MAP[lang] for lang in LANGUAGE_MAP if lang in self.languages]
        else:
            paths = LANGUAGE_MAP.values()
        write_file = None if self.target_file is None \
            else open(self.target_file, 'w', encoding=self.encoding)
        if self.attack_group is not None:
            prefix = self.attack_group['prefix']
            pump = self.attack_group['pump']
            suffix = self.attack_group['suffix']
            steps = self.attack_group['steps']
            for word in [prefix + pump * n + suffix for n in range(*steps)]:
                self._match_word(paths, word, write_file, timeout)
        else:
            assert self.word is not None, 'define word or attack_group'
            self._match_word(paths, self.word, write_file, timeout)
        if write_file is not None:
            write_file.close()
        if self.visual_file is not None and self.target_file is not None:
            plot_dependance(self.target_file, self.visual_file, encoding=self.encoding)

    def _format_regex(self, regex: str) -> str:
        return '(' + regex + ')'

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
