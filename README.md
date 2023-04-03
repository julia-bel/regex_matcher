# Regex Matcher

## Installing
1. Set the environment variable `REGEX_MATCHER_ROOT=../regex_matcher`
2. Set configuration `perl configure`
3. Run `pip install -r requirements.txt`

## Matching
```
python main.py filename.json
```

filename.json
```
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
```

## Example
```
python main.py test/test.json
```
<p align="center">
    <img src="test/visual.png"/>
</p>